from tkinter import Tk, Label, Button, CENTER, Frame
from picamera2 import Picamera2
import cv2
import PIL.Image, PIL.ImageTk
import os
import time

class CameraApp:
    def __init__(self, root, camera, save_dir="../../images"):
        # initializing variables and setting up the gui
        self.root = root
        self.camera = camera
        self.save_dir = save_dir
        self.frame = None
        self.captured_image = None
        self.image_captured = False

        # ensuring the save directory exists
        os.makedirs(self.save_dir, exist_ok=True)

        # setting up the protocol to handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # setting up full-screen mode for the window
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))

        # Create two main halves of the screen
        left_half = Frame(root, width=root.winfo_screenwidth()//2)
        left_half.pack(side="left", fill="both", expand=True)
        left_half.pack_propagate(False)  # Prevent the frame from shrinking

        right_half = Frame(root, width=root.winfo_screenwidth()//2)
        right_half.pack(side="left", fill="both", expand=True)

        # Create a frame for camera and buttons in the left half
        camera_container = Frame(left_half)
        camera_container.pack(expand=True)

        # creating a label to display the camera preview with fixed size
        self.label = Label(camera_container, width=640, height=480)
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

    def update_frame(self):
        # continuously updating the camera preview
        if not self.image_captured:
            frame = self.camera.capture_array()  # capturing the camera frame
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # converting frame to bgr
            self.frame = frame

            # converting the frame to tkinter-compatible format
            img = PIL.Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
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
            timestamp = time.strftime("%Y%m%d_%H%M%S")  # generating a unique filename
            filename = os.path.join(self.save_dir, f"image_{timestamp}.jpg")
            cv2.imwrite(filename, self.captured_image)  # saving the image
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
    
    # Get screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Set the initial window size to match screen size
    root.geometry(f"{screen_width}x{screen_height}+0+0")
    
    # Remove window decorations
    root.overrideredirect(True)
    
    # Create the app
    app = CameraApp(root, picam2)
    
    root.mainloop()