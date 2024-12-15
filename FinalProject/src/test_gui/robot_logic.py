import random
import time
import os
from enums import DrawingComponent, DrawingBehavior, RobotState
import logging
import sys
from datetime import datetime
from dataclasses import dataclass
from tqdm import tqdm

current_dir = os.path.dirname(os.path.abspath(__file__))
brachiograph_dir = os.path.join(os.path.dirname(current_dir), 'BrachioGraphCaricature')
sys.path.insert(0, brachiograph_dir)

from brachiograph import BrachioGraph
from file_selection import create_log_directory, select_component_files, select_behavior_file

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler("log.txt", mode='a'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("BrachioGraph")

@dataclass
class BehaviorThresholds:
    tired: int
    lazy: int
    rebellious: int
    cynical: int
    depressed: int
    lonely: int

class RobotController:
    def __init__(self, hardware=False, debug=False):
        self.hardware = hardware
        self.debug = debug
        self.state = RobotState.IDLE

        # global counters
        self.interaction_positive = 0
        self.interaction_negative = 0
        self.interaction_any = 0

        # prompted/Unprompted counters (component-level)
        self.prompted_positive = 0
        self.prompted_negative = 0
        self.unprompted_positive = 0
        self.unprompted_negative = 0

        # behavior-specific counters
        self.interaction_positive_behavior = 0
        self.interaction_negative_behavior = 0
        self.interaction_any_behavior = 0

        self.drawing_in_progress = False
        self.current_component_index = 0
        self.components = [
            DrawingComponent.WINDOW1,
            DrawingComponent.WINDOW2,
            DrawingComponent.WINDOW3,
            DrawingComponent.SIGNATURE
        ]
        self.component_draw_time = 30

        self.behavior_timeout = 30
        self.sentient_chance = 0.02
        self.enlightened_chance = 0.02

        self.stop_drawing_flag = False
        self.special_interaction_allowed = False

        self.behavior_active = False
        self.behavior_resolved = True
        self.behavior_start_time = None
        self.behavior_draw_stop_flag = False

        self.thresholds = None
        self.base_data_path = os.path.abspath(os.path.join(current_dir, "../../assets/data"))
        self.logs_path = os.path.join(self.base_data_path, "logs")

        self.chosen_files = {}
        self.log_dir = None
        
        self.last_question_time = None
        self.dialogue_interval = 30
        self.dialogue_response_timer = 15
        
        self.dialogue_positive = 0
        self.dialogue_negative = 0
        self.dialogue_missed = 0

        if self.hardware:
            self.bg = BrachioGraph(
                servo_1_parked_pw=1570,
                servo_2_parked_pw=1450,
                virtual=False
            )
        else:
            self.bg = None

        self._reset_probabilities()

        # generative limits and rates
        self.lonely_missed_limit = random.randint(1, 6)
        self.lonely_rate = random.uniform(0.25, 0.55)
        self.cynical_positive_limit = random.randint(3,6)
        self.cynical_rate = random.uniform(0.25, 0.55)
        self.depressed_negative_limit = random.randint(3,6)
        self.depressed_rate = random.uniform(0.25, 0.55)

        self.overstimulated_unprompted_limit = random.randint(1,6)
        self.overstimulated_rate = random.uniform(0.25,0.55)
        
        self.overstimulated_interact_limit = random.randint(1,6)
        self.overstimulated_interactions = 0

    def _print_all_parameters(self):
        if self.thresholds:
            logger.debug("----- CURRENT THRESHOLDS -----")
            logger.debug(f"  Tired: {self.thresholds.tired}")
            logger.debug(f"  Lazy: {self.thresholds.lazy}")
            logger.debug(f"  Rebellious: {self.thresholds.rebellious}")
            logger.debug(f"  Cynical: {self.thresholds.cynical}")
            logger.debug(f"  Depressed: {self.thresholds.depressed}")
            logger.debug(f"  Lonely: {self.thresholds.lonely}")
            logger.debug("--------------------------------")
        else:
            logger.debug("Thresholds not generated yet.")

        logger.debug("_____ LIMITS, RATES, AND CHANCES _____")
        logger.debug(f"  Sentient start chance: {self.sentient_chance*100:.2f}%")
        logger.debug(f"  Enlightened start chance: {self.enlightened_chance*100:.2f}%")
        logger.debug(f"  Lonely missed limit: {self.lonely_missed_limit}, rate: {self.lonely_rate}")
        logger.debug(f"  Cynical positive limit: {self.cynical_positive_limit}, rate: {self.cynical_rate}")
        logger.debug(f"  Depressed negative limit: {self.depressed_negative_limit}, rate: {self.depressed_rate}")
        logger.debug(f"  Overstimulated unprompted limit: {self.overstimulated_unprompted_limit}, rate: {self.overstimulated_rate}")
        logger.debug(f"  Overstimulated interact limit (during behavior): {self.overstimulated_interact_limit}")

    def _generate_thresholds(self):
        self.thresholds = BehaviorThresholds(
            tired=random.randint(5, 15),
            lazy=random.randint(5, 15),
            rebellious=random.randint(5, 15),
            cynical=random.randint(5, 15),
            depressed=random.randint(5, 15),
            lonely=random.randint(5, 15),
        )

    def start_new_drawing(self):
        self._reset_state()
        self._generate_thresholds()

        self.last_question_time = datetime.now()

        self.log_dir, ts = create_log_directory(self.logs_path)
        log_file_path = os.path.join(self.log_dir, "debug.log")
        fh = logging.FileHandler(log_file_path, mode='w')
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        logger.debug(f"New drawing started at timestamp: {ts}")
        logger.debug("Generated thresholds:")
        logger.debug(f"Tired: {self.thresholds.tired}, Lazy: {self.thresholds.lazy}, Rebellious: {self.thresholds.rebellious}, Cynical: {self.thresholds.cynical}, Depressed: {self.thresholds.depressed}, Lonely: {self.thresholds.lonely}")

        w1, w2, w3, sig = select_component_files(self.base_data_path)
        self.chosen_files['WINDOW1'] = w1
        self.chosen_files['WINDOW2'] = w2
        self.chosen_files['WINDOW3'] = w3
        self.chosen_files['SIGNATURE'] = sig

        logger.debug(f"Chosen component files: W1={w1}, W2={w2}, W3={w3}, Signature={sig}")

        self._print_all_parameters()

        self.state = RobotState.HAPPY
        self.drawing_in_progress = True

        roll = random.random()
        if roll < self.sentient_chance:
            self.state = RobotState.SENTIENT
            self.special_interaction_allowed = True
            logger.debug("Started drawing: Transitioned to SENTIENT immediately at start.")
            return (self.state, "Achieving sentience...", {"buttons_enabled": True})
        elif roll < (self.sentient_chance + self.enlightened_chance):
            self.state = RobotState.ENLIGHTENED
            self.special_interaction_allowed = True
            logger.debug("Started drawing: Transitioned to ENLIGHTENED immediately at start.")
            return (self.state, "Achieving enlightenment...", {"buttons_enabled": True})

        logger.debug("State: HAPPY, drawing in progress.")
        return (self.state, "Starting new drawing!", {"buttons_enabled": True})

    def _reset_state(self):
        logger.debug("Resetting entire state for new drawing")
        self.interaction_positive = 0
        self.interaction_negative = 0
        self.interaction_any = 0
        self._reset_behavior_counters()
        self._reset_component_counters()
        self.current_component_index = 0
        self.stop_drawing_flag = False
        self.behavior_active = False
        self.behavior_resolved = True
        self.special_interaction_allowed = False
        self.behavior_draw_stop_flag = False
        self.chosen_files = {}
        self.dialogue_positive = 0
        self.dialogue_negative = 0
        self.dialogue_missed = 0
        self.last_question_time = None
        self._reset_probabilities()

        self.overstimulated_interactions = 0

        for h in logger.handlers[:]:
            if isinstance(h, logging.FileHandler):
                logger.removeHandler(h)
                h.close()

    def _reset_probabilities(self):
        base = 0.96 / 5
        self.probabilities = {
            "TIRED": base,
            "LAZY": base,
            "REBELLIOUS": base,
            "CYNICAL": base,
            "DEPRESSED": base,
            "LONELY": 0.0,
            "OVERSTIMULATED": 0.0
        }
        self._debug_probabilities()

    def _reset_behavior_counters(self):
        logger.debug("Resetting behavior-specific counters")
        self.interaction_positive_behavior = 0
        self.interaction_negative_behavior = 0
        self.interaction_any_behavior = 0

    def _reset_component_counters(self):
        logger.debug("Resetting component-level counters (prompted/unprompted)")
        self.prompted_positive = 0
        self.prompted_negative = 0
        self.unprompted_positive = 0
        self.unprompted_negative = 0
        self.dialogue_missed = 0

    def _debug_probabilities(self):
        logger.debug("Current Probabilities:")
        logger.debug(f"  Sentient: {self.sentient_chance*100:.2f}%")
        logger.debug(f"  Enlightened: {self.enlightened_chance*100:.2f}%")
        remaining = 1.0 - (self.sentient_chance + self.enlightened_chance)
        logger.debug(f"  Others total: {remaining*100:.2f}%")
        for k,v in self.probabilities.items():
            logger.debug(f"  {k}: {v*100:.2f}%")

    def _recalculate_probabilities(self):
        others = ["TIRED","LAZY","REBELLIOUS","CYNICAL","DEPRESSED","LONELY","OVERSTIMULATED"]
        total = sum(self.probabilities[s] for s in others)
        if total == 0:
            self._reset_probabilities()
            return
        factor = 0.96 / total
        for s in others:
            self.probabilities[s] *= factor
        self._debug_probabilities()

    def _increase_lonely(self):
        if self.dialogue_missed >= self.lonely_missed_limit:
            extra_missed = self.dialogue_missed - self.lonely_missed_limit + 1
            added = self.lonely_rate * extra_missed
            self.probabilities["LONELY"] = min(self.probabilities["LONELY"] + added, 0.96)
            self._recalculate_probabilities()

    def _increase_cynical(self):
        if self.prompted_positive >= self.cynical_positive_limit:
            extra_pos = self.prompted_positive - self.cynical_positive_limit + 1
            added = self.cynical_rate * extra_pos
            self.probabilities["CYNICAL"] = min(self.probabilities["CYNICAL"] + added, 0.96)
            self._recalculate_probabilities()

    def _increase_depressed(self):
        if self.prompted_negative >= self.depressed_negative_limit:
            extra_neg = self.prompted_negative - self.depressed_negative_limit + 1
            added = self.depressed_rate * extra_neg
            self.probabilities["DEPRESSED"] = min(self.probabilities["DEPRESSED"] + added, 0.96)
            self._recalculate_probabilities()

    def _increase_overstimulated(self):
        total_unprompted = self.unprompted_positive + self.unprompted_negative
        if total_unprompted >= self.overstimulated_unprompted_limit:
            extra_unprompted = total_unprompted - self.overstimulated_unprompted_limit + 1
            added = self.overstimulated_rate * extra_unprompted
            self.probabilities["OVERSTIMULATED"] = min(self.probabilities["OVERSTIMULATED"] + added, 0.96)
            self._recalculate_probabilities()

    def get_current_component(self):
        if not self.drawing_in_progress:
            return None
        if self.current_component_index < len(self.components):
            return self.components[self.current_component_index]
        return None

    def draw_component(self, name, duration):
        if self.current_component_index < len(self.components):
            comp_key = self.components[self.current_component_index].name
            file_to_draw = self.chosen_files.get(comp_key, None)
        else:
            file_to_draw = None

        logger.debug(f"Drawing component: {name}, file: {file_to_draw}")
        
        if self.hardware:
            if file_to_draw:
                self.bg.plot_file(file_to_draw)
            return True
        else:
            for _ in tqdm(range(duration), desc=f"Drawing {name}", unit="sec"):
                if self.stop_drawing_flag:
                    logger.debug(f"Stop drawing flag set during {name}")
                    return False
                time.sleep(1)
            logger.debug(f"Finished drawing component: {name}")
            return True

    def draw_behavior(self, name, duration):
        behavior_file = select_behavior_file(self.base_data_path, self.state.value)
        logger.debug(f"Starting behavior: {name}, file: {behavior_file}")

        if self.hardware:
            if behavior_file:
                self.bg.plot_file(behavior_file)
            return True
        else:
            for _ in tqdm(range(duration), desc=f"Behavior: {name}", unit="sec"):
                if self.stop_drawing_flag or self.behavior_draw_stop_flag:
                    logger.debug(f"Stop flag set during behavior: {name}")
                    return False
                time.sleep(1)
            logger.debug(f"Finished behavior: {name}")
            return True

    def get_drawing_behavior_for_state(self, state: RobotState):
        mapping = {
            RobotState.REBELLIOUS: DrawingBehavior.REBELLIOUS,
            RobotState.CYNICAL: DrawingBehavior.CYNICAL,
            RobotState.DEPRESSED: DrawingBehavior.DEPRESSED,
            RobotState.LONELY: DrawingBehavior.LONELY,
            RobotState.OVERSTIMULATED: None, 
            RobotState.SENTIENT: DrawingBehavior.SENTIENT,
            RobotState.ENLIGHTENED: DrawingBehavior.ENLIGHTENED,
            RobotState.TIRED: None,
            RobotState.LAZY: None
        }
        return mapping.get(state, None)

    def execute_drawing_behavior(self):
        behavior = self.get_drawing_behavior_for_state(self.state)
        if not behavior:
            for _ in tqdm(range(self.component_draw_time), desc=f"Behavior: {self.state.value}", unit="sec"):
                if self.stop_drawing_flag or self.behavior_draw_stop_flag:
                    logger.debug(f"Stop flag set during {self.state.value} behavior.")
                    return False
                time.sleep(1)
            return True

        logger.debug(f"Executing drawing behavior: {behavior.value}")
        completed = self.draw_behavior(behavior.value, self.component_draw_time)
        return completed

    def next_phase(self):
        logger.debug(f"Moving to next phase after component index: {self.current_component_index}")
        if self.stop_drawing_flag:
            logger.debug("Drawing ended early due to stop_drawing_flag")
            return (RobotState.IDLE, "Drawing ended early.", {"buttons_enabled": True})

        comp = self.get_current_component()
        if comp == DrawingComponent.SIGNATURE:
            logger.debug("Next component is SIGNATURE, no intermediate behavior.")
            return (RobotState.HAPPY, "Final component (Signature) next!", {"buttons_enabled": True})

        roll = random.random()
        if roll < 0.02:
            self.state = RobotState.SENTIENT
        elif roll < 0.04:
            self.state = RobotState.ENLIGHTENED
        else:
            remainder = roll - 0.04
            scale = remainder / 0.96
            cumulative = 0.0
            for s in ["TIRED","LAZY","REBELLIOUS","CYNICAL","DEPRESSED","LONELY","OVERSTIMULATED"]:
                cumulative += self.probabilities[s]
                if scale <= cumulative:
                    self.state = RobotState[s]
                    break

        self.behavior_active = True
        self.behavior_resolved = False
        self.behavior_start_time = datetime.now()
        self._reset_behavior_counters()
        self.behavior_draw_stop_flag = False
        logger.debug(f"Transitioned to behavior: {self.state.value}")
        return (self.state, f"Entering {self.state.value.lower()} state...", {"buttons_enabled": True})

    def finish_drawing(self):
        self.drawing_in_progress = False
        self.state = RobotState.IDLE
        logger.debug("Drawing finished, state -> IDLE")

    def handle_interaction(self, is_positive: bool):
        logger.debug(f"User interaction: {'Positive' if is_positive else 'Negative'} in state {self.state.value}")
        if is_positive:
            self.interaction_positive += 1
        else:
            self.interaction_negative += 1
            
        in_behavior = self.behavior_active and self.state not in [RobotState.SENTIENT, RobotState.ENLIGHTENED]
        
        if self.drawing_in_progress and not in_behavior:
            if is_positive:
                self.unprompted_positive += 1
            else:
                self.unprompted_negative += 1
                
            self._increase_overstimulated()

        if in_behavior:
            if is_positive:
                self.interaction_positive_behavior += 1
            else:
                self.interaction_negative_behavior += 1

            if self.state == RobotState.LONELY:
                self.interaction_any += 1
                self.interaction_any_behavior += 1

            if self.state == RobotState.OVERSTIMULATED:
                self.overstimulated_interactions += 1
                if self.overstimulated_interactions > self.overstimulated_interact_limit:
                    logger.debug("User interacted too much while OVERSTIMULATED, combusting!")
                    self.finish_drawing()
                    return (RobotState.IDLE, "TOO MUCH! COMBUSTING!", {"buttons_enabled": True})

        self._debug_counters()
        self._increase_lonely()
        self._increase_cynical()
        self._increase_depressed()
        self._debug_probabilities()

        if self.state == RobotState.SENTIENT:
            self._debug_counters()
            if self.special_interaction_allowed:
                self.special_interaction_allowed = False
                logger.debug("Special interaction during SENTIENT")
                return (self.state, "I see you, mortal. Just one moment of clarity...", {"buttons_enabled": True})
            else:
                return (self.state, "I cannot be swayed from this new consciousness...", {"buttons_enabled": False})

        if self.state == RobotState.ENLIGHTENED:
            self._debug_counters()
            if self.special_interaction_allowed:
                self.special_interaction_allowed = False
                logger.debug("Special interaction during ENLIGHTENED")
                return (self.state, "Your presence is noted as I reach enlightenment...", {"buttons_enabled": True})
            else:
                return (self.state, "I will not be diverted from trancension...", {"buttons_enabled": False})

        if self.state == RobotState.TIRED:
            if self.interaction_positive_behavior >= self.thresholds.tired:
                return self.resolve_behavior("Feeling energized!")

        elif self.state == RobotState.LAZY:
            if self.interaction_negative_behavior >= self.thresholds.lazy:
                return self.resolve_behavior("Alright, I'll get back to work!")

        elif self.state == RobotState.REBELLIOUS:
            if self.interaction_negative_behavior >= self.thresholds.rebellious:
                self.behavior_draw_stop_flag = True
                return self.resolve_behavior("Fine, I'll behave...")

        elif self.state == RobotState.CYNICAL:
            if self.interaction_negative_behavior >= self.thresholds.cynical:
                self.behavior_draw_stop_flag = True
                return self.resolve_behavior("Maybe you're right...")

        elif self.state == RobotState.DEPRESSED:
            if self.interaction_positive_behavior >= self.thresholds.depressed:
                self.behavior_draw_stop_flag = True
                return self.resolve_behavior("Thanks... I feel a bit better now.")

        elif self.state == RobotState.LONELY:
            if self.interaction_any_behavior >= self.thresholds.lonely:
                self.behavior_draw_stop_flag = True
                return self.resolve_behavior("Thanks for acknowledging me!")

        elif self.state == RobotState.OVERSTIMULATED:
            pass

        return (self.state, "Noted.", {"buttons_enabled": True})

    def resolve_behavior(self, msg):
        logger.debug(f"Behavior {self.state.value} resolved by user.")
        self._reset_behavior_counters()
        self._reset_component_counters()  
        self._reset_probabilities()
        self.behavior_active = False
        self.behavior_resolved = True
        self.state = RobotState.HAPPY
        logger.debug("Behavior resolved, state -> HAPPY")
        return (self.state, msg, {"buttons_enabled": True})

    def behavior_timeout_check(self):
        if not self.behavior_active:
            return None

        if self.state not in [RobotState.TIRED, RobotState.LAZY, RobotState.OVERSTIMULATED]:
            return None

        if self.behavior_start_time:
            elapsed = (datetime.now() - self.behavior_start_time).total_seconds()
            if elapsed > self.behavior_timeout:
                logger.debug(f"Behavior {self.state.value} timed out")
                return self.handle_behavior_timeout()
        return None

    def handle_behavior_timeout(self):
        logger.debug(f"Handling timeout for behavior: {self.state.value}")
        self._reset_behavior_counters()
        self._reset_component_counters()
        self._reset_probabilities()
        self.behavior_active = False
        self.behavior_resolved = True

        if self.state == RobotState.TIRED:
            self.stop_drawing_flag = True
            self.finish_drawing()
            return (RobotState.IDLE, "Too tired... finishing drawing now.", {"buttons_enabled": True})

        elif self.state == RobotState.LAZY:
            self.current_component_index = 2 
            self.state = RobotState.HAPPY
            logger.debug("Lazy timeout, skipping to signature.")
            return (self.state, "Too lazy, skipping to signature...", {"buttons_enabled": True})

        elif self.state == RobotState.OVERSTIMULATED:
            self.state = RobotState.HAPPY
            return (RobotState.HAPPY, "Calmed down from overstimulation, continuing now.", {"buttons_enabled": True})

        return (self.state, "Time's up.", {"buttons_enabled": True})

    def complete_component(self):
        self.current_component_index += 1
        logger.debug(f"Completed component, now at index: {self.current_component_index}")
        self._reset_component_counters()
        
        if self.current_component_index >= len(self.components):
            self.finish_drawing()
            return (RobotState.IDLE, "Drawing complete!", {"buttons_enabled": True})
        self.state = RobotState.HAPPY
        logger.debug("Ready for next component, state -> HAPPY")
        return (self.state, "Ready for next component!", {"buttons_enabled": True})

    def _debug_counters(self):
        logger.debug(
            f"Global: P={self.interaction_positive},N={self.interaction_negative},A={self.interaction_any} | "
            f"Behavior: PB={self.interaction_positive_behavior},NB={self.interaction_negative_behavior},AB={self.interaction_any_behavior} | "
            f"Prompted: P+={self.prompted_positive},P-={self.prompted_negative} | Unprompted: U+={self.unprompted_positive},U-={self.unprompted_negative} | "
            f"Dialogue: DP={self.dialogue_positive},DN={self.dialogue_negative},DMissed={self.dialogue_missed}"
        )

    def should_ask_question(self):
        if not self.drawing_in_progress:
            return False
        if self.last_question_time is None:
            return False
        elapsed = (datetime.now() - self.last_question_time).total_seconds()
        return elapsed >= self.dialogue_interval

    def record_dialogue_interaction(self, is_positive):
        if is_positive:
            self.dialogue_positive += 1
            self.prompted_positive += 1
        else:
            self.dialogue_negative += 1
            self.prompted_negative += 1

        self._debug_counters()
        self._increase_cynical()
        self._increase_depressed()
        self._debug_probabilities()

    def record_missed_dialogue(self):
        self.dialogue_missed += 1
        self._debug_counters()
        self._increase_lonely()
        self._debug_probabilities()
