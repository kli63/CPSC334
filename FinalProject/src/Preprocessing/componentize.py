import os
from PIL import Image
import shutil

class ImageComponentizer:
    def __init__(self):
        # Define constants - updated with correct relative paths
        self.INPUT_DIR = "../../assets/images/cropped"
        self.OUTPUT_BASE_DIR = "../../assets/images/components"
        self.FINAL_SIZE = 1024  # Total canvas size
        self.QUADRANT_SIZE = self.FINAL_SIZE // 2  # Size of each quadrant
        
        # Define quadrant positions (top-left corner of each quadrant)
        self.QUADRANTS = {
            'q1': (0, 0),                                    # top-left
            'q2': (self.QUADRANT_SIZE, 0),                  # top-right
            'q3': (0, self.QUADRANT_SIZE),                  # bottom-left
            'q4': (self.QUADRANT_SIZE, self.QUADRANT_SIZE)  # bottom-right
        }

    def setup_directories(self):
        """Create output directories for each quadrant if they don't exist."""
        # Remove existing output directory if it exists
        if os.path.exists(self.OUTPUT_BASE_DIR):
            shutil.rmtree(self.OUTPUT_BASE_DIR)
        
        # Create directories for each quadrant
        for quadrant in self.QUADRANTS.keys():
            os.makedirs(os.path.join(self.OUTPUT_BASE_DIR, quadrant), exist_ok=True)

    def process_image_for_quadrant(self, image_path, quadrant):
        """Process a single image for a specific quadrant."""
        # Load and convert image to RGBA
        with Image.open(image_path) as img:
            img = img.convert('RGBA')
            
            # Create a blank canvas of the final size
            canvas = Image.new('RGBA', (self.FINAL_SIZE, self.FINAL_SIZE), (255, 255, 255, 0))
            
            # Resize image to fit quadrant while maintaining aspect ratio
            aspect_ratio = img.width / img.height
            if aspect_ratio > 1:
                new_width = self.QUADRANT_SIZE
                new_height = int(self.QUADRANT_SIZE / aspect_ratio)
            else:
                new_height = self.QUADRANT_SIZE
                new_width = int(self.QUADRANT_SIZE * aspect_ratio)
            
            # Resize image
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Calculate position to center the image within its quadrant
            quadrant_x, quadrant_y = self.QUADRANTS[quadrant]
            x_offset = quadrant_x + (self.QUADRANT_SIZE - new_width) // 2
            y_offset = quadrant_y + (self.QUADRANT_SIZE - new_height) // 2
            
            # Paste the image onto the canvas at the calculated position
            canvas.paste(img, (x_offset, y_offset), img)
            
            # Save the result
            output_filename = f"{os.path.splitext(os.path.basename(image_path))[0]}_{quadrant}.png"
            output_path = os.path.join(self.OUTPUT_BASE_DIR, quadrant, output_filename)
            canvas.save(output_path)
            
            return output_path

    def process_all_images(self):
        """Process all images in the input directory for all quadrants."""
        self.setup_directories()
        
        # Get list of all images in input directory
        images = [f for f in os.listdir(self.INPUT_DIR) 
                 if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        
        if not images:
            print(f"No images found in {self.INPUT_DIR}")
            return
        
        # Process each image for each quadrant
        for image in images:
            image_path = os.path.join(self.INPUT_DIR, image)
            print(f"Processing {image}...")
            
            for quadrant in self.QUADRANTS.keys():
                output_path = self.process_image_for_quadrant(image_path, quadrant)
                print(f"  Created {output_path}")

def main():
    # Check if input directory exists
    if not os.path.exists("../../assets/images/cropped"):
        print("Error: Input directory '../../assets/images/cropped' does not exist!")
        return
        
    componentizer = ImageComponentizer()
    componentizer.process_all_images()
    print("Processing complete!")

if __name__ == "__main__":
    main()