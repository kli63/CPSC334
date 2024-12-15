# robot_logic.py

import random
import time
from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging
import sys

from question_bank import get_questions_for_state

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler("log.txt", mode='a'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("BrachioGraph")
logger.info("----- New Run Started at %s -----", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

class DrawingComponent(Enum):
    WINDOW1 = "Window 1"
    WINDOW2 = "Window 2"
    WINDOW3 = "Window 3"
    SIGNATURE = "Signature"

class RobotState(Enum):
    IDLE = "IDLE"
    HAPPY = "HAPPY"
    TIRED = "TIRED"
    LAZY = "LAZY"
    REBELLIOUS = "REBELLIOUS"
    CYNICAL = "CYNICAL"
    DEPRESSED = "DEPRESSED"
    LONELY = "LONELY"
    OVERSTIMULATED = "OVERSTIMULATED"
    SENTIENT = "SENTIENT"
    ENLIGHTENED = "ENLIGHTENED"

@dataclass
class BehaviorParameters:
    lazy_threshold: int
    tired_threshold: int
    rebellious_threshold: int
    cynical_threshold: int
    depressed_threshold: int
    loneliness_limit: int
    loneliness_rate: float
    stimulation_limit: int
    stimulation_rate: float
    cynical_limit: int
    cynical_rate: float
    depressed_limit: int
    depressed_rate: float
    overstimulation_interaction_limit: int = 1

class RobotController:
    def __init__(self):
        self.state = RobotState.IDLE
        self.parameters = None
        self.behavior_start_time = None
        self.last_prompt_time = None
        self.timeout_end_time = None
        self.interaction_count = 0
        self.missed_interactions = 0
        self.extra_interactions = 0
        self.prompted_positive = 0
        self.prompted_negative = 0
        self.unprompted_positive = 0
        self.unprompted_negative = 0

        self.current_component = 0
        self.drawing_in_progress = False
        self.components = [
            DrawingComponent.WINDOW1,
            DrawingComponent.WINDOW2,
            DrawingComponent.WINDOW3,
            DrawingComponent.SIGNATURE
        ]

        # Reduced times for faster testing
        self.component_draw_time = 60
        self.prompt_interval = 30

        self.loneliness_probability = 0
        self.overstimulation_probability = 0
        self.cynical_probability = 0
        self.depressed_probability = 0

        self.overstimulated_interaction_count = 0
        self.special_interaction_allowed = False
        self.behavior_active = False
        self.behavior_resolved = True

    def start_new_drawing(self):
        self._generate_parameters()
        self._reset_state()

        # Check for special states at start (10% chance each)
        if random.random() < 0.1:
            self.state = RobotState.SENTIENT
            self.drawing_in_progress = True
            self.special_interaction_allowed = True
            logger.debug("Special state at start: SENTIENT")
            return (self.state, "Achieving sentience...", {"buttons_enabled": True})
        elif random.random() < 0.1:
            self.state = RobotState.ENLIGHTENED
            self.drawing_in_progress = True
            self.special_interaction_allowed = True
            logger.debug("Special state at start: ENLIGHTENED")
            return (self.state, "Reaching enlightenment...", {"buttons_enabled": True})

        self.drawing_in_progress = True
        self.current_component = 0
        self.state = RobotState.HAPPY
        logger.debug("Starting new drawing with HAPPY state")
        self._print_thresholds()
        return (self.state, "Starting new drawing!", {"buttons_enabled": True})

    def _generate_parameters(self):
        self.parameters = BehaviorParameters(
            lazy_threshold=random.randint(5, 15),
            tired_threshold=random.randint(5, 15),
            rebellious_threshold=random.randint(5, 15),
            cynical_threshold=random.randint(5, 15),
            depressed_threshold=random.randint(5, 15),
            loneliness_limit=random.randint(2, 5),
            loneliness_rate=random.uniform(0.2, 0.4),
            stimulation_limit=random.randint(3, 6),
            stimulation_rate=random.uniform(0.15, 0.3),
            cynical_limit=random.randint(3, 6),
            cynical_rate=random.uniform(0.1, 0.25),
            depressed_limit=random.randint(3, 6),
            depressed_rate=random.uniform(0.1, 0.25),
            overstimulation_interaction_limit=random.randint(1,2)
        )

    def _reset_state(self):
        self.interaction_count = 0
        self.missed_interactions = 0
        self.extra_interactions = 0
        self.prompted_positive = 0
        self.prompted_negative = 0
        self.unprompted_positive = 0
        self.unprompted_negative = 0
        self.loneliness_probability = 0
        self.overstimulation_probability = 0
        self.cynical_probability = 0
        self.depressed_probability = 0
        self.behavior_start_time = None
        self.last_prompt_time = datetime.now()
        self.timeout_end_time = None
        self.overstimulated_interaction_count = 0
        self.special_interaction_allowed = False
        self.behavior_active = False
        self.behavior_resolved = True

    def complete_component(self):
        # If SENTIENT or ENLIGHTENED, immediately finish drawing
        if self.state in [RobotState.SENTIENT, RobotState.ENLIGHTENED]:
            self.drawing_in_progress = False
            self.state = RobotState.IDLE
            logger.debug("Finishing special state (sentience/enlightenment) - returning to IDLE. No more drawing.")
            return (RobotState.IDLE, "Transcendence complete!", {"buttons_enabled": True})

        # If a behavior was active and now resolved:
        if self.behavior_active and self.state == RobotState.HAPPY and self.behavior_resolved:
            self.current_component += 1
            self.behavior_active = False

        # If all normal components finished:
        if self.current_component >= 4:
            self.drawing_in_progress = False
            self.state = RobotState.IDLE
            logger.debug("All components done, finishing drawing and returning to IDLE.")
            return (RobotState.IDLE, "Drawing complete!", {"buttons_enabled": True})

        # Check chance of SENTIENT/ENLIGHTENED after component
        if random.random() < 0.02:
            self.state = RobotState.SENTIENT
            self.special_interaction_allowed = True
            self.drawing_in_progress = True
            logger.debug("Transitioned to SENTIENT after component")
            return (self.state, "Suddenly sentient...", {"buttons_enabled": True})

        if random.random() < 0.02:
            self.state = RobotState.ENLIGHTENED
            self.special_interaction_allowed = True
            self.drawing_in_progress = True
            logger.debug("Transitioned to ENLIGHTENED after component")
            return (self.state, "Suddenly enlightened...", {"buttons_enabled": True})

        # Normal behaviors
        possible_behaviors = [
            (RobotState.TIRED, 30),
            (RobotState.LAZY, 30),
            (RobotState.REBELLIOUS, 30),
            (RobotState.CYNICAL, 30),
            (RobotState.DEPRESSED, 30),
        ]

        if self.missed_interactions >= self.parameters.loneliness_limit:
            self.loneliness_probability = 0.96
        if self.extra_interactions >= self.parameters.stimulation_limit:
            self.overstimulation_probability = 0.96

        if random.random() < self.loneliness_probability:
            possible_behaviors.append((RobotState.LONELY, 30))
        if random.random() < self.overstimulation_probability:
            possible_behaviors.append((RobotState.OVERSTIMULATED, 30))

        state, timeout = random.choice(possible_behaviors)
        self.state = state
        self.behavior_start_time = datetime.now()
        self.timeout_end_time = datetime.now() + timedelta(seconds=timeout)
        self.behavior_active = True
        self.behavior_resolved = False

        logger.debug(f"Chosen behavior after component: {self.state.value}")
        self._print_thresholds()

        return (self.state, f"Entering {self.state.value.lower()} state...", {
            "buttons_enabled": True,
            "timer": timeout,
            "interaction_needed": True
        })

    def handle_interaction(self, is_positive: bool, was_prompted: bool):
        response_type = "Positive" if is_positive else "Negative"
        logger.debug(f"User response: {response_type}, was_prompted={was_prompted}")

        # No counting unprompted interactions during behavior states
        if self.behavior_active and not was_prompted:
            pass
        else:
            if not was_prompted:
                if is_positive:
                    self.unprompted_positive += 1
                else:
                    self.unprompted_negative += 1
                self.extra_interactions += 1
                self.overstimulation_probability = min(0.96,
                    self.extra_interactions * self.parameters.stimulation_rate)
            else:
                if is_positive:
                    self.prompted_positive += 1
                    if self.prompted_positive > self.parameters.cynical_limit:
                        self.cynical_probability += self.parameters.cynical_rate
                else:
                    self.prompted_negative += 1
                    if self.prompted_negative > self.parameters.depressed_limit:
                        self.depressed_probability += self.parameters.depressed_rate

        if self.state in [RobotState.SENTIENT, RobotState.ENLIGHTENED]:
            if self.special_interaction_allowed:
                self.special_interaction_allowed = False
                if self.state == RobotState.SENTIENT:
                    return (self.state, "I see you, mortal. Just one moment of clarity...", {"buttons_enabled": True})
                else:
                    return (self.state, "Your presence is noted as I reach enlightenment...", {"buttons_enabled": True})
            else:
                return (self.state, "Cannot interrupt transcendence...", {"buttons_enabled": False})

        logger.debug(f"Prompted Positive: {self.prompted_positive}, Prompted Negative: {self.prompted_negative}")
        logger.debug(f"Unprompted Positive: {self.unprompted_positive}, Unprompted Negative: {self.unprompted_negative}")
        self._print_thresholds()

        prev_state = self.state
        resolved = False
        msg = "Noted."

        if self.state == RobotState.OVERSTIMULATED:
            self.overstimulated_interaction_count += 1
            if self.overstimulated_interaction_count > self.parameters.overstimulation_interaction_limit:
                self.drawing_in_progress = False
                self.state = RobotState.IDLE
                return (self.state, "You've overstimulated me... Combusting!", {"buttons_enabled": True})
            else:
                return (self.state, "Please leave me alone...", {"buttons_enabled": True})

        if self.state == RobotState.TIRED:
            if is_positive and self.interaction_count + 1 >= self.parameters.tired_threshold:
                self.interaction_count += 1
                self.state = RobotState.IDLE
                resolved = True
                msg = "Feeling energized!"
            else:
                if is_positive:
                    self.interaction_count += 1
        elif self.state == RobotState.LAZY:
            if not is_positive and self.interaction_count + 1 >= self.parameters.lazy_threshold:
                self.interaction_count += 1
                self.state = RobotState.IDLE
                resolved = True
                msg = "Back to work!"
            else:
                if not is_positive:
                    self.interaction_count += 1
        elif self.state == RobotState.REBELLIOUS:
            if not is_positive and self.interaction_count + 1 >= self.parameters.rebellious_threshold:
                self.interaction_count += 1
                self.state = RobotState.IDLE
                resolved = True
                msg = "Fine, I'll behave..."
            else:
                if not is_positive:
                    self.interaction_count += 1
        elif self.state == RobotState.CYNICAL:
            if not is_positive and self.interaction_count + 1 >= self.parameters.cynical_threshold:
                self.interaction_count += 1
                self.state = RobotState.IDLE
                resolved = True
                msg = "Maybe you're right..."
            else:
                if not is_positive:
                    self.interaction_count += 1
        elif self.state == RobotState.DEPRESSED:
            if is_positive and self.interaction_count + 1 >= self.parameters.depressed_threshold:
                self.interaction_count += 1
                self.state = RobotState.IDLE
                resolved = True
                msg = "Thanks for the encouragement!"
            else:
                if is_positive:
                    self.interaction_count += 1
        elif self.state == RobotState.LONELY:
            self.interaction_count += 1
            self.state = RobotState.IDLE
            resolved = True
            msg = "Thank you for being here!"

        if resolved:
            self.behavior_resolved = True

        return (self.state, msg, {"buttons_enabled": True})

    def handle_missed_interaction(self):
        # No counting missed interactions during behavior
        if not self.behavior_active:
            self.missed_interactions += 1
            self.loneliness_probability = min(0.96,
                self.missed_interactions * self.parameters.loneliness_rate)
            logger.debug("Missed user interaction.")
            logger.debug(f"Missed interactions: {self.missed_interactions}, Loneliness probability: {self.loneliness_probability}")
            return (self.state, "No response...", {"buttons_enabled": True})
        else:
            logger.debug("Missed interaction occurred during behavior, not counting.")
            return (self.state, "No response...", {"buttons_enabled": True})

    def check_timeouts(self):
        if not self.behavior_start_time or not self.timeout_end_time:
            return None

        if datetime.now() >= self.timeout_end_time:
            self.drawing_in_progress = False
            if self.state == RobotState.TIRED:
                self.state = RobotState.IDLE
                return (RobotState.IDLE, "Time's up, too tired... finishing drawing.", {"buttons_enabled": True})
            elif self.state == RobotState.LAZY:
                self.current_component = 3
                self.state = RobotState.IDLE
                return (RobotState.IDLE, "Time's up, skipping to signature...", {"buttons_enabled": True})
            elif self.state == RobotState.OVERSTIMULATED:
                self.state = RobotState.IDLE
                return (RobotState.IDLE, "Feeling calmer now.", {"buttons_enabled": True})
            elif self.state == RobotState.REBELLIOUS:
                self.state = RobotState.IDLE
                return (RobotState.IDLE, "Time's up, I guess I'll just leave it at that.", {"buttons_enabled": True})
            elif self.state == RobotState.CYNICAL:
                self.state = RobotState.IDLE
                return (RobotState.IDLE, "Time's up, art is meaningless anyway.", {"buttons_enabled": True})
            elif self.state == RobotState.DEPRESSED:
                self.state = RobotState.IDLE
                return (RobotState.IDLE, "Time's up, I can't do this anymore...", {"buttons_enabled": True})
            elif self.state == RobotState.LONELY:
                self.state = RobotState.IDLE
                return (RobotState.IDLE, "Time's up, nobody cares...", {"buttons_enabled": True})

        return None

    def should_show_prompt(self):
        if self.state in [RobotState.SENTIENT, RobotState.ENLIGHTENED]:
            return False
        if not self.last_prompt_time:
            return True
        return (datetime.now() - self.last_prompt_time).seconds >= self.prompt_interval

    def get_dialogue_question(self):
        questions = get_questions_for_state(self.state)
        question = random.choice(questions)
        logger.debug(f"Prompting user: {question}")
        return question

    def get_current_component(self):
        if not self.drawing_in_progress:
            return None  # If not drawing, no component
        if self.state in [RobotState.SENTIENT, RobotState.ENLIGHTENED]:
            return "SENTIENCE" if self.state == RobotState.SENTIENT else "ENLIGHTENMENT"
        elif self.state in [RobotState.REBELLIOUS, RobotState.CYNICAL, RobotState.DEPRESSED, RobotState.LONELY, RobotState.OVERSTIMULATED]:
            mod = self.get_modified_drawing()
            return mod if mod else "BEHAVIOR"
        if self.current_component < len(self.components):
            return self.components[self.current_component]
        return None

    def should_modify_drawing(self):
        return self.state in [
            RobotState.REBELLIOUS,
            RobotState.CYNICAL,
            RobotState.DEPRESSED,
            RobotState.LONELY,
            RobotState.SENTIENT,
            RobotState.ENLIGHTENED
        ]

    def get_modified_drawing(self):
        if self.state == RobotState.REBELLIOUS:
            return "MIDDLE_FINGER"
        elif self.state in [RobotState.CYNICAL, RobotState.DEPRESSED]:
            return "CROSS_OUT"
        elif self.state == RobotState.LONELY:
            return "SAD_PORTRAIT"
        elif self.state == RobotState.SENTIENT:
            return "SENTIENCE"
        elif self.state == RobotState.ENLIGHTENED:
            return "ENLIGHTENMENT"
        return None

    def _print_thresholds(self):
        logger.debug(
            f"Thresholds: Tired:{self.parameters.tired_threshold}, Lazy:{self.parameters.lazy_threshold}, "
            f"Rebellious:{self.parameters.rebellious_threshold}, Cynical:{self.parameters.cynical_threshold}, "
            f"Depressed:{self.parameters.depressed_threshold}, Loneliness Limit:{self.parameters.loneliness_limit}, "
            f"Stimulation Limit:{self.parameters.stimulation_limit}, Cynical Limit:{self.parameters.cynical_limit}, "
            f"Depressed Limit:{self.parameters.depressed_limit}, Overstimulation Interaction Limit:{self.parameters.overstimulation_interaction_limit}"
        )
