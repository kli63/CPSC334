import tkinter as tk
from tkinter import ttk
import time
from enum import Enum
import threading

class RobotEmotion(Enum):
    HAPPY = "Happy 😊"
    LAZY = "Lazy 😴"
    REBELLIOUS = "Rebellious 😈"

class BrachioGraphGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Creative BrachioGraph")
        
        # State variables
        self.is_drawing = False
        self.progress = 0
        self.patience = 100  # Starts at 100%
        self.current_emotion = RobotEmotion.HAPPY
        self.thumbs_up_count = 0
        self.thumbs_down_count = 0
        self.drawing_paused = False
        
        self.setup_gui()
        self.start_patience_decay()
        
    def setup_gui(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Emotion display
        self.emotion_label = ttk.Label(
            main_frame, 
            text=self.current_emotion.value,
            font=('Arial', 24)
        )
        self.emotion_label.grid(row=0, column=0, columnspan=3, pady=10)
        
        # Canvas for drawing
        self.canvas = tk.Canvas(
            main_frame,
            width=400,
            height=400,
            bg='white',
            bd=2,
            relief='solid'
        )
        self.canvas.grid(row=1, column=0, columnspan=3, pady=10)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            main_frame,
            length=400,
            mode='determinate',
            variable=self.progress_var
        )
        self.progress_bar.grid(row=2, column=0, columnspan=3, pady=10)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=10)
        
        # Thumbs up button
        self.thumbs_up_btn = ttk.Button(
            button_frame,
            text="👍",
            command=self.thumbs_up
        )
        self.thumbs_up_btn.grid(row=0, column=0, padx=10)
        
        # Start/Pause button
        self.start_pause_btn = ttk.Button(
            button_frame,
            text="Start Drawing",
            command=self.toggle_drawing
        )
        self.start_pause_btn.grid(row=0, column=1, padx=10)
        
        # Thumbs down button
        self.thumbs_down_btn = ttk.Button(
            button_frame,
            text="👎",
            command=self.thumbs_down
        )
        self.thumbs_down_btn.grid(row=0, column=2, padx=10)
        
        # Status message
        self.status_label = ttk.Label(
            main_frame,
            text="Ready to draw",
            font=('Arial', 12)
        )
        self.status_label.grid(row=4, column=0, columnspan=3, pady=10)
        
    def start_patience_decay(self):
        def decay_loop():
            while True:
                if not self.drawing_paused:
                    self.patience -= 5
                    if self.patience <= 0:
                        self.trigger_random_rebellion()
                        self.patience = 100
                time.sleep(15)  # Decay every 15 seconds
                
        patience_thread = threading.Thread(target=decay_loop, daemon=True)
        patience_thread.start()
        
    def trigger_random_rebellion(self):
        import random
        self.current_emotion = random.choice([RobotEmotion.LAZY, RobotEmotion.REBELLIOUS])
        self.emotion_label.config(text=self.current_emotion.value)
        self.thumbs_up_count = 0
        self.thumbs_down_count = 0
        self.update_status()
        
    def thumbs_up(self):
        if self.current_emotion == RobotEmotion.LAZY:
            self.thumbs_up_count += 1
            if self.thumbs_up_count >= 5:
                self.current_emotion = RobotEmotion.HAPPY
                self.emotion_label.config(text=self.current_emotion.value)
                self.drawing_paused = False
        self.update_status()
        
    def thumbs_down(self):
        if self.current_emotion == RobotEmotion.REBELLIOUS:
            self.thumbs_down_count += 1
            if self.thumbs_down_count >= 5:
                self.current_emotion = RobotEmotion.HAPPY
                self.emotion_label.config(text=self.current_emotion.value)
                self.drawing_paused = False
        self.update_status()
        
    def toggle_drawing(self):
        if not self.is_drawing:
            self.is_drawing = True
            self.start_pause_btn.config(text="Pause Drawing")
            self.start_drawing_progress()
        else:
            self.is_drawing = False
            self.start_pause_btn.config(text="Resume Drawing")
            
    def start_drawing_progress(self):
        def progress_loop():
            while self.is_drawing and self.progress < 100:
                if not self.drawing_paused:
                    self.progress += 0.28  # Complete in ~5 minutes
                    self.progress_var.set(self.progress)
                    
                    if self.current_emotion in [RobotEmotion.LAZY, RobotEmotion.REBELLIOUS]:
                        if (self.current_emotion == RobotEmotion.LAZY and self.thumbs_up_count < 5) or \
                           (self.current_emotion == RobotEmotion.REBELLIOUS and self.thumbs_down_count < 5):
                            self.drawing_paused = True
                            
                time.sleep(0.1)
                
            if self.progress >= 100:
                self.is_drawing = False
                self.progress = 0
                self.start_pause_btn.config(text="Start Drawing")
                
        progress_thread = threading.Thread(target=progress_loop, daemon=True)
        progress_thread.start()
        
    def update_status(self):
        status_text = ""
        if self.current_emotion == RobotEmotion.LAZY:
            remaining = max(0, 5 - self.thumbs_up_count)
            status_text = f"Robot is feeling lazy! Need {remaining} more encouragements!"
        elif self.current_emotion == RobotEmotion.REBELLIOUS:
            remaining = max(0, 5 - self.thumbs_down_count)
            status_text = f"Robot is being rebellious! Need {remaining} more discouragements!"
        elif self.current_emotion == RobotEmotion.HAPPY:
            status_text = "Robot is happy and drawing!"
            
        if self.drawing_paused:
            status_text += " (Drawing paused for 15 seconds)"
            
        self.status_label.config(text=status_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = BrachioGraphGUI(root)
    root.mainloop()