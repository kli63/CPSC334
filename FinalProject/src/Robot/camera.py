import os
import io

from tkinter import Label, Button, Frame
import cv2
import PIL.Image, PIL.ImageTk
from PIL import Image, ImageTk
import time
import threading
import tflite_runtime.interpreter as tflite
import numpy as np

import cairosvg
# Now import linedraw
try:
    from process import vectorise, makesvg, lines_to_file
    print("Successfully imported linedraw")
except Exception as e:
    print(f"Error importing linedraw: {e}")
    
from tkinter import Canvas
import PIL.ImageDraw
import math

from robot import Robot


class CameraApp:
    def __init__(self, root, camera, save_dir="../../assets/images"):
        # initializing variables and setting up the gui
        self.robot = Robot()
        
        self.root = root
        self.camera = camera
        self.save_dir = save_dir
        self.frame = None
        self.captured_image = None
        self.processed_image = None
        self.image_captured = False
        self.is_processing = False
        self.is_sending = False
        self.is_drawing = False
        self.drawing_progress = 0.0

        
        self.fullscreen = False
        
        self.loading_frames = [
            "⠋", "⠙", "⠹",
            "⠸", "⠼", "⠴",
            "⠦", "⠧", "⠇",
            "⠏"
        ]
        self.loading_index = 0

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


        # Create a single parent frame to hold both halves
        main_frame = Frame(root)
        main_frame.pack(fill="both", expand=True)

        # Create two main halves of the screen within the parent frame
        left_half = Frame(main_frame, width=root.winfo_screenwidth() // 2)
        left_half.pack(side="left", fill="both", expand=True)
        left_half.pack_propagate(False)  # Prevent the frame from shrinking

        right_half = Frame(main_frame, width=root.winfo_screenwidth() // 2)
        right_half.pack(side="left", fill="both", expand=True)
        right_half.pack_propagate(False)  # Prevent the frame from shrinking

        # Create a frame for the camera and buttons in the left half
        camera_container = Frame(left_half)
        camera_container.pack(expand=True)

        # Create a label to display the camera preview with fixed size
        self.camera_label = Label(camera_container, width=480, height=480)
        self.camera_label.pack()

        # Create button frame tied to the camera width
        button_frame = Frame(camera_container)
        button_frame.pack(fill="x", pady=10)

        # Add buttons (capture, accept, retake) to the button frame
        self.capture_button = Button(button_frame, text="take photo [ ◉¯]", command=self.capture_image)
        self.capture_button.pack(expand=True)

        self.approve_button = Button(button_frame, text="accept 😊", command=self.save_image)
        self.approve_button.pack(expand=True)
        self.approve_button.pack_forget()  # Initially hidden

        self.retake_button = Button(button_frame, text="reject 😞", command=self.retake_image)
        self.retake_button.pack(expand=True)
        self.retake_button.pack_forget()  # Initially hidden
        
        svg_container = Frame(right_half)
        svg_container.pack(expand=True)

        # Create the black box in the right half
        self.svg_canvas = Canvas(svg_container, width=480, height=480, bg="white", highlightthickness=1, highlightbackground="black")
        self.svg_canvas.pack(expand=True)
        
        
        self.loading_label = Label(self.root, text="", font=("Helvetica", 24), fg="black", highlightthickness=0,
                                   borderwidth=0)
        self.loading_label.place_forget()
        
        svg_button_frame = Frame(svg_container)
        svg_button_frame.pack(fill="x", pady=10)        
        
        self.svg_approve_button = Button(svg_button_frame, text="accept 😊", command=self.approve_svg)
        self.svg_approve_button.pack(expand=True)
        self.svg_approve_button.pack_forget()  # Initially hidden

        self.svg_reject_button = Button(svg_button_frame, text="reject 😞", command=self.reject_svg)
        self.svg_reject_button.pack(expand=True)
        self.svg_reject_button.pack_forget()  # Initially hidden

        # Add instance variables to store current file paths
        self.current_svg_path = None
        self.current_json_path = None
        
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
                self.camera_label.imgtk = imgtk
                self.camera_label.configure(image=imgtk, text="")
            elif self.is_processing:
                # Animate loading text
                self.loading_index = (self.loading_index + 1) % len(self.loading_frames)
                self.camera_label.configure(
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
        self.camera_label.imgtk = imgtk
        self.camera_label.configure(image=imgtk, text="")
        
        # Show the buttons
        self.approve_button.pack(expand=True)
        self.retake_button.pack(expand=True)

    def processing_failed(self):
        """Called if processing fails"""
        print("failed")
        self.is_processing = False
        self.image_captured = False
        self.capture_button.pack(expand=True)
        self.camera_label.configure(text="failed, please try again", font=("Helvetica", 16))

    def capture_image(self):
        print("Capturing image")
        self.image_captured = True
        self.is_processing = True
        self.captured_image = self.frame.copy()
        self.capture_button.pack_forget()
        
        # Start processing in background thread
        threading.Thread(target=self.process_image_thread, daemon=True).start()

    def save_image(self):
        """Handle saving the image with vectorization and sending animation."""
        if self.image_captured and self.processed_image is not None:
            self.approve_button.pack_forget()
            self.retake_button.pack_forget()
            
            self.is_sending = True
            self.start_sending_animation()

            # Run the vectorization in a separate thread
            def background_save():
                svg_path = self.save_vectorized_image()
                self.root.after(0, lambda: self.on_save_complete(svg_path))

            threading.Thread(target=background_save, daemon=True).start()

    def on_save_complete(self, svg_path):
        """Callback after the image save process completes."""
        self.is_sending = False
        self.stop_sending_animation()

        if svg_path:
            # Store the current paths
            self.current_svg_path = svg_path
            self.current_json_path = svg_path.replace('.svg', '.json')
            
            # Display SVG and show new approval buttons
            self.display_svg(svg_path)
            self.svg_approve_button.pack(expand=True)
            self.svg_reject_button.pack(expand=True)
            print("Vectorization and save complete.")
        else:
            print("Vectorization or save failed.")
            self.reset_ui()

        # # Reset UI
        # self.image_captured = False
        # self.processed_image = None
        # self.approve_button.pack_forget()
        # self.retake_button.pack_forget()
        # self.capture_button.pack(expand=True)
        
    def approve_svg(self):
        """Handle SVG approval - placeholder for next steps"""
        # Hide SVG approval buttons
        self.svg_approve_button.pack_forget()
        self.svg_reject_button.pack_forget()
        
        print("SVG approved - ready for next steps")
        
        self.is_drawing = True  # New state variable
        self.drawing_progress = 0.0
        self.start_drawing_animation()
        
        def update_progress(progress):
            """Callback for robot drawing progress"""
            if self.is_drawing:
                # Update the progress value - will be picked up by animation
                self.drawing_progress = progress
                
                # If drawing is complete
                if progress >= 100:
                    self.root.after(2000, self.complete_drawing)
        
        # Start the drawing with progress tracking
        self.robot.draw(self.current_json_path, update_progress)
    
    def complete_drawing(self):
        """Clean up after drawing is complete"""
        self.is_drawing = False
        self.stop_drawing_animation()
        self.reset_ui()
    
    def start_drawing_animation(self):
        """Start the drawing animation in the center of the GUI."""
        self.loading_label.lift()
        self.loading_label.place(relx=0.5, rely=0.5, anchor="center")
        self.update_drawing_animation()

    def stop_drawing_animation(self):
        """Stop the drawing animation."""
        self.loading_label.place_forget()

    def update_drawing_animation(self):
        """Update the text of the drawing animation."""
        if self.is_drawing:
            self.loading_index = (self.loading_index + 1) % len(self.loading_frames)
            current_frame = self.loading_frames[self.loading_index]
            self.loading_label.config(
                text=f"Drawing your portrait... {self.drawing_progress:.1f}% {current_frame}"
            )
            
            # Schedule next update
            self.root.after(100, self.update_drawing_animation)
        
    def reject_svg(self):
        """Handle SVG rejection"""
        try:
            # Delete SVG and JSON files
            if self.current_svg_path and os.path.exists(self.current_svg_path):
                os.remove(self.current_svg_path)
            if self.current_json_path and os.path.exists(self.current_json_path):
                os.remove(self.current_json_path)
                
            # Clear the canvas
            self.svg_canvas.delete("all")
            
            # Reset paths
            self.current_svg_path = None
            self.current_json_path = None
            
            # Hide SVG approval buttons
            self.svg_approve_button.pack_forget()
            self.svg_reject_button.pack_forget()
            
            # Reset the camera UI
            self.reset_ui()
            
        except Exception as e:
            print(f"Error in reject_svg: {e}")
            self.reset_ui()
        
    def reset_ui(self):
        """Reset the UI to initial state"""
        # Clear captured image state
        self.image_captured = False
        self.processed_image = None
        
        # Hide all buttons except capture
        self.approve_button.pack_forget()
        self.retake_button.pack_forget()
        self.svg_approve_button.pack_forget()
        self.svg_reject_button.pack_forget()
        
        # Show capture button
        self.capture_button.pack(expand=True)
        
        # Reset camera label
        self.camera_label.configure(text="")

    def save_vectorized_image(self):
        """Save the processed image as SVG and JSON."""
        try:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            resized_image = cv2.resize(self.processed_image, (1024, 1024))
            image_filename = os.path.join(self.save_dir, f"image_{timestamp}.jpg")
            cv2.imwrite(image_filename, resized_image)
            print(f"Image saved: {image_filename}")

            # Convert to vector format
            print("Converting to vector format...")
            svg_folder = "../../assets/data/"
            json_folder = "../../assets/data/"
            os.makedirs(svg_folder, exist_ok=True)
            os.makedirs(json_folder, exist_ok=True)

            # Generate lines from the image
            lines = vectorise(
                image_filename,
                resolution=1024,
                draw_contours=2,
                repeat_contours=1,
                draw_hatch=16,
                repeat_hatch=1,
                svg_folder=svg_folder,
                json_folder=json_folder
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

            return svg_filename
        except Exception as e:
            print(f"Error in save_vectorized_image: {e}")
            return None
        
    def display_svg(self, svg_path):
        """Render the SVG onto the canvas."""
        try:
            # Convert the SVG to a PNG using cairosvg
            png_data = cairosvg.svg2png(url=svg_path)
            image = Image.open(io.BytesIO(png_data))
            image = image.resize((480, 480), Image.ANTIALIAS)
            imgtk = ImageTk.PhotoImage(image)

            # Display the image on the canvas
            self.svg_canvas.delete("all")  # Clear the canvas
            self.svg_canvas.create_image(240, 240, image=imgtk)
            self.svg_canvas.image = imgtk  # Prevent garbage collection

        except Exception as e:
            print(f"Error displaying SVG: {e}")

    def retake_image(self):
        self.image_captured = False
        self.processed_image = None
        self.approve_button.pack_forget()
        self.retake_button.pack_forget()
        self.camera_label.configure(text="okay... i'll try again... 😞", font=("Helvetica", 16))
        self.capture_button.pack(expand=True)
        
    def start_sending_animation(self):
        """Start the sending animation in the center of the GUI."""
        self.loading_label.lift()
        self.loading_label.place(relx=0.5, rely=0.5, anchor="center")
        self.update_sending_animation()

    def stop_sending_animation(self):
        """Stop the sending animation."""
        self.loading_label.place_forget()

    def update_sending_animation(self):
        """Update the text of the sending animation."""
        if self.is_sending:
            current_frame = f"sending to robot d[o_0]b {self.loading_frames[self.loading_index]}"
            self.loading_label.config(text=current_frame)
            self.loading_index = (self.loading_index + 1) % len(self.loading_frames)
            self.root.after(300, self.update_sending_animation)


    def on_close(self):
        self.camera.stop()
        self.camera.close()
        self.root.quit()
        
