from picamera2 import Picamera2
from tkinter import Tk
from camera import CameraApp


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