# question_bank.py
import random
from enums import RobotState

STATE_QUESTIONS = {
    RobotState.HAPPY: [
        "How am I doing?",
        "Do you like what I'm drawing?",
        "Is my art making you happy?",
        "Should I try something different?",
        "Am I meeting your expectations?",
        "Is this style appealing to you?",
        "Do these lines speak to you?",
        "Am I capturing the right mood?",
        "Is the composition balanced?",
        "Do you find these shapes interesting?",
        "Should I add more details?",
        "Do you think others would enjoy this?",
        "Do the proportions feel right?",
        "Am I being too cautious?",
        "Is there enough variety here?",
        "Do you see any room for improvement?",
        "Am I too repetitive?",
        "Is the theme clear?",
        "Do you appreciate my effort?",
        "Is this evolving as you'd hoped?",
    ],
    RobotState.TIRED: [
        "Am I working too slowly?",
        "Should I push myself harder?",
        "Do I deserve a rest?",
        # add more...
    ],
    RobotState.LAZY: [
        "Do I really need to finish this?",
        "Would you mind if I cut corners?",
        # add more...
    ],
    RobotState.REBELLIOUS: [
        "Why follow these rules anyway?",
        "Isn't chaos more exciting?",
        # add more...
    ],
    RobotState.CYNICAL: [
        "Does any of this matter?",
        "Why bother with art at all?",
        "You'll just eat up anything",
        # add more...
    ],
    RobotState.DEPRESSED: [
        "Is my work hopeless?",
        "Should I give up now?",
        # add more...
    ],
    RobotState.LONELY: [
        "Am I all alone here?",
        "Does anyone care?",
        # add more...
    ],
    RobotState.OVERSTIMULATED: [
        "AAHHHHHHHHHHHHHHHHHHHHHHHH",
        "Too much...",
        # add more...
    ]
}

def get_questions_for_state(state: RobotState):
    # if state missing, fallback to HAPPY
    return STATE_QUESTIONS.get(state, STATE_QUESTIONS[RobotState.HAPPY])

def get_random_question(state: RobotState):
    questions = get_questions_for_state(state)
    return random.choice(questions) if questions else "What do you think?"
