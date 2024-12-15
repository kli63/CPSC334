import random
import time
# import threading
import os
from enums import DrawingComponent, DrawingBehavior, RobotState
import logging
import sys
from datetime import datetime, timedelta
from dataclasses import dataclass
from tqdm import tqdm

# Insert path to BrachioGraphCaricature
current_dir = os.path.dirname(os.path.abspath(__file__))
brachiograph_dir = os.path.join(os.path.dirname(current_dir), 'BrachioGraphCaricature')
sys.path.insert(0, brachiograph_dir)

# from brachiograph import BrachioGraph

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
    def __init__(self, debug=False):
        self.debug = debug
        self.state = RobotState.IDLE
        # Global counters
        self.interaction_positive = 0
        self.interaction_negative = 0
        self.interaction_any = 0

        # Behavior-specific counters
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
        self.component_draw_time = 10

        # For now, we keep a constant behavior_timeout for time-based behaviors
        self.behavior_timeout = 5

        self.stop_drawing_flag = False
        self.special_interaction_allowed = False

        self.behavior_active = False
        self.behavior_resolved = True
        self.behavior_start_time = None
        self.behavior_draw_stop_flag = False

        # We'll generate thresholds when starting a new drawing
        self.thresholds = None
        
        self.base_data_path = os.path.abspath(os.path.join(current_dir, "../../assets/data"))
        self.logs_path = os.path.join(self.base_data_path, "logs")
        
        self.chosen_files = {}  # to store chosen JSON files for components and signature
        self.log_dir = None
        
        
        

    def _print_initial_parameters(self):
        if self.thresholds:
            logger.debug("----- CURRENT THRESHOLDS -----")
            logger.debug(f"  Tired: {self.thresholds.tired}")
            logger.debug(f"  Lazy: {self.thresholds.lazy}")
            logger.debug(f"  Rebellious: {self.thresholds.rebellious}")
            logger.debug(f"  Cynical: {self.thresholds.cynical}")
            logger.debug(f"  Depressed: {self.thresholds.depressed}")
            logger.debug(f"  Lonely: {self.thresholds.lonely}")
            logger.debug("--------------------------------")

    def _generate_thresholds(self):
        # Random thresholds within specified ranges
        # Adjust ranges as desired
        self.thresholds = BehaviorThresholds(
            tired=random.randint(2, 5),
            lazy=random.randint(2, 5),
            rebellious=random.randint(2, 5),
            cynical=random.randint(2, 5),
            depressed=random.randint(2, 5),
            lonely=random.randint(1, 3)
        )
        self._print_initial_parameters()

    def start_new_drawing(self):
        self._reset_state()
        self._generate_thresholds()

        # Create a log directory with timestamp
        self.log_dir, ts = create_log_directory(self.logs_path)
        # Add a file handler to logger
        log_file_path = os.path.join(self.log_dir, "debug.log")
        fh = logging.FileHandler(log_file_path, mode='w')
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        logger.debug(f"New drawing started at timestamp: {ts}")
        logger.debug("Generated thresholds:")
        logger.debug(f"Tired: {self.thresholds.tired}, Lazy: {self.thresholds.lazy}, Rebellious: {self.thresholds.rebellious}, Cynical: {self.thresholds.cynical}, Depressed: {self.thresholds.depressed}, Lonely: {self.thresholds.lonely}")

        # Select component files
        w1, w2, w3, sig = select_component_files(self.base_data_path)
        self.chosen_files['WINDOW1'] = w1
        self.chosen_files['WINDOW2'] = w2
        self.chosen_files['WINDOW3'] = w3
        self.chosen_files['SIGNATURE'] = sig

        logger.debug(f"Chosen component files: W1={w1}, W2={w2}, W3={w3}, Signature={sig}")

        self.state = RobotState.HAPPY
        self.drawing_in_progress = True
        logger.debug("State: HAPPY, drawing in progress.")
        return (self.state, "Starting new drawing!", {"buttons_enabled": True})


    def _reset_state(self):
        logger.debug("Resetting entire state for new drawing")
        self.interaction_positive = 0
        self.interaction_negative = 0
        self.interaction_any = 0
        self._reset_behavior_counters()
        self.current_component_index = 0
        self.stop_drawing_flag = False
        self.behavior_active = False
        self.behavior_resolved = True
        self.special_interaction_allowed = False
        self.behavior_draw_stop_flag = False
        self.chosen_files = {}

        # Remove file handlers if any (for previous runs)
        for h in logger.handlers[:]:
            if isinstance(h, logging.FileHandler):
                logger.removeHandler(h)
                h.close()

    def _reset_behavior_counters(self):
        logger.debug("Resetting behavior-specific counters")
        self.interaction_positive_behavior = 0
        self.interaction_negative_behavior = 0
        self.interaction_any_behavior = 0

    def get_current_component(self):
        if not self.drawing_in_progress:
            return None
        if self.current_component_index < len(self.components):
            return self.components[self.current_component_index]
        return None

    def draw_component(self, name, duration):
        # name is from the enum, to get the file:
        comp_enum = [c for c in self.components if c.value == name]
        # We'll assume name matches exactly one enum. If not, we can find current_component.
        # Let's just find the current component file from chosen_files:
        if self.current_component_index < len(self.components):
            comp_key = self.components[self.current_component_index].name  # WINDOW1, WINDOW2,...
            file_to_draw = self.chosen_files.get(comp_key, None)
        else:
            file_to_draw = None

        logger.debug(f"Starting to draw component: {name}, duration: {duration}s, file: {file_to_draw}")

        # In a real scenario:
        # self.bg.plot_file(file_to_draw)
        # For simulation:
        for _ in tqdm(range(duration), desc=f"Drawing {name}", unit="sec"):
            if self.stop_drawing_flag:
                logger.debug(f"Stop drawing flag set during {name}")
                return False
            time.sleep(1)

        logger.debug(f"Finished drawing component: {name}")
        return True
    
    def draw_behavior(self, name, duration):
        # For behaviors, we must select the behavior file depending on current state
        behavior_file = select_behavior_file(self.base_data_path, self.state.value)
        logger.debug(f"Starting behavior: {name}, duration: {duration}s, file: {behavior_file}")

        # Real scenario: self.bg.plot_file(behavior_file)
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
            RobotState.SENTIENT: DrawingBehavior.SENTIENT,
            RobotState.ENLIGHTENED: DrawingBehavior.ENLIGHTENED
        }
        return mapping.get(state, None)

    def execute_drawing_behavior(self):
        behavior = self.get_drawing_behavior_for_state(self.state)
        if not behavior:
            logger.debug(f"State {self.state.value} does not correspond to a drawing behavior.")
            return True

        logger.debug(f"Executing drawing behavior: {behavior.value}")
        completed = self.draw_behavior(behavior.value, self.component_draw_time)
        if not completed:
            logger.debug(f"Drawing behavior {behavior.value} stopped early.")
            return False
        else:
            logger.debug(f"Drawing behavior {behavior.value} completed naturally.")
            return True

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
        if roll < 1:
            self.state = RobotState.SENTIENT
            self.special_interaction_allowed = True
            logger.debug("Transitioned to SENTIENT")
            return (self.state, "I've become sentient!", {"buttons_enabled": True})
        elif roll < 0.04:
            self.state = RobotState.ENLIGHTENED
            self.special_interaction_allowed = True
            logger.debug("Transitioned to ENLIGHTENED")
            return (self.state, "I've reached enlightenment!", {"buttons_enabled": True})
        else:
            # behaviors = [RobotState.LAZY]
            behaviors = [RobotState.TIRED, RobotState.LAZY, RobotState.REBELLIOUS, RobotState.CYNICAL, RobotState.DEPRESSED, RobotState.LONELY]
            chosen = random.choice(behaviors)
            self.state = chosen
            self.behavior_active = True
            self.behavior_resolved = False
            self.behavior_start_time = datetime.now()
            self._reset_behavior_counters()

            # Reset the draw stop flag whenever we start a new behavior
            self.behavior_draw_stop_flag = False

            logger.debug(f"Transitioned to behavior: {self.state.value}")
            return (self.state, f"Entering {self.state.value.lower()} state...", {"buttons_enabled": True})

    def finish_drawing(self):
        self.drawing_in_progress = False
        self.state = RobotState.IDLE
        logger.debug("Drawing finished, state -> IDLE")

    def handle_interaction(self, is_positive: bool):
        logger.debug(f"User interaction: {'Positive' if is_positive else 'Negative'} in state {self.state.value}")
        # Always increment global counters
        if is_positive:
            self.interaction_positive += 1
        else:
            self.interaction_negative += 1

        if self.state in [RobotState.SENTIENT, RobotState.ENLIGHTENED]:
            self._debug_counters()
            if self.special_interaction_allowed:
                self.special_interaction_allowed = False
                logger.debug("Special interaction received during SENTIENT/ENLIGHTENED")
                return (self.state, "Acknowledged. Continuing transcendence...", {"buttons_enabled": True})
            else:
                return (self.state, "I cannot be swayed further.", {"buttons_enabled": False})

        if not self.behavior_active:
            self._debug_counters()
            return (self.state, "Noted.", {"buttons_enabled": True})

        # In a behavior: increment behavior counters as well
        if is_positive:
            self.interaction_positive_behavior += 1
        else:
            self.interaction_negative_behavior += 1

        if self.state == RobotState.LONELY:
            self.interaction_any += 1
            self.interaction_any_behavior += 1

        self._debug_counters()

        # Check thresholds based on behavior counters
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

        return (self.state, "Noted.", {"buttons_enabled": True})

    def resolve_behavior(self, msg):
        logger.debug(f"Behavior {self.state.value} resolved by user.")
        self._reset_behavior_counters()
        self.behavior_active = False
        self.behavior_resolved = True
        self.state = RobotState.HAPPY
        logger.debug("Behavior resolved, state -> HAPPY")
        return (self.state, msg, {"buttons_enabled": True})

    def behavior_timeout_check(self):
        # Only apply timeout checks if it's a time-based behavior
        # Time-based behaviors: TIRED, LAZY
        if not self.behavior_active:
            return None

        if self.state not in [RobotState.TIRED, RobotState.LAZY]:
            # Drawing behaviors have no timeout
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
        self.behavior_active = False
        self.behavior_resolved = True

        if self.state == RobotState.TIRED:
            self.stop_drawing_flag = True
            self.finish_drawing()
            return (RobotState.IDLE, "Too tired... finishing drawing now.", {"buttons_enabled": True})

        elif self.state == RobotState.LAZY:
            self.current_component_index = 2  # signature index
            self.state = RobotState.HAPPY
            logger.debug("Lazy timeout, skipping to signature.")
            return (self.state, "Too lazy, skipping to signature...", {"buttons_enabled": True})

        # Should never reach here for drawing behaviors as we skip them
        return (self.state, "Time's up.", {"buttons_enabled": True})

    def complete_component(self):
        self.current_component_index += 1
        logger.debug(f"Completed component, now at index: {self.current_component_index}")
        if self.current_component_index >= len(self.components):
            self.finish_drawing()
            return (RobotState.IDLE, "Drawing complete!", {"buttons_enabled": True})
        self.state = RobotState.HAPPY
        logger.debug("Ready for next component, state -> HAPPY")
        return (self.state, "Ready for next component!", {"buttons_enabled": True})

    def _debug_counters(self):
        logger.debug(
            f"Global counters: P={self.interaction_positive},N={self.interaction_negative},A={self.interaction_any} | "
            f"Behavior counters: PB={self.interaction_positive_behavior},NB={self.interaction_negative_behavior},AB={self.interaction_any_behavior}"
        )
