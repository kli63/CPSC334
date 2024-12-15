import os
from PIL import Image, ImageDraw, ImageFont

class SignatureHouseGenerator:
    def __init__(self):
        # Define constants
        self.FINAL_SIZE = 2000  # Canvas size
        self.LINE_WIDTH = 3
        
        # House proportions
        self.HOUSE_BASE_Y = 700
        self.HOUSE_WIDTH = 1800
        self.HOUSE_HEIGHT = 1200
        self.ROOF_HEIGHT = 400
        
        # Window sizes
        self.WINDOW_SIZE = 600
        self.LONG_WINDOW_WIDTH = 800
        self.LONG_WINDOW_HEIGHT = 400
        
        # Door and doorknob
        self.DOOR_WIDTH = 350
        self.DOOR_HEIGHT = 500
        self.DOORKNOB_RADIUS = 15
        
        # Chimney
        self.CHIMNEY_WIDTH = 100
        self.CHIMNEY_HEIGHT = 200
        
        # Signature box dimensions
        self.SIGNATURE_BOX_WIDTH = 800
        self.SIGNATURE_BOX_HEIGHT = 150
        self.SIGNATURE_TEXT = "Mechalangelo d[o_0]b"
        self.SIGNATURE_FONT_SIZE = 70  # Try a large but reasonable size
        
        # Path to a known TTF font on your system. Adjust as needed:
        # For Linux (often pre-installed):
        self.FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

    def draw_house(self, draw):
        """Draw the house frame with windows and a signature box."""
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
        
        # Draw chimney
        chimney_x = house_right - self.HOUSE_WIDTH//4
        roof_slope = (self.HOUSE_BASE_Y - roof_peak) / (house_right - roof_mid_x)
        chimney_y = roof_peak + (chimney_x - roof_mid_x) * roof_slope
        
        draw.line(
            [(chimney_x, chimney_y - self.CHIMNEY_HEIGHT), (chimney_x, chimney_y)],
            fill='black',
            width=self.LINE_WIDTH
        )

        chimney_right_x = chimney_x + self.CHIMNEY_WIDTH
        chimney_right_y = roof_peak + (chimney_right_x - roof_mid_x) * roof_slope

        draw.line(
            [(chimney_right_x, chimney_y - self.CHIMNEY_HEIGHT), 
             (chimney_right_x, chimney_right_y)],
            fill='black',
            width=self.LINE_WIDTH
        )

        draw.line(
            [(chimney_x, chimney_y - self.CHIMNEY_HEIGHT),
             (chimney_right_x, chimney_y - self.CHIMNEY_HEIGHT)],
            fill='black',
            width=self.LINE_WIDTH
        )
        
        # Door and windows
        window_margin = (self.HOUSE_WIDTH - (2 * self.WINDOW_SIZE)) // 3
        top_window_y = self.HOUSE_BASE_Y + 30
        first_floor_window_y = top_window_y + self.WINDOW_SIZE + 100
        door_x = house_left + window_margin
        door_y = house_bottom - self.DOOR_HEIGHT
        
        draw.rectangle(
            [(door_x, door_y), (door_x + self.DOOR_WIDTH, house_bottom)],
            outline='black',
            width=self.LINE_WIDTH
        )
        
        knob_x = door_x + self.DOOR_WIDTH - 50
        knob_y = door_y + self.DOOR_HEIGHT // 2
        draw.ellipse(
            [(knob_x - self.DOORKNOB_RADIUS, knob_y - self.DOORKNOB_RADIUS),
             (knob_x + self.DOORKNOB_RADIUS, knob_y + self.DOORKNOB_RADIUS)],
            outline='black',
            width=self.LINE_WIDTH
        )

        window_positions = {
            'top_left': (house_left + window_margin, top_window_y),
            'top_right': (house_right - window_margin - self.WINDOW_SIZE, top_window_y),
            'middle': (house_right - self.LONG_WINDOW_WIDTH - window_margin,
                       first_floor_window_y)
        }

        for pos in ['top_left', 'top_right']:
            x, y = window_positions[pos]
            draw.rectangle(
                [(x, y), (x + self.WINDOW_SIZE, y + self.WINDOW_SIZE)],
                outline='black',
                width=self.LINE_WIDTH
            )
        
        x, y = window_positions['middle']
        draw.rectangle(
            [(x, y), (x + self.LONG_WINDOW_WIDTH, y + self.LONG_WINDOW_HEIGHT)],
            outline='black',
            width=self.LINE_WIDTH
        )
        
        # Signature box
        sig_box_x1, sig_box_y1 = 50, 50
        sig_box_x2, sig_box_y2 = sig_box_x1 + self.SIGNATURE_BOX_WIDTH, sig_box_y1 + self.SIGNATURE_BOX_HEIGHT
        draw.rectangle(
            [(sig_box_x1, sig_box_y1), (sig_box_x2, sig_box_y2)],
            outline='black',
            width=self.LINE_WIDTH
        )

        # Load a scalable TrueType font
        font = ImageFont.truetype(self.FONT_PATH, self.SIGNATURE_FONT_SIZE)
        
        bbox = draw.textbbox((0, 0), self.SIGNATURE_TEXT, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        text_x = sig_box_x1 + (self.SIGNATURE_BOX_WIDTH - text_width) // 2
        text_y = sig_box_y1 + (self.SIGNATURE_BOX_HEIGHT - text_height) // 2

        draw.text((text_x, text_y), self.SIGNATURE_TEXT, fill='black', font=font)

    def generate_image(self, output_path="../../assets/images/components/signature/signature.png"):
        # Ensure directories exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Create canvas
        canvas = Image.new('RGB', (self.FINAL_SIZE, self.FINAL_SIZE), 'WHITE')
        draw = ImageDraw.Draw(canvas)
        
        # Draw content
        self.draw_house(draw)
        
        # Save the image
        canvas.save(output_path)
        print(f"Saved image to {output_path}")

def main():
    generator = SignatureHouseGenerator()
    generator.generate_image()

if __name__ == "__main__":
    main()
