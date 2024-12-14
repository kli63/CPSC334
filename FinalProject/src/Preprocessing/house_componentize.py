import os
from PIL import Image, ImageDraw
import shutil

class ImageComponentizer:
    def __init__(self):
       # Define constants
        self.INPUT_DIR = "../../assets/images/cropped"
        self.OUTPUT_BASE_DIR = "../../assets/images/components"
        self.FINAL_SIZE = 2000  # Bigger canvas
        self.LINE_WIDTH = 3
        
        # House proportions - MUCH lower and bigger
        self.HOUSE_BASE_Y = 700  # Move house way down
        self.HOUSE_WIDTH = 1800
        self.HOUSE_HEIGHT = 1200
        self.ROOF_HEIGHT = 400
        
        # Window sizes
        self.WINDOW_SIZE = 600
        self.LONG_WINDOW_WIDTH = 800
        self.LONG_WINDOW_HEIGHT = 400
        
        # Door and doorknob - shorter to avoid intersection
        self.DOOR_WIDTH = 350
        self.DOOR_HEIGHT = 500  # Shortened to avoid intersection
        self.DOORKNOB_RADIUS = 15
        
        # Chimney - taller
        self.CHIMNEY_WIDTH = 100
        self.CHIMNEY_HEIGHT = 200  # Taller chimney

    def draw_house(self, draw):
        """Draw the house frame with windows."""
        # Calculate positions
        house_left = (self.FINAL_SIZE - self.HOUSE_WIDTH) // 2
        house_right = house_left + self.HOUSE_WIDTH
        house_bottom = self.HOUSE_BASE_Y + self.HOUSE_HEIGHT
        
        # Draw main house rectangle
        draw.rectangle(
            [(house_left, self.HOUSE_BASE_Y), (house_right, house_bottom)],
            outline='black',
            width=self.LINE_WIDTH
        )
        
        # Calculate roof points
        roof_peak = self.HOUSE_BASE_Y - self.ROOF_HEIGHT
        roof_mid_x = house_left + self.HOUSE_WIDTH//2
        
        # Draw roof (triangle)
        draw.line(
            [(house_left, self.HOUSE_BASE_Y), 
             (roof_mid_x, roof_peak),
             (house_right, self.HOUSE_BASE_Y)],
            fill='black',
            width=self.LINE_WIDTH
        )
        
        # Draw chimney with proper roof intersection
        chimney_x = house_right - self.HOUSE_WIDTH//4
        roof_slope = (self.HOUSE_BASE_Y - roof_peak) / (house_right - roof_mid_x)
        chimney_y = roof_peak + (chimney_x - roof_mid_x) * roof_slope

        # Draw chimney vertical lines ensuring they connect to roof slope
        draw.line(
            [(chimney_x, chimney_y - self.CHIMNEY_HEIGHT), (chimney_x, chimney_y)],
            fill='black',
            width=self.LINE_WIDTH
        )

        # Calculate exact intersection point for right chimney line
        chimney_right_x = chimney_x + self.CHIMNEY_WIDTH
        chimney_right_y = roof_peak + (chimney_right_x - roof_mid_x) * roof_slope

        draw.line(
            [(chimney_right_x, chimney_y - self.CHIMNEY_HEIGHT), 
            (chimney_right_x, chimney_right_y)],
            fill='black',
            width=self.LINE_WIDTH
        )

        # Top of chimney
        draw.line(
            [(chimney_x, chimney_y - self.CHIMNEY_HEIGHT),
            (chimney_right_x, chimney_y - self.CHIMNEY_HEIGHT)],
            fill='black',
            width=self.LINE_WIDTH
        )
        
        # Calculate window positions with adjusted layout
        window_margin = (self.HOUSE_WIDTH - (2 * self.WINDOW_SIZE)) // 3
        top_window_y = self.HOUSE_BASE_Y + 30  # Higher up
        
        # Door aligned with top of first floor window
        first_floor_window_y = top_window_y + self.WINDOW_SIZE + 100  # Lower the first floor window
        door_x = house_left + window_margin
        door_y = house_bottom - self.DOOR_HEIGHT
        
        # Draw door
        draw.rectangle(
            [(door_x, door_y), (door_x + self.DOOR_WIDTH, house_bottom)],
            outline='black',
            width=self.LINE_WIDTH
        )
        
        # Draw doorknob
        knob_x = door_x + self.DOOR_WIDTH - 50
        knob_y = door_y + self.DOOR_HEIGHT // 2
        draw.ellipse(
            [(knob_x - self.DOORKNOB_RADIUS, knob_y - self.DOORKNOB_RADIUS),
             (knob_x + self.DOORKNOB_RADIUS, knob_y + self.DOORKNOB_RADIUS)],
            outline='black',
            width=self.LINE_WIDTH
        )
        
        # Adjust window positions to avoid door
        self.window_positions = {
            'top_left': (house_left + window_margin, top_window_y),
            'top_right': (house_right - window_margin - self.WINDOW_SIZE, top_window_y),
            'middle': (house_right - self.LONG_WINDOW_WIDTH - window_margin,
                      first_floor_window_y)
        }
        
        # Draw top windows
        for pos in ['top_left', 'top_right']:
            x, y = self.window_positions[pos]
            draw.rectangle(
                [(x, y), (x + self.WINDOW_SIZE, y + self.WINDOW_SIZE)],
                outline='black',
                width=self.LINE_WIDTH
            )
        
        # Draw middle long window
        x, y = self.window_positions['middle']
        draw.rectangle(
            [(x, y), (x + self.LONG_WINDOW_WIDTH, y + self.LONG_WINDOW_HEIGHT)],
            outline='black',
            width=self.LINE_WIDTH
        )

    def process_image_for_window(self, image_path, window_position):
        """Process a single image for a specific window."""
        with Image.open(image_path) as img:
            img = img.convert('RGBA')
            
            # Create a white canvas
            canvas = Image.new('RGB', (self.FINAL_SIZE, self.FINAL_SIZE), 'WHITE')
            draw = ImageDraw.Draw(canvas)
            
            # Draw the house first
            self.draw_house(draw)
            
            # Get window position and size
            x, y = self.window_positions[window_position]
            if window_position in ['top_left', 'top_right']:
                window_width = window_height = self.WINDOW_SIZE
            else:
                window_width = self.LONG_WINDOW_WIDTH
                window_height = self.LONG_WINDOW_HEIGHT
            
            # Resize image to fit window while maintaining aspect ratio
            img_width, img_height = img.size
            ratio = min((window_width - 20) / img_width, 
                       (window_height - 20) / img_height)
            new_size = (int(img_width * ratio), int(img_height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            # Center image in window
            x_offset = x + (window_width - new_size[0]) // 2
            y_offset = y + (window_height - new_size[1]) // 2
            
            # Create temporary white background for image
            temp_bg = Image.new('RGB', new_size, 'WHITE')
            temp_bg.paste(img, (0, 0), img)
            
            # Paste the image onto the canvas
            canvas.paste(temp_bg, (x_offset, y_offset))
            
            # Save the result
            output_filename = f"{os.path.splitext(os.path.basename(image_path))[0]}_{window_position}.png"
            output_path = os.path.join(self.OUTPUT_BASE_DIR, window_position, output_filename)
            canvas.save(output_path)
            
            return output_path

    def process_all_images(self):
        self.setup_directories()
        
        images = [f for f in os.listdir(self.INPUT_DIR) 
                 if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        
        if not images:
            print(f"No images found in {self.INPUT_DIR}")
            return
        
        for image in images:
            image_path = os.path.join(self.INPUT_DIR, image)
            print(f"Processing {image}...")
            
            for window in ['top_left', 'top_right', 'middle']:
                output_path = self.process_image_for_window(image_path, window)
                print(f"  Created {output_path}")

    def setup_directories(self):
        if os.path.exists(self.OUTPUT_BASE_DIR):
            shutil.rmtree(self.OUTPUT_BASE_DIR)
        
        for window in ['top_left', 'top_right', 'middle']:
            os.makedirs(os.path.join(self.OUTPUT_BASE_DIR, window), exist_ok=True)

def main():
    if not os.path.exists("../../assets/images/cropped"):
        print("Error: Input directory '../../assets/images/cropped' does not exist!")
        return
        
    componentizer = ImageComponentizer()
    componentizer.process_all_images()
    print("\nProcessing complete!")

if __name__ == "__main__":
    main()