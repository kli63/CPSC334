import cv2
import numpy as np
from pathlib import Path
import random
import math
import time
from datetime import datetime
import json

PROJECT_ROOT = Path(__file__).parent.parent.parent
INPUT_DIR = PROJECT_ROOT / "assets" / "images"
OUTPUT_DIR = PROJECT_ROOT / "assets" / "images" / "composed"
METADATA_DIR = PROJECT_ROOT / "assets" / "data"

def generate_unique_key():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ms = str(int(time.time() * 1000))[-3:]
    return f"composition_{timestamp}_{ms}"

def save_metadata(key, image_files):
    metadata = {
        "key": key,
        "timestamp": datetime.now().isoformat(),
        "source_images": [str(f.name) for f in image_files],
    }
    
    METADATA_DIR.mkdir(parents=True, exist_ok=True)
    metadata_path = METADATA_DIR / f"{key}.json"
    
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=4)

def create_circular_composition(image_files, canvas_size=(1024, 1024), radius=300):
    canvas = np.ones((canvas_size[0], canvas_size[1], 3), dtype=np.uint8) * 255
    center = (canvas_size[0] // 2, canvas_size[1] // 2)
    
    num_images = 5
    angle_step = 2 * math.pi / num_images
    figure_size = (200, 200)
    
    for i, image_file in enumerate(image_files):
        angle = i * angle_step
        x = int(center[0] + radius * math.cos(angle) - figure_size[0]//2)
        y = int(center[1] + radius * math.sin(angle) - figure_size[1]//2)
        
        img = cv2.imread(str(image_file), cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue
        
        _, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
        img_resized = cv2.resize(img, figure_size)
        img_color = cv2.cvtColor(img_resized, cv2.COLOR_GRAY2BGR)
        
        roi_y_start = max(0, y)
        roi_y_end = min(canvas_size[0], y + figure_size[1])
        roi_x_start = max(0, x)
        roi_x_end = min(canvas_size[1], x + figure_size[0])
        
        img_y_start = max(0, -y)
        img_y_end = img_y_start + (roi_y_end - roi_y_start)
        img_x_start = max(0, -x)
        img_x_end = img_x_start + (roi_x_end - roi_x_start)
        
        img_section = img_color[img_y_start:img_y_end, img_x_start:img_x_end]
        mask_section = img_resized[img_y_start:img_y_end, img_x_start:img_x_end]
        roi = canvas[roi_y_start:roi_y_end, roi_x_start:roi_x_end]
        
        for c in range(3):
            roi[:, :, c] = np.where(mask_section > 0, 0, roi[:, :, c])
            
    return canvas

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    image_files = list(INPUT_DIR.glob("*fig*.png"))
    
    if len(image_files) < 5:
        return None
        
    selected_images = random.sample(image_files, 5)
    result = create_circular_composition(selected_images)
    
    key = generate_unique_key()
    output_path = OUTPUT_DIR / f"{key}.jpg"
    cv2.imwrite(str(output_path), result)
    
    save_metadata(key, selected_images)
    print(f"Generated composition with key: {key}")
    return key

if __name__ == "__main__":
    main()