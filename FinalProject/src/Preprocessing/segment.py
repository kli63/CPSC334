from PIL import Image
from pathlib import Path
import sys
import os

PROJECT_ROOT = Path(__file__).parent.parent.parent
IMAGE_DIR = PROJECT_ROOT / "assets" / "images" / "raw"
OUTPUT_DIR = PROJECT_ROOT / "assets" / "images" / "cropped"

def segment_image(image_path, rows, cols, name_prefix):
    img = Image.open(image_path)
    width, height = img.size
    
    segment_width = width // cols
    segment_height = height // rows
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    count = 0
    for i in range(rows):
        for j in range(cols):
            left = j * segment_width
            upper = i * segment_height
            right = left + segment_width
            lower = upper + segment_height
            
            box = (left, upper, right, lower)
            segment = img.crop(box)
            
            output_path = OUTPUT_DIR / f"{name_prefix}_{count}.png"
            segment.save(output_path)
            count += 1

def main():
    image_files = list(IMAGE_DIR.glob("*"))
    if not image_files:
        print(f"No images found in {IMAGE_DIR}")
        sys.exit(1)
        
    print("Available images:")
    for i, file in enumerate(image_files):
        print(f"{i}: {file.name}")
    
    choice = int(input("Enter the number of the image you want to segment: "))
    if choice < 0 or choice >= len(image_files):
        print("Invalid choice")
        sys.exit(1)
        
    selected_image = image_files[choice]
    
    name_prefix = input("Enter the prefix for segment names: ")
    rows = int(input("Enter number of rows: "))
    cols = int(input("Enter number of columns: "))
    
    if rows <= 0 or cols <= 0:
        print("Rows and columns must be positive numbers")
        sys.exit(1)
        
    try:
        segment_image(selected_image, rows, cols, name_prefix)
        print(f"Segmentation complete. Segments saved in {OUTPUT_DIR}")
    except Exception as e:
        print(f"Error during segmentation: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()