import os
from PIL import Image, ImageDraw
import shutil

class ImageComponentizer:
    def __init__(self):
        # Define constants
        self.INPUT_DIR = "../../assets/images/cropped"
        self.OUTPUT_BASE_DIR = "../../assets/images/components"
        self.FINAL_SIZE = 1024  # Total canvas size
        self.QUADRANT_SIZE = self.FINAL_SIZE // 2  # Size of each quadrant
        self.BOX_SIZE = 400  # Size of the square box in each quadrant
        self.BOX_MARGIN = (self.QUADRANT_SIZE - self.BOX_SIZE) // 2  # Margin to center box in quadrant
        
        # Define quadrant positions with centered boxes
        self.QUADRANTS = {
            'q1': (self.BOX_MARGIN, self.BOX_MARGIN),  # top-left
            'q2': (self.QUADRANT_SIZE + self.BOX_MARGIN, self.BOX_MARGIN),  # top-right
            'q3': (self.BOX_MARGIN, self.QUADRANT_SIZE + self.BOX_MARGIN),  # bottom-left
            'q4': (self.QUADRANT_SIZE + self.BOX_MARGIN, self.QUADRANT_SIZE + self.BOX_MARGIN)  # bottom-right
        }

    def setup_directories(self):
        """Create output directories for each quadrant if they don't exist."""
        if os.path.exists(self.OUTPUT_BASE_DIR):
            shutil.rmtree(self.OUTPUT_BASE_DIR)
        
        for quadrant in self.QUADRANTS.keys():
            os.makedirs(os.path.join(self.OUTPUT_BASE_DIR, quadrant), exist_ok=True)

    def draw_boxes(self, draw):
        """Draw boxes in all quadrants"""
        LINE_WIDTH = 5  # Width of the box lines
        
        for x, y in self.QUADRANTS.values():
            # Draw a square box
            draw.rectangle(
                [
                    (x, y),  # Top-left corner
                    (x + self.BOX_SIZE, y + self.BOX_SIZE)  # Bottom-right corner
                ],
                outline='black',
                width=LINE_WIDTH
            )

    def process_image_for_quadrant(self, image_path, quadrant):
        """Process a single image for a specific quadrant."""
        with Image.open(image_path) as img:
            img = img.convert('RGBA')
            
            # Create a white canvas
            canvas = Image.new('RGB', (self.FINAL_SIZE, self.FINAL_SIZE), 'WHITE')
            draw = ImageDraw.Draw(canvas)
            
            # Draw all boxes first
            self.draw_boxes(draw)
            
            # Calculate the size to fit inside the box (leaving some margin for the box border)
            BOX_PADDING = 20  # Padding inside the box
            MAX_IMAGE_SIZE = self.BOX_SIZE - (BOX_PADDING * 2)
            
            # Resize image to fit inside box while maintaining aspect ratio
            img_size = img.size
            ratio = min(MAX_IMAGE_SIZE / img_size[0], MAX_IMAGE_SIZE / img_size[1])
            new_size = (int(img_size[0] * ratio), int(img_size[1] * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            # Calculate position to center the image within its box
            quadrant_x, quadrant_y = self.QUADRANTS[quadrant]
            x_offset = quadrant_x + (self.BOX_SIZE - new_size[0]) // 2
            y_offset = quadrant_y + (self.BOX_SIZE - new_size[1]) // 2
            
            # Create temporary white background for this component
            temp_bg = Image.new('RGB', new_size, 'WHITE')
            temp_bg.paste(img, (0, 0), img)
            
            # Paste the image with white background onto the main canvas
            canvas.paste(temp_bg, (x_offset, y_offset))
            
            # Save the result
            output_filename = f"{os.path.splitext(os.path.basename(image_path))[0]}_{quadrant}.png"
            output_path = os.path.join(self.OUTPUT_BASE_DIR, quadrant, output_filename)
            canvas.save(output_path)
            
            return output_path

    def process_all_images(self):
        """Process all images in the input directory for all quadrants."""
        self.setup_directories()
        
        images = [f for f in os.listdir(self.INPUT_DIR) 
                 if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        
        if not images:
            print(f"No images found in {self.INPUT_DIR}")
            return
        
        for image in images:
            image_path = os.path.join(self.INPUT_DIR, image)
            print(f"Processing {image}...")
            
            for quadrant in self.QUADRANTS.keys():
                output_path = self.process_image_for_quadrant(image_path, quadrant)
                print(f"  Created {output_path}")

def main():
    if not os.path.exists("../../assets/images/cropped"):
        print("Error: Input directory '../../assets/images/cropped' does not exist!")
        return
        
    componentizer = ImageComponentizer()
    componentizer.process_all_images()
    print("Processing complete!")

if __name__ == "__main__":
    main()