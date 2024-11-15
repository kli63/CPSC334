from tkinter import Tk, Label, Button, Frame
from picamera2 import Picamera2
import cv2
import numpy as np
import PIL.Image, PIL.ImageTk
import os
import time

class CameraApp:
    def __init__(self, root, camera, save_dir="../../assets/images"):
        # initializing variables and setting up the gui
        self.root = root
        self.camera = camera
        self.save_dir = save_dir
        self.frame = None
        self.captured_image = None
        self.image_captured = False

        # Load pre-trained segmentation model (e.g., MobileNet)
        self.net = cv2.dnn.readNetFromONNX("../../assets/model/tiny-yolov3-11.onnx")  # Replace with your ONNX model path

        # ensuring the save directory exists
        os.makedirs(self.save_dir, exist_ok=True)

        # setting up the protocol to handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # setting up full-screen mode for the window
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))

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

        # starting the continuous frame update
        self.update_frame()

    def process_frame(self, frame):
        """
        Process the frame to blur the background and keep people in focus.
        """
        h, w = frame.shape[:2]

        # Create a blob from the frame and pass it to the segmentation model
        blob = cv2.dnn.blobFromImage(frame, scalefactor=1/255.0, size=(224, 224), mean=(0, 0, 0), swapRB=True, crop=False)
        self.net.setInput(blob)
        output = self.net.forward()  # Forward pass

        # Reshape output to match the input image
        segmentation_map = output[0, 0]  # Assuming the person class is at index 0
        segmentation_map = cv2.resize(segmentation_map, (w, h))

        # Create a binary mask for the person
        _, binary_mask = cv2.threshold(segmentation_map, 0.5, 1, cv2.THRESH_BINARY)
        binary_mask = binary_mask.astype(np.uint8)

        # Blur the background
        blurred_frame = cv2.GaussianBlur(frame, (21, 21), 0)

        # Combine the original frame and blurred frame using the mask
        foreground = cv2.bitwise_and(frame, frame, mask=binary_mask)
        background = cv2.bitwise_and(blurred_frame, blurred_frame, mask=cv2.bitwise_not(binary_mask))
        processed_frame = cv2.add(foreground, background)

        return processed_frame

    def update_frame(self):
        # continuously updating the camera preview
        if not self.image_captured:
            frame = self.camera.capture_array()  # capturing the camera frame
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # converting frame to bgr

            # cropping the frame to 480x480 by trimming sides
            left_crop = (640 - 480) // 2
            cropped_frame = frame[:, left_crop:left_crop + 480]

            # Apply background blur
            processed_frame = self.process_frame(cropped_frame)
            self.frame = processed_frame  # Save the processed frame for later use

            # converting the processed frame to tkinter-compatible format
            img = PIL.Image.fromarray(cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB))
            imgtk = PIL.ImageTk.PhotoImage(image=img)
            self.label.imgtk = imgtk
            self.label.configure(image=imgtk, text="")  # clear text if any

        # scheduling the next frame update
        self.root.after(10, self.update_frame)

    def capture_image(self):
        # capturing the current frame
        self.image_captured = True
        self.captured_image = self.frame

        # hide the capture button and show the approve and retake buttons
        self.capture_button.pack_forget()
        self.approve_button.pack(expand=True)
        self.retake_button.pack(expand=True)

    def save_image(self):
        # saving the captured image to the specified directory
        if self.image_captured:
            # resize the processed image to 1024x1024 for saving
            resized_image = cv2.resize(self.captured_image, (1024, 1024))

            timestamp = time.strftime("%Y%m%d_%H%M%S")  # generating a unique filename
            filename = os.path.join(self.save_dir, f"image_{timestamp}.jpg")
            cv2.imwrite(filename, resized_image)  # saving the resized image
            print(f"image saved: {filename}")
            self.image_captured = False  # resetting the capture state

            # hide the approve and retake buttons after saving
            self.approve_button.pack_forget()
            self.retake_button.pack_forget()

            # re-enable the capture button for the next photo
            self.capture_button.pack(expand=True)

    def retake_image(self):
        # resetting for retaking the image
        self.image_captured = False  # resetting the capture state

        # hide the approve and retake buttons, show sad face message, re-enable capture button
        self.approve_button.pack_forget()
        self.retake_button.pack_forget()
        self.label.configure(text="okay... i'll try again... 😞", font=("Helvetica", 16))
        self.capture_button.pack(expand=True)

    def on_close(self):
        # cleaning up the camera resources and closing the gui
        self.camera.stop()  # stopping the camera
        self.camera.close()  # closing the camera resource
        self.root.quit()  # closing the tkinter window

if __name__ == "__main__":
    # initializing the camera
    picam2 = Picamera2()
    config = picam2.create_preview_configuration()
    picam2.configure(config)
    picam2.start()

    # setting up the tkinter gui with title emojis
    root = Tk()
    root.title("Robotic Caricaturist d[o_0]b")
    
    # get screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # set the initial window size to match screen size
    root.geometry(f"{screen_width}x{screen_height}+0+0")
    
    # remove window decorations
    root.overrideredirect(True)
    
    # create the app
    app = CameraApp(root, picam2)
    
    root.mainloop()
