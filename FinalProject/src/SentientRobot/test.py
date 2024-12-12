import tkinter as tk
from tkinter import ttk
import time
import random
import threading
from datetime import datetime
from tqdm import tqdm
import pygame
from robot_face import PygameEmbed

class BrachioGraphGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Creative BrachioGraph")
        
        pygame.init()
        
        self.is_drawing = False
        self.is_paused = False
        self.progress = 0
        self.current_state = "HAPPY"
        self.thumbs_up_count = 0
        self.thumbs_down_count = 0
        self.needs_encouragement = False
        self.needs_discouragement = False
        self.timer = None
        
        self.setup_gui()

    def setup_gui(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky="nsew")
        
        self.face_display = PygameEmbed(frame, 400, 300)
        self.face_display.grid(row=0, column=0, columnspan=3, pady=10)
        
        self.canvas = tk.Canvas(frame, width=400, height=400, bg='white', relief='solid', bd=1)
        self.canvas.grid(row=1, column=0, columnspan=3, pady=10)
        self.update_canvas_message("Ready to Start Drawing!\nPlace paper on the Designated Spot")
        
        self.status_label = ttk.Label(frame, text="Ready to start", font=('Arial', 12))
        self.status_label.grid(row=2, column=0, columnspan=3, pady=5)
        
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(frame, length=400, mode='determinate', variable=self.progress_var)
        self.progress_bar.grid(row=3, column=0, columnspan=3, pady=10)
        
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=10)
        
        self.discourage_btn = ttk.Button(button_frame, text="</3", command=self.discourage)
        self.discourage_btn.grid(row=0, column=0, padx=10)
        
        control_frame = ttk.Frame(button_frame)
        control_frame.grid(row=0, column=1, padx=20)
        
        self.start_button = ttk.Button(control_frame, text="Start Drawing", command=self.start_drawing)
        self.start_button.grid(row=0, column=0, padx=5)
        
        self.pause_button = ttk.Button(control_frame, text="Pause", command=self.toggle_pause, state='disabled')
        self.pause_button.grid(row=0, column=1, padx=5)
        
        self.encourage_btn = ttk.Button(button_frame, text="<3", command=self.encourage)
        self.encourage_btn.grid(row=0, column=2, padx=10)

    def update_canvas_message(self, message):
        self.canvas.delete("all")
        self.canvas.create_text(
            200, 200,
            text=message,
            font=('Arial', 14),
            justify=tk.CENTER,
            width=350
        )

    def log_status(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
        self.status_label.config(text=message)

    def update_emotion(self, emotion, emoji):
        self.current_state = emotion
        self.face_display.set_emotion(emotion)
        self.log_status(f"Robot is now {emotion}")
        
        if emotion == "LAZY":
            self.needs_encouragement = True
            self.needs_discouragement = False
            self.thumbs_up_count = 0
            self.log_status("Robot is lazy! Give encouragement <3")
            self.update_canvas_message("Too tired to draw...\nNeed encouragement!")
        elif emotion == "REBELLIOUS":
            self.needs_encouragement = False
            self.needs_discouragement = True
            self.thumbs_down_count = 0
            self.log_status("Robot is rebellious! Give discouragement </3")
            self.update_canvas_message("Not following instructions!\nNeed discipline!")
        else:
            self.needs_encouragement = False
            self.needs_discouragement = False
            if self.is_drawing:
                self.update_canvas_message("Drawing in progress...")

    def toggle_pause(self):
        if self.is_drawing:
            self.is_paused = not self.is_paused
            self.pause_button.config(text="Resume" if self.is_paused else "Pause")
            status = "paused" if self.is_paused else "resumed"
            self.log_status(f"Drawing {status}")
            if self.is_paused:
                self.update_canvas_message("Drawing Paused")
            else:
                self.update_canvas_message("Drawing in progress...")

    def encourage(self):
        if self.needs_encouragement:
            self.thumbs_up_count += 1
            remaining = 5 - self.thumbs_up_count
            if remaining > 0:
                self.log_status(f"Need {remaining} more encouragements!")
            else:
                self.update_emotion("HAPPY", "😊")
                self.log_status("Robot is encouraged and happy again!")

    def discourage(self):
        if self.needs_discouragement:
            self.thumbs_down_count += 1
            remaining = 5 - self.thumbs_down_count
            if remaining > 0:
                self.log_status(f"Need {remaining} more discouragements!")
            else:
                self.update_emotion("HAPPY", "😊")
                self.log_status("Robot is discouraged and back to work!")

    def reset_timer(self, state_description):
        if self.timer:
            self.timer.close()
        self.timer = tqdm(total=15, desc=state_description, unit="sec")

    def start_drawing(self):
        self.start_button.config(state='disabled')
        self.pause_button.config(state='normal')
        self.progress_var.set(0)
        self.progress = 0
        self.is_drawing = True
        self.is_paused = False
        self.update_emotion("HAPPY", "😊")
        self.update_canvas_message("Drawing in progress...")
        
        def run_robot():
            start_time = time.time()
            last_emotion_time = start_time
            pause_start_time = 0
            
            self.reset_timer("Happy State")
            
            while self.is_drawing and self.progress < 100:
                current_time = time.time()
                
                if self.is_paused:
                    if pause_start_time == 0:
                        pause_start_time = current_time
                    start_time = start_time + (current_time - pause_start_time)
                    last_emotion_time = last_emotion_time + (current_time - pause_start_time)
                    pause_start_time = current_time
                    time.sleep(0.1)
                    continue

                pause_start_time = 0
                elapsed_time = current_time - start_time
                
                if self.current_state == "HAPPY":
                    self.progress = (elapsed_time / 300) * 100
                    self.progress_var.set(min(100, self.progress))
                
                if current_time - last_emotion_time >= 15:
                    new_emotion = random.choice(["LAZY", "REBELLIOUS"])
                    emoji = "😴" if new_emotion == "LAZY" else "😈"
                    self.update_emotion(new_emotion, emoji)
                    self.reset_timer(f"{new_emotion} State - Waiting for interaction")
                    
                    interaction_start = time.time()
                    while time.time() - interaction_start < 15 and self.current_state != "HAPPY":
                        self.timer.update(1)
                        time.sleep(1)
                    
                    if self.current_state != "HAPPY":
                        self.reset_timer("Taking a break")
                        self.log_status("Robot stopped drawing for 15 seconds!")
                        self.update_canvas_message("Taking a break for 15 seconds...")
                        
                        for _ in range(15):
                            self.timer.update(1)
                            time.sleep(1)
                        
                        self.update_emotion("HAPPY", "😊")
                    
                    last_emotion_time = time.time()
                    self.reset_timer("Happy State")
                else:
                    self.timer.update(1)
                    time.sleep(1)
            
            self.is_drawing = False
            self.start_button.config(state='normal')
            self.pause_button.config(state='disabled')
            self.log_status("Drawing complete!")
            self.update_canvas_message("Ready to Start Drawing!\nPlace paper on the Designated Spot")
            if self.timer:
                self.timer.close()
            
        threading.Thread(target=run_robot, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = BrachioGraphGUI(root)
    root.mainloop()