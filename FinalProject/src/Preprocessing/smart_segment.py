import cv2
import numpy as np
from pathlib import Path
import sys
from PIL import Image

PROJECT_ROOT = Path(__file__).parent.parent.parent
IMAGE_DIR = PROJECT_ROOT / "assets" / "images" / "raw"
OUTPUT_DIR = PROJECT_ROOT / "assets" / "images"

def detect_stick_figures(image_path, target_size=(256, 256)):
    img = cv2.imread(str(image_path))
    if img is None:
        raise ValueError(f"Could not load image: {image_path}")
        
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    
    kernel = np.ones((5,5), np.uint8)
    dilated = cv2.dilate(edges, kernel, iterations=2)
    
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    segments = []
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        
        if w * h > 100:
            roi = img[y:y+h, x:x+w]
            pil_roi = Image.fromarray(cv2.cvtColor(roi, cv2.COLOR_BGR2RGB))
            resized_roi = pil_roi.resize(target_size, Image.Resampling.LANCZOS)
            segments.append(resized_roi)
    
    return segments

def process_image(filename):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    image_path = IMAGE_DIR / filename
    if not image_path.exists():
        print(f"Error: Image {filename} not found in {IMAGE_DIR}")
        return
        
    try:
        segments = detect_stick_figures(image_path)
        
        for i, segment in enumerate(segments):
            output_path = OUTPUT_DIR / "cropped" / f"{image_path.stem}_fig_{i}.png"
            segment.save(output_path)
            
        print(f"Processed {filename}: found {len(segments)} figures")
        print(f"Segments saved to {OUTPUT_DIR}")
            
    except Exception as e:
        print(f"Error processing {filename}: {str(e)}")

def main():
    print(f"Available images in {IMAGE_DIR}:")
    images = list(IMAGE_DIR.glob("*"))
    if not images:
        print("No images found")
        sys.exit(1)
        
    for i, img in enumerate(images):
        print(f"{i + 1}. {img.name}")
    
    choice = input("\nEnter the image filename (e.g., sticks.jpg): ")
    process_image(choice)

if __name__ == "__main__":
    main()