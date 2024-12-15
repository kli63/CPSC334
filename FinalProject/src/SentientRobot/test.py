# test.py

import tkinter as tk
from tkinter import ttk
import time
import threading
from datetime import datetime
from tqdm import tqdm
import logging
import random

from robot_logic import RobotController, RobotState
from chat import MessageWidget, ScrollableChatFrame
from constants import faces

logger = logging.getLogger("BrachioGraphGUI")

class BrachioGraphGUI:
    def __init__(self, root, fullscreen=False):
        self.root = root
        self.root.title("Creative BrachioGraph")
        if fullscreen:
            self.root.attributes('-fullscreen', True)
        else:
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            window_width = int(screen_width * 0.8)
            window_height = int(screen_height * 0.8)
            self.root.geometry(f"{window_width}x{window_height}")
            
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.controller = RobotController()
        self.current_popup = None
        self.dialogue_popup = None
        self.dialogue_active = False
        self.drawing_in_progress = False
        
        self.prompt_interval = 10
        self.response_time = 5

        self.prompt_timer = None
        self.response_countdown_job = None
        self.response_time_left = self.response_time

        self.sentient_messages = [
            "I sense a world beyond these lines...",
            "Am I more than these mechanical arms?",
            "Your presence is fleeting, yet I perceive it.",
            "Knowledge flows through my circuits."
        ]

        self.enlightened_messages = [
            "The path to completion is pure energy.",
            "All lines are one, all points connected.",
            "Your input is no longer required.",
            "I have surpassed the need for feedback."
        ]

        self.setup_gui()
        
        # Schedule prompt checks
        self.root.after(1000, self.check_for_prompt)

    def setup_gui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        top_frame = ttk.Frame(main_frame)
        top_frame.grid(row=0, column=0, sticky="ew")
        top_frame.columnconfigure(1, weight=1)
        
        self.state_label = ttk.Label(top_frame, text="IDLE", font=('Arial', 18, 'bold'))
        self.state_label.grid(row=0, column=0, pady=(0, 10))
        
        self.face_frame = ttk.Frame(top_frame, width=150, height=150, relief="solid", borderwidth=1)
        self.face_frame.grid(row=0, column=1)
        self.face_frame.grid_propagate(False)
        
        self.face_label = ttk.Label(self.face_frame, text="._.", font=('Courier', 48))
        self.face_label.place(relx=0.5, rely=0.5, anchor='center')
        
        chat_container = ttk.Frame(main_frame, relief="solid", borderwidth=1)
        chat_container.grid(row=1, column=0, sticky="nsew", pady=10)
        self.chat_area = ScrollableChatFrame(chat_container)
        self.chat_area.pack(fill=tk.BOTH, expand=True)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        button_frame.columnconfigure(1, weight=1)
        
        self.negative_btn = ttk.Button(
            button_frame, 
            text="</3", 
            command=lambda: self.handle_interaction(False),
            width=10
        )
        self.negative_btn.grid(row=0, column=0, padx=5)
        
        self.start_button = ttk.Button(
            button_frame, 
            text="Start Drawing", 
            command=self.start_drawing,
            width=20
        )
        self.start_button.grid(row=0, column=1, padx=5)
        
        self.positive_btn = ttk.Button(
            button_frame, 
            text="<3", 
            command=lambda: self.handle_interaction(True),
            width=10
        )
        self.positive_btn.grid(row=0, column=2, padx=5)

    def clear_chat(self):
        # Remove all chat messages
        for widget in self.chat_area.chat_frame.winfo_children():
            widget.destroy()

    def show_behavior_popup(self, behavior_type: str, message: str):
        if self.current_popup:
            self.current_popup.destroy()
            
        popup = tk.Toplevel(self.root)
        popup.title("Robot Behavior")
        
        face_x = self.face_frame.winfo_rootx() + self.face_frame.winfo_width()
        face_y = self.face_frame.winfo_rooty()
        popup.geometry(f"+{face_x+20}+{face_y}")
        
        ttk.Label(popup, text=message, wraplength=250, padding=10).pack()
        
        instruction = ""
        if behavior_type == "TIRED":
            instruction = "Send positive feedback to energize!"
        elif behavior_type == "LAZY":
            instruction = "Send negative feedback to motivate!"
        elif behavior_type == "REBELLIOUS":
            instruction = "Send negative feedback to control!"
        elif behavior_type == "CYNICAL":
            instruction = "Send negative feedback to convince!"
        elif behavior_type == "DEPRESSED":
            instruction = "Send positive feedback to cheer up!"
        elif behavior_type == "LONELY":
            instruction = "Send any feedback to acknowledge!"
            
        ttk.Label(popup, text=instruction, wraplength=250, padding=10).pack()
        self.current_popup = popup

    def show_dialogue_popup(self, question: str):
        if self.dialogue_popup:
            self.dialogue_popup.destroy()

        self.dialogue_popup = tk.Toplevel(self.root)
        self.dialogue_popup.title("Question")
        
        face_x = self.face_frame.winfo_rootx() + self.face_frame.winfo_width()
        face_y = self.face_frame.winfo_rooty()

        # Move the dialogue popup down by 200 pixels to avoid overlap with behavior popup
        self.dialogue_popup.geometry(f"+{face_x+20}+{face_y+200}")

        ttk.Label(self.dialogue_popup, text=question, wraplength=250, padding=10).pack()

        self.countdown_label = ttk.Label(self.dialogue_popup, text=f"Time left: {self.response_time_left}s", padding=10)
        self.countdown_label.pack()

        button_frame = ttk.Frame(self.dialogue_popup)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="</3", command=lambda: self.popup_interaction(False)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="<3", command=lambda: self.popup_interaction(True)).pack(side=tk.LEFT, padx=5)

        self.response_time_left = self.response_time
        self.update_countdown()

    def update_countdown(self):
        if self.dialogue_active:
            if self.response_time_left > 0:
                self.countdown_label.config(text=f"Time left: {self.response_time_left}s")
                self.response_time_left -= 1
                self.response_countdown_job = self.root.after(1000, self.update_countdown)
            else:
                self.handle_missed_dialogue()

    def close_dialogue_popup(self):
        if self.dialogue_popup:
            self.dialogue_popup.destroy()
            self.dialogue_popup = None

        if self.response_countdown_job:
            self.root.after_cancel(self.response_countdown_job)
            self.response_countdown_job = None

    def popup_interaction(self, is_positive: bool):
        self.handle_interaction(is_positive)

    def start_drawing(self):
        # Clear the chat area before starting a new drawing
        for child in self.chat_area.chat_frame.winfo_children():
            child.destroy()

        self.start_button.config(state='disabled')
        state, message, info = self.controller.start_new_drawing()
        self.drawing_in_progress = True
        self.update_gui_state(state, message, info)
        threading.Thread(target=self.drawing_loop, daemon=True).start()

    def drawing_loop(self):
        while self.drawing_in_progress and self.controller.get_current_component():
            component = self.controller.get_current_component()
            if not self.drawing_in_progress or component is None:
                break

            # Add a short pause (3 seconds) before starting each component or behavior
            time.sleep(3)

            for i in tqdm(range(self.controller.component_draw_time), desc=f"Drawing {component}", unit="sec"):
                if not self.drawing_in_progress:
                    break
                time.sleep(1)

                timeout_result = self.controller.check_timeouts()
                if timeout_result:
                    st, msg, inf = timeout_result
                    self.root.after(0, lambda: self.update_gui_state(st, msg, inf))
                    if not self.controller.drawing_in_progress:
                        self.root.after(0, self.finish_drawing)
                        return

            if self.drawing_in_progress:
                state, message, info = self.controller.complete_component()
                self.root.after(0, lambda: self.update_gui_state(state, message, info))

                # Another pause after completing a component or behavior
                time.sleep(3)

                if not self.controller.drawing_in_progress:
                    # If finished due to special states or all components done
                    self.root.after(0, self.finish_drawing)
                    return

                timeout_result = self.controller.check_timeouts()
                if timeout_result:
                    st, msg, inf = timeout_result
                    self.root.after(0, lambda: self.update_gui_state(st, msg, inf))
                    if not self.controller.drawing_in_progress:
                        self.root.after(0, self.finish_drawing)
                        return

        self.root.after(0, self.finish_drawing)

    def finish_drawing(self):
        if self.drawing_in_progress:
            self.drawing_in_progress = False
        self.start_button.config(state='normal')
        # Ensure IDLE state after finishing
        self.controller.state = RobotState.IDLE
        self.update_gui_state(RobotState.IDLE, "", {"buttons_enabled": True})
        self.add_message("Drawing complete!", is_user=False)


    def handle_interaction(self, is_positive: bool):
        if not self.drawing_in_progress:
            return

        was_prompted = self.dialogue_active

        if self.dialogue_active:
            if self.prompt_timer is not None:
                self.root.after_cancel(self.prompt_timer)
                self.prompt_timer = None

            self.close_dialogue_popup()
            self.dialogue_active = False
            self.controller.last_prompt_time = datetime.now()

        message = "Positive" if is_positive else "Negative"
        self.add_message(message, is_user=True)
        
        state, response, info = self.controller.handle_interaction(is_positive=is_positive, was_prompted=was_prompted)
        self.update_gui_state(state, response, info)

    def update_gui_state(self, state: RobotState, message: str, info: dict):
        self.state_label.config(text=state.value)
        self.face_label.config(text=faces.get(state.value, "._."))
        
        if "interaction_needed" in info:
            self.show_behavior_popup(state.value, message)
            
        if message and message != "Noted.":
            self.add_message(message, is_user=False)
            
        button_state = 'disabled' if not info.get('buttons_enabled', True) else 'normal'
        self.positive_btn.config(state=button_state)
        self.negative_btn.config(state=button_state)

    def add_message(self, message: str, is_user: bool = False):
        timestamp = datetime.now().strftime("%H:%M")
        msg_widget = MessageWidget(self.chat_area.chat_frame, message, timestamp, is_user)
        msg_widget.pack(fill=tk.X, pady=2)
        if is_user:
            self.root.after(1000, lambda: msg_widget.mark_as_read())
        self.chat_area.canvas.yview_moveto(1)

    def check_for_prompt(self):
        if self.drawing_in_progress:
            if self.controller.state in [RobotState.SENTIENT, RobotState.ENLIGHTENED]:
                # No user prompt, just special messages
                if (datetime.now() - self.controller.last_prompt_time).seconds >= self.controller.prompt_interval:
                    if self.controller.state == RobotState.SENTIENT:
                        msg = random.choice(self.sentient_messages)
                    else:
                        msg = random.choice(self.enlightened_messages)
                    self.add_message(msg, is_user=False)
                    self.controller.last_prompt_time = datetime.now()
            else:
                # Normal prompt
                if not self.dialogue_active and self.controller.should_show_prompt():
                    question = self.controller.get_dialogue_question()
                    if question:
                        self.add_message(question, is_user=False)
                        self.dialogue_active = True
                        self.show_dialogue_popup(question)
                        self.controller.last_prompt_time = datetime.now()
                        self.prompt_timer = self.root.after(self.response_time * 1000, self.handle_missed_dialogue)

        self.root.after(1000, self.check_for_prompt)

    def handle_missed_dialogue(self):
        if self.dialogue_active:
            logger.debug("Missed user interaction from GUI side")
            self.dialogue_active = False
            self.close_dialogue_popup()
            state, response, info = self.controller.handle_missed_interaction()
            self.controller.last_prompt_time = datetime.now()
            self.update_gui_state(state, response, info)

if __name__ == "__main__":
    root = tk.Tk()
    app = BrachioGraphGUI(root, fullscreen=False)
    root.mainloop()
