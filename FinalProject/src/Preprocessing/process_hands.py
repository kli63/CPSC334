import cv2
import os
import numpy as np

# Directories
INPUT_DIR = "../../assets/images/raw"
OUTPUT_DIR = "../../assets/images/behaviors"

def process_image_to_stick_figure(input_path, output_path):
    # Load the image
    image = cv2.imread(input_path)
    if image is None:
        print(f"Error: Could not load image {input_path}")
        return
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Perform edge detection using Canny
    edges = cv2.Canny(blurred, threshold1=50, threshold2=150)
    
    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Create a white canvas for stick figure
    stick_figure = np.ones_like(gray) * 255  # Initialize with white background
    
    # Draw approximated contours on the canvas
    for contour in contours:
        # Approximate contour to reduce the number of points
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        # Draw contours in black
        cv2.drawContours(stick_figure, [approx], -1, 0, 2)
    
    # Save the result
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, stick_figure)
    print(f"Processed image saved to {output_path}")

def main():
    # Define the raw image filenames
    input_files = ["badhand.png", "goodhand.jpg"]
    
    for file_name in input_files:
        input_path = os.path.join(INPUT_DIR, file_name)
        output_path = os.path.join(OUTPUT_DIR, f"stick_figure_{file_name}")
        process_image_to_stick_figure(input_path, output_path)

if __name__ == "__main__":
    main()
