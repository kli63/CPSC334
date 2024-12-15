# question_bank.py
import random
from enums import RobotState

# Each state maps to its own list of questions.
STATE_QUESTIONS = {
    RobotState.HAPPY: [
        "How am I doing?",
        "Do you like what I'm drawing?",
        "Is my art making you happy?",
        "Should I try something different?",
        "Am I meeting your expectations?"
    ],
    RobotState.TIRED: [
        "Am I working hard enough?", 
        "Should I take a break?"
    ],
    RobotState.LAZY: [
        "Do I really have to finish?", 
        "Can't we just skip to the end?"
    ],
    RobotState.REBELLIOUS: [
        "Why should I follow the rules?", 
        "Isn't breaking rules more fun?"
    ],
    RobotState.CYNICAL: [
        "Why do we even make art?", 
        "Does any of this matter?"
    ],
    RobotState.DEPRESSED: [
        "Is my art really that bad?", 
        "Should I just give up?"
    ],
    RobotState.LONELY: [
        "Is anyone still watching?", 
        "Does anyone care about my art?"
    ],
    RobotState.OVERSTIMULATED: [
        "Is it too much for me to handle?", 
        "Should I just stop?"
    ]
    # SENTIENT and ENLIGHTENED do not prompt user questions
    # If state missing, fallback to HAPPY
}

def get_questions_for_state(state: RobotState):
    return STATE_QUESTIONS.get(state, STATE_QUESTIONS[RobotState.HAPPY])
