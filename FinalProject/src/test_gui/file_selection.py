import os
import random
from datetime import datetime

def create_log_directory(base_path):
    # base_path could be "CPSC334/FinalProject/assets/data/logs"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = os.path.join(base_path, timestamp)
    os.makedirs(log_dir, exist_ok=True)
    return log_dir, timestamp

def select_component_files(assets_base):
    # assets_base could be "CPSC334/FinalProject/assets/data"
    # We'll randomly choose one file from middle/json, top_left/json, top_right/json
    middle_path = os.path.join(assets_base, "middle/json")
    top_left_path = os.path.join(assets_base, "top_left/json")
    top_right_path = os.path.join(assets_base, "top_right/json")
    signature_path = os.path.join(assets_base, "signature/json")

    # Random file from each
    def random_file_from_dir(dir_path):
        files = [f for f in os.listdir(dir_path) if f.endswith(".json")]
        return os.path.join(dir_path, random.choice(files))

    window1_file = random_file_from_dir(middle_path)
    window2_file = random_file_from_dir(top_left_path)
    window3_file = random_file_from_dir(top_right_path)

    # Signature is constant - assume one json or pick the same file if multiple
    # If multiple signatures, do the same random process
    signature_files = [f for f in os.listdir(signature_path) if f.endswith(".json")]
    # If always the same, just choose first file
    signature_file = os.path.join(signature_path, signature_files[0])

    return window1_file, window2_file, window3_file, signature_file

def select_behavior_file(assets_base, state):
    # For behaviors:
    # rebellious -> badhand.json
    # enlightened -> goodhand.json
    # lonely -> sad.json
    # sentient -> painter.json
    # cynical/depressed -> random from [scribble1.json, scribble3.json, scribble4.json]

    behaviors_path = os.path.join(assets_base, "behaviors")

    if state == "REBELLIOUS":
        return os.path.join(behaviors_path, "data/json", "badhand.json")
    elif state == "ENLIGHTENED":
        return os.path.join(behaviors_path, "data/json", "goodhand.json")
    elif state == "LONELY":
        return os.path.join(behaviors_path, "portraits/json", "sad.json")
    elif state == "SENTIENT":
        return os.path.join(behaviors_path, "portraits/json", "painter.json")
    elif state == "CYNICAL" or state == "DEPRESSED":
        scribble_dir = os.path.join(behaviors_path, "scribbles/json")
        scribbles = ["scribble1.json", "scribble3.json", "scribble4.json"]
        chosen = random.choice(scribbles)
        return os.path.join(scribble_dir, chosen)
    else:
        # For TIRED, LAZY, no drawing file needed
        return None
