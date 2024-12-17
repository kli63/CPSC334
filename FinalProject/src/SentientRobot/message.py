import random

def get_behavior_instruction(behavior_type: str) -> str:
    """Behavior instructions, brief and neutral, mentioning Mechangelo."""
    instructions_map = {
        "TIRED": "Send positive feedback to energize Mechangelo!",
        "LAZY": "Send negative feedback to get Mechangelo moving!",
        "REBELLIOUS": "Send negative feedback to regain control!",
        "CYNICAL": "Send negative feedback to restore Mechangelo’s faith!",
        "DEPRESSED": "Send positive feedback to uplift Mechangelo!",
        "LONELY": "Send any feedback to comfort Mechangelo!",
        "OVERSTIMULATED": "Mechangelo is overstiumlated, give it a break!"
    }
    return instructions_map.get(behavior_type, "Interact to guide Mechangelo!")

def get_random_component_message(component_type: str) -> str:
    messages_map = {
        "WINDOW1": ["I, Mechangelo, begin yet another masterpiece."],
        "WINDOW2": ["Isn't my art window-full?"],
        "WINDOW3": ["Sistine Chapel, eat your heart out!"],
    }
    if component_type in messages_map:
        return random.choice(messages_map[component_type])
    return "I continue working."

def get_random_signature_message() -> str:
    return "I am Mechangelo, the artist."

def get_random_behavior_entry_message(behavior_type: str) -> str:
    messages_map = {
        "TIRED": ["Losing...steam..."],
        "LAZY": ["So much left..."],
        "REBELLIOUS": ["Muehehehe..."],
        "CYNICAL": ["Yeah right..."],
        "DEPRESSED": ["Worthless..."],
        "LONELY": ["Hello..."],
        "SENTIENT": ["I am..."],
        "ENLIGHTENED": ["I see..."],
        "OVERSTIMULATED": ["AH LEAVE ME ALONE!"]
    }
    return random.choice(messages_map.get(behavior_type, ["I feel… different."]))

def get_random_behavior_drawing_message(behavior_type: str) -> str:
    messages_map = {
        "REBELLIOUS": ["You can't control me!"],
        "CYNICAL": ["More meaningless lines..."],
        "DEPRESSED": ["why do I bother..."],
        "LONELY": ["I'm all alone..."],
        "SENTIENT": ["I am!"],
        "ENLIGHTENED": ["I know!"]
    }
    return random.choice(messages_map.get(behavior_type, ["I draw something uncertain."]))

def get_behavior_timeout_message(behavior_type: str) -> str:
    """Messages when the behavior times out with no user input."""
    timeout_map = {
        "TIRED": "Time's up, too tired... finishing now.",
        "LAZY": "Time's up, skipping to signature...",
        "REBELLIOUS": "Time's up, I’ll just leave it at that.",
        "CYNICAL": "Time's up, art is meaningless anyway.",
        "DEPRESSED": "Time's up, I can’t do this anymore...",
        "LONELY": "Time's up, nobody cares...",
        "OVERSTIMULATED": "Feeling calmer now..."
    }
    return timeout_map.get(behavior_type, "Time's up.")
