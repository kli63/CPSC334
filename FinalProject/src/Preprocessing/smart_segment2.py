import cv2
import numpy as np
from pathlib import Path
import sys
from PIL import Image

PROJECT_ROOT = Path(__file__).parent.parent.parent
IMAGE_DIR = PROJECT_ROOT / "assets" / "images" / "raw"
OUTPUT_DIR = PROJECT_ROOT / "assets" / "images" / "cropped"

def detect_and_crop(image_path):
    img = cv2.imread(str(image_path))
    if img is None:
        raise ValueError(f"Could not load image: {image_path}")

    # Convert to grayscale and then to binary image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 225, 255, cv2.THRESH_BINARY_INV)

    # Remove thin lines possibly connecting figures
    kernel = np.ones((3, 3), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=1)

    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cropped_images = []
    for contour in contours:
        # Get bounding box for each contour
        x, y, w, h = cv2.boundingRect(contour)
        # Consider contours with a minimum size
        if w > 20 and h > 20:
            cropped_img = img[y:y+h, x:x+w]
            cropped_images.append(cropped_img)

    return cropped_images

def process_image(filename):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    image_path = IMAGE_DIR / filename
    if not image_path.exists():
        print(f"Error: Image {filename} not found in {IMAGE_DIR}")
        return

    try:
        cropped_images = detect_and_crop(image_path)

        for i, cropped_img in enumerate(cropped_images):
            output_path = OUTPUT_DIR / f"{image_path.stem}_{i}.png"
            Image.fromarray(cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB)).save(output_path)

        print(f"Processed {filename}: found {len(cropped_images)} regions")
        print(f"Cropped images saved to {OUTPUT_DIR}")

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
