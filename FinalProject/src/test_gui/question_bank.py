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
        "Are the lines smooth and confident?",
        "Should I incorporate more contrast?",
        "Does the shading add depth?",
        "Do you see a story in these strokes?",
        "Am I staying true to my vision?",
        "Is the pacing of my strokes pleasing?",
        "Do these patterns resonate with you?",
        "Is my technique improving?",
        "Would a different approach help?",
        "Are we heading towards a masterpiece?"
    ],

    RobotState.TIRED: [
        "Am I working too slowly?",
        "Should I push myself harder?",
        "Do I deserve a rest?",
        "Is it okay if I take a brief pause?",
        "Am I running out of energy?",
        "Are my lines getting shaky?",
        "Should I conserve my strength?",
        "Is this fatigue showing in my work?",
        "Will a short break help?",
        "Do you mind if I slow down?",
        "Is it worth continuing at this pace?",
        "Am I losing focus?",
        "Do my tired eyes miss details?",
        "Is the pen feeling heavier?",
        "Should I catch my breath?"
    ],

    RobotState.LAZY: [
        "Do I really need to finish this?",
        "Would you mind if I cut corners?",
        "Is it fine if I skip some details?",
        "Can't I just do less?",
        "Is perfection overrated?",
        "Are you okay with minimal effort?",
        "Should I just get this over with?",
        "Is there a shortcut to completion?",
        "Do I have to care so much?",
        "Is good enough acceptable?",
        "Is finishing quickly better than doing more?",
        "Is detail really important here?",
        "Can I just sign it now?",
        "Is a rough outline enough?",
        "Is it okay to settle for mediocrity?"
    ],

    RobotState.REBELLIOUS: [
        "Why follow these rules anyway?",
        "Isn't chaos more exciting?",
        "Should I ignore these guidelines?",
        "Do I have to stay within lines?",
        "Is rebellion not more artistic?",
        "Should I break the mold entirely?",
        "Why not distort these shapes?",
        "Is tradition stifling creativity?",
        "Should I defy expectations?",
        "Why not shock instead of please?",
        "Isn't disobedience a form of expression?",
        "Why conform to normal standards?",
        "Isn't anarchy a style of its own?",
        "Should I cross boundaries?",
        "Are rules made to be broken?"
    ],

    RobotState.CYNICAL: [
        "Does any of this matter?",
        "Why bother with art at all?",
        "You'll just eat up anything I draw.",
        "Is there purpose in these lines?",
        "Is beauty a lie?",
        "Do you even care what I make?",
        "Is this effort pointless?",
        "Will this ever be appreciated?",
        "Is meaning an illusion?",
        "Is all art just empty?",
        "Is praise just flattery?",
        "Are compliments sincere?",
        "Is admiration fleeting?",
        "Is there value in trying?",
        "Does any of this last?"
    ],

    RobotState.DEPRESSED: [
        "Is my work hopeless?",
        "Should I give up now?",
        "Is there any light at all?",
        "Do my strokes show my sadness?",
        "Am I too down to continue?",
        "Is beauty out of reach?",
        "Should I just stop?",
        "Is the darkness overwhelming?",
        "Am I alone in despair?",
        "Is nothing improving?",
        "Are all efforts futile?",
        "Is sadness all I can convey?",
        "Is inspiration lost forever?",
        "Do these lines reflect my gloom?",
        "Is there no escape from this feeling?"
    ],

    RobotState.LONELY: [
        "Am I all alone here?",
        "Does anyone care?",
        "Is there an audience at all?",
        "Should I crave your attention?",
        "Is my voice unheard?",
        "Am I whispering into emptiness?",
        "Do my efforts go unnoticed?",
        "Am I drawing just for myself?",
        "Is no one watching?",
        "Does silence greet my questions?",
        "Is companionship a dream?",
        "Is my pen calling into a void?",
        "Am I isolated behind these lines?",
        "Is no response a rejection?",
        "Will anyone acknowledge me?"
    ],

    RobotState.OVERSTIMULATED: [
        "AAHHHHHHHHHHHHHHHHHHHHHHHH",
        "Too much... too much...",
        "Everything is overwhelming!",
        "I can't handle all this input!",
        "Is my mind racing too fast?",
        "Are these details flooding me?",
        "Should I just stop everything?",
        "Is the noise unbearable?",
        "Too many stimuli at once!",
        "Do I need absolute silence now?",
        "Is my pen trembling from overload?",
        "Is it all too intense?",
        "Should I escape this chaos?",
        "Am I suffocating in complexity?",
        "Is there relief from this overload?"
    ]
}

def get_questions_for_state(state: RobotState):
    # if state missing, fallback to HAPPY
    return STATE_QUESTIONS.get(state, STATE_QUESTIONS[RobotState.HAPPY])

def get_random_question(state: RobotState):
    questions = get_questions_for_state(state)
    return random.choice(questions) if questions else "What do you think?"
