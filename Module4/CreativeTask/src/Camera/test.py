import sys
import os

# Get the absolute path to the BrachioGraph directory
# current_dir = os.path.dirname(os.path.abspath(__file__))
# brachiograph_dir = os.path.join(os.path.dirname(current_dir), 'BrachioGraph')
# print(current_dir)
# print(brachiograph_dir)
# sys.path.insert(0, brachiograph_dir)

from tkinter import Tk, Label, Button, Frame
from picamera2 import Picamera2
import cv2
import PIL.Image, PIL.ImageTk
import time
import threading
import tflite_runtime.interpreter as tflite
import numpy as np

# Now import linedraw
try:
    from CPSC334.Module4.CreativeTask.src.Robot.linedraw import vectorise, makesvg, lines_to_file
    print("Successfully imported linedraw")
except Exception as e:
    print(f"Error importing linedraw: {e}")
    
from tkinter import Canvas
import PIL.ImageDraw
import math

class CameraApp:
    def __init__(self, root, camera, save_dir="../../assets/images"):
        # initializing variables and setting up the gui
        self.root = root
        self.camera = camera
        self.save_dir = save_dir
        self.frame = None
        self.captured_image = None
        self.processed_image = None
        self.image_captured = False
        self.is_processing = False
        
        self.fullscreen = False
        
        self.loading_frames = [
            "⠋", "⠙", "⠹",
            "⠸", "⠼", "⠴",
            "⠦", "⠧", "⠇",
            "⠏"
        ]
        self.loading_index = 0
        
        self.animation_frame = 0
        self.is_animating = False
        self.svg_content = None
        self.drawing_captured = False

        # Load the TFLite model
        try:
            model_path = "../../assets/model/deeplabv3_257_mv_gpu.tflite"
            self.interpreter = tflite.Interpreter(model_path=model_path)
            self.interpreter.allocate_tensors()
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
            print("Model loaded successfully")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.interpreter = None

        # ensuring the save directory exists
        os.makedirs(self.save_dir, exist_ok=True)

        # setting up the protocol to handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # setting up full-screen mode for the window
        self.root.attributes("-fullscreen", self.fullscreen)
        self.root.bind("<Escape>", self.toggle_fullscreen)
        self.root.bind("<F11>", self.toggle_fullscreen)

        # Create two main halves of the screen
        left_half = Frame(root, width=root.winfo_screenwidth() // 2)
        left_half.pack(side="left", fill="both", expand=True)
        left_half.pack_propagate(False)  # Prevent the frame from shrinking

        right_half = Frame(root, width=root.winfo_screenwidth() // 2)
        right_half.pack(side="left", fill="both", expand=True)

        # Create a frame for camera and buttons in the left half
        camera_container = Frame(left_half)
        camera_container.pack(expand=True)

        # creating a label to display the camera preview with fixed size
        self.label = Label(camera_container, width=480, height=480)
        self.label.pack()

        # Create button frame that's tied to camera width
        button_frame = Frame(camera_container)
        button_frame.pack(fill="x", pady=10)

        # adding a button to take a photo
        self.capture_button = Button(button_frame, text="take photo [ ◉¯]", command=self.capture_image)
        self.capture_button.pack(expand=True)

        # adding an approve button with a smiley face emoji, initially hidden
        self.approve_button = Button(button_frame, text="accept 😊", command=self.save_image)
        self.approve_button.pack(expand=True)
        self.approve_button.pack_forget()  # hide initially

        # adding a retake button with a sad face emoji, initially hidden
        self.retake_button = Button(button_frame, text="reject 😞", command=self.retake_image)
        self.retake_button.pack(expand=True)
        self.retake_button.pack_forget()  # hide initially
        
        self.drawing_container = Frame(right_half)
        self.drawing_container.pack(expand=True)
        
        self.right_label = Label(self.drawing_container, width=480, height=480)
        self.right_label.pack()
        
        # Create button frame for right side
        self.right_button_frame = Frame(self.drawing_container)
        self.right_button_frame.pack(fill="x", pady=10)
        
        self.drawing_approve_button = Button(self.right_button_frame, text="accept drawing 😊", 
                                          command=self.approve_drawing)
        self.drawing_approve_button.pack(expand=True)
        self.drawing_approve_button.pack_forget()
        
        self.drawing_reject_button = Button(self.right_button_frame, text="reject drawing 😞", 
                                         command=self.reject_drawing)
        self.drawing_reject_button.pack(expand=True)
        self.drawing_reject_button.pack_forget()

        # Create paper airplane animation canvas
        self.animation_canvas = Canvas(root, width=200, height=200, 
                                     bg='black', highlightthickness=0)
        self.animation_canvas.place_forget()
        
        self.airplane = self.animation_canvas.create_polygon(
            0, 0, 30, 15, 0, 30, 10, 15,
            fill='white', outline='white'
        )

        # starting the continuous frame update
        self.update_frame()

    
    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)
        if not self.fullscreen:
            # Set a reasonable window size when not fullscreen
            self.root.geometry("800x600")
        return "break"
    
    def update_frame(self):
        try:
            # continuously updating the camera preview
            if not self.image_captured:
                frame = self.camera.capture_array()
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                
                left_crop = (640 - 480) // 2
                cropped_frame = frame[:, left_crop:left_crop + 480]
                self.frame = cropped_frame

                img = PIL.Image.fromarray(cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2RGB))
                imgtk = PIL.ImageTk.PhotoImage(image=img)
                self.label.imgtk = imgtk
                self.label.configure(image=imgtk, text="")
            elif self.is_processing:
                # Animate loading text
                self.loading_index = (self.loading_index + 1) % len(self.loading_frames)
                self.label.configure(
                    text=self.loading_frames[self.loading_index],
                    font=("Helvetica", 24),
                    foreground="white",
                    compound="center"
                )

        except Exception as e:
            print(f"Error in update_frame: {e}")

        self.root.after(100, self.update_frame)

    # lol this doesn't work yet...
    def process_image_thread(self):
        try:
            print("Starting image processing")
            time.sleep(1)
            
            if self.interpreter:
                print("Applying background blur")
                input_size = (257, 257)
                input_image = cv2.resize(self.captured_image, input_size)
                input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)
                input_image = input_image.astype(np.float32) / 255.0
                input_image = np.expand_dims(input_image, axis=0)

                self.interpreter.set_tensor(self.input_details[0]['index'], input_image)
                self.interpreter.invoke()
                mask = self.interpreter.get_tensor(self.output_details[0]['index'])
                
                person_mask = mask[0, :, :, 15]
                person_mask = cv2.resize(person_mask, (480, 480))
                person_mask = (person_mask > 0.2).astype(np.uint8) 
                
                kernel = np.ones((5,5), np.uint8)
                person_mask = cv2.dilate(person_mask, kernel, iterations=2)
                person_mask = cv2.GaussianBlur(person_mask.astype(float), (21, 21), 0)
                
                background = self.captured_image.copy()
                for _ in range(5): 
                    background = cv2.GaussianBlur(background, (151, 151), 50)
                
                person_mask = np.expand_dims(person_mask, axis=-1)
                person_mask = np.repeat(person_mask, 3, axis=-1)

                self.processed_image = (person_mask * self.captured_image + 
                                     (1 - person_mask) * background).astype(np.uint8)
            else:
                print("No model available, applying simple blur")
                self.processed_image = cv2.GaussianBlur(self.captured_image, (151, 151), 50)

            print("complete")
            self.root.after(0, self.processing_complete)
        except Exception as e:
            print(f"Error in process_image_thread: {e}")
            self.root.after(0, self.processing_failed)

    def processing_complete(self):
        """Called when processing is done"""
        print("Showing processed image")
        self.is_processing = False
        
        # Display the processed image
        img = PIL.Image.fromarray(cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2RGB))
        imgtk = PIL.ImageTk.PhotoImage(image=img)
        self.label.imgtk = imgtk
        self.label.configure(image=imgtk, text="")
        
        # Show the buttons
        self.approve_button.pack(expand=True)
        self.retake_button.pack(expand=True)

    def processing_failed(self):
        """Called if processing fails"""
        print("failed")
        self.is_processing = False
        self.image_captured = False
        self.capture_button.pack(expand=True)
        self.label.configure(text="failed, please try again", font=("Helvetica", 16))

    def capture_image(self):
        print("Capturing image")
        self.image_captured = True
        self.is_processing = True
        self.captured_image = self.frame.copy()
        self.capture_button.pack_forget()
        
        # Start processing in background thread
        threading.Thread(target=self.process_image_thread, daemon=True).start()

    def save_image(self):
        if self.image_captured and self.processed_image is not None:
            # resized_image = cv2.resize(self.processed_image, (1024, 1024))
            # timestamp = time.strftime("%Y%m%d_%H%M%S")
            # filename = os.path.join(self.save_dir, f"image_{timestamp}.jpg")
            # cv2.imwrite(filename, resized_image)
            # print(f"Image saved: {filename}")
            
            # self.image_captured = False
            # self.processed_image = None
            # self.approve_button.pack_forget()
            # self.retake_button.pack_forget()
            # self.capture_button.pack(expand=True)
            try:
                # First save the processed image
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                resized_image = cv2.resize(self.processed_image, (1024, 1024))
                image_filename = os.path.join(self.save_dir, f"image_{timestamp}.jpg")
                cv2.imwrite(image_filename, resized_image)
                print(f"Image saved: {image_filename}")

                # Convert to vector format
                print("Converting to vector format...")
                
                # Change the export paths to assets/data
                svg_folder = "../../assets/data/"
                json_folder = "../../assets/data/"
                
                # Generate lines from the image
                lines = vectorise(
                    image_filename,
                    resolution=1024,
                    draw_contours=2,
                    repeat_contours=1,
                    draw_hatch=16,
                    repeat_hatch=1,
                    svg_folder="../../assets/data/",
                    json_folder="../../assets/data/"
                )
                # Save as SVG
                svg_filename = os.path.join(svg_folder, f"drawing_{timestamp}.svg")
                with open(svg_filename, 'w') as f:
                    f.write(makesvg(lines))
                print(f"SVG saved: {svg_filename}")
                
                # Save as JSON
                json_filename = os.path.join(json_folder, f"drawing_{timestamp}.json")
                lines_to_file(lines, json_filename)
                print(f"JSON saved: {json_filename}")

                # Reset the UI state
                self.image_captured = False
                self.processed_image = None
                self.approve_button.pack_forget()
                self.retake_button.pack_forget()
                self.capture_button.pack(expand=True)
                
                print("Vector conversion complete")

            except Exception as e:
                print(f"Error in vector conversion: {e}")
                # Still reset UI even if vector conversion fails
                self.image_captured = False
                self.processed_image = None
                self.approve_button.pack_forget()
                self.retake_button.pack_forget()
                self.capture_button.pack(expand=True)

    def retake_image(self):
        self.image_captured = False
        self.processed_image = None
        self.approve_button.pack_forget()
        self.retake_button.pack_forget()
        self.label.configure(text="okay... i'll try again... 😞", font=("Helvetica", 16))
        self.capture_button.pack(expand=True)

    def animate_airplane(self):
        if not self.is_animating:
            return
            
        # Get screen dimensions
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        
        # Calculate animation path
        start_x = width // 4
        end_x = 3 * width // 4
        center_y = height // 2
        
        # Current position (move across in 50 steps)
        progress = min(1.0, self.animation_frame / 50)
        current_x = start_x + (end_x - start_x) * progress
        
        # Add wave motion
        wave_y = center_y + math.sin(progress * 6 * math.pi) * 30
        
        # Position the canvas
        self.animation_canvas.place(
            x=current_x - 100,
            y=wave_y - 100
        )
        
        # Rotate the airplane
        angle = math.sin(progress * 4 * math.pi) * 10
        self.animation_canvas.delete("all")
        self.airplane = self.animation_canvas.create_polygon(
            0, 0, 30, 15, 0, 30, 10, 15,
            fill='white', outline='white'
        )
        
        # Continue animation
        self.animation_frame += 1
        if progress < 1.0:
            self.root.after(20, self.animate_airplane)
        else:
            self.animation_canvas.place_forget()
            self.is_animating = False

    def display_svg(self, svg_content):
        """Display the SVG on the right side"""
        img = PIL.Image.new('RGB', (480, 480), 'white')
        draw = PIL.ImageDraw.Draw(img)
        
        lines = svg_content.split('\n')
        for line in lines:
            if 'polyline points="' in line:
                points_str = line.split('points="')[1].split('"')[0]
                points = [float(x) for x in points_str.split(',')]
                scaled_points = [(x * 480/1024, y * 480/1024) for x, y in zip(points[::2], points[1::2])]
                if len(scaled_points) >= 2:
                    draw.line(scaled_points, fill='black', width=1)
        
        imgtk = PIL.ImageTk.PhotoImage(img)
        self.right_label.imgtk = imgtk
        self.right_label.configure(image=imgtk)
        
        self.drawing_approve_button.pack(expand=True)
        self.drawing_reject_button.pack(expand=True)
        self.drawing_captured = True

    def approve_drawing(self):
        """Handle approval of the drawing"""
        print("Drawing approved")
        self.drawing_approve_button.pack_forget()
        self.drawing_reject_button.pack_forget()
        self.drawing_captured = False
        # Add any additional actions you want for drawing approval

    def reject_drawing(self):
        """Handle rejection of the drawing"""
        print("Drawing rejected")
        self.drawing_approve_button.pack_forget()
        self.drawing_reject_button.pack_forget()
        self.drawing_captured = False
        self.right_label.configure(image='')
        # Add any additional actions you want for drawing rejection
        
    def on_close(self):
        self.camera.stop()
        self.camera.close()
        self.root.quit()

if __name__ == "__main__":
    picam2 = Picamera2()
    config = picam2.create_preview_configuration()
    picam2.configure(config)
    picam2.start()

    root = Tk()
    root.title("Robotic Caricaturist d[o_0]b")
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}+0+0")
    root.overrideredirect(True)
    
    app = CameraApp(root, picam2)
    root.mainloop()