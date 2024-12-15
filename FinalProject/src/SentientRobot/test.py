import tkinter as tk
from tkinter import ttk
import threading
import time
import logging
from datetime import datetime
from robot_logic import RobotController, RobotState, DrawingComponent, DrawingBehavior
import argparse
from chat import MessageWidget, ScrollableChatFrame
from message import (
    get_behavior_instruction,
    get_random_component_message,
    get_random_signature_message,
    get_random_behavior_entry_message,
    get_random_behavior_drawing_message,
    get_behavior_timeout_message
)
from question_bank import get_random_question

logger = logging.getLogger("BrachioGraphGUI")

faces = {
    "HAPPY": "^_^",
    "TIRED": "-_-",
    "LAZY": "u_u",
    "REBELLIOUS": ">:)",
    "CYNICAL": "¬_¬",
    "DEPRESSED": "T_T",
    "LONELY": ";_;",
    "OVERSTIMULATED": "@_@",
    "SENTIENT": "O_O",
    "ENLIGHTENED": "☯",
    "IDLE": "._."
}

class BrachioGraphGUI:
    def __init__(self, root, fullscreen=False, debug=True):
        self.root = root
        self.root.title("Mechangelo d[o_0]b")
        self.fullscreen = fullscreen

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = int(screen_width * 0.9)
        window_height = int(screen_height * 0.9)
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        if fullscreen:
            self.root.attributes('-fullscreen', True)
        else:
            self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.controller = RobotController(debug=debug)
        self.draw_thread = None

        self.instruction_frame = None
        self.instruction_label = None
        self.dialogue_popup = None
        self.dialogue_timer_label = None
        self.dialogue_countdown = 0
        self.dialogue_question = ""
        self.dialogue_active = False

        self.setup_gui()
        self.show_initial_instructions()
        self.root.after(1000, self.check_behavior_timeout)
        self.root.after(1000, self.check_dialogue)

    def setup_gui(self):
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        top_frame = ttk.Frame(main_frame)
        top_frame.grid(row=0, column=0, sticky="ew")
        top_frame.columnconfigure(0, weight=1)

        top_inner_frame = ttk.Frame(top_frame)
        top_inner_frame.pack(fill='x', expand=True)

        left_frame = ttk.Frame(top_inner_frame)
        left_frame.pack(side='left', anchor='w')

        self.state_label = ttk.Label(left_frame, text="IDLE", font=('Arial', 18, 'bold'))
        self.state_label.pack(side='left', padx=(10,0))

        center_frame = ttk.Frame(top_inner_frame)
        center_frame.pack(side='left', expand=True)

        self.face_frame = ttk.Frame(center_frame, width=150, height=150, relief="solid", borderwidth=1)
        self.face_frame.pack(anchor='center')
        self.face_frame.grid_propagate(False)

        self.face_label = ttk.Label(self.face_frame, text="._.", font=('Courier', 48))
        self.face_label.place(relx=0.5, rely=0.5, anchor='center')

        self.instruction_frame = tk.Frame(top_inner_frame, bg=self.root.cget('bg'), highlightthickness=0, bd=0)
        self.instruction_frame.pack(side='right', padx=10, anchor='ne')

        self.instruction_label = tk.Label(self.instruction_frame, text="", font=('Arial', 12), justify='center', bg=self.root.cget('bg'))
        self.instruction_label.pack(padx=10, pady=10)

        chat_container = ttk.Frame(main_frame, relief="solid", borderwidth=1)
        chat_container.grid(row=1, column=0, sticky="nsew", pady=10)
        chat_container.rowconfigure(0, weight=1)
        chat_container.columnconfigure(0, weight=1)
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

    def add_message(self, message: str, is_user: bool = False):
        timestamp = datetime.now().strftime("%H:%M:%S") if is_user else ""
        msg_widget = MessageWidget(self.chat_area.chat_frame, message, timestamp, is_user)
        msg_widget.pack(fill=tk.X, pady=2)
        self.chat_area.add_message(msg_widget)
        self.chat_area.canvas.yview_moveto(1.0)

    def show_initial_instructions(self):
        self.add_message("Waiting to draw... let me help you place the paper!", is_user=False)
        self.add_message(
            "1. The arm holding the pen should run along the shorter side of the paper\n"
            "2. Place the top edge of paper about 3-4 inches above the pen\n"
            "3. Slide paper underneath so pen rests in the middle horizontally\n"
            "4. Press Start Drawing when ready!",
            is_user=False
        )

    def start_drawing(self):
        for child in self.chat_area.chat_frame.winfo_children():
            child.destroy()
        self.chat_area.messages.clear()

        state, message, info = self.controller.start_new_drawing()
        self.update_gui_state(state, message, info)

        self.draw_thread = threading.Thread(target=self.drawing_loop, daemon=True)
        self.draw_thread.start()

    def drawing_loop(self):
        if self.controller.state in [RobotState.SENTIENT, RobotState.ENLIGHTENED]:
            behavior_msg = get_random_behavior_drawing_message(self.controller.state.value)
            self.add_message(behavior_msg, is_user=False)
            self.controller.execute_drawing_behavior()
            self.controller.finish_drawing()
            self.update_gui_state(RobotState.IDLE, "Transcendence complete!", {"buttons_enabled": True})
            return
        
        while self.controller.drawing_in_progress:
            component = self.controller.get_current_component()
            if not component:
                break

            if component == DrawingComponent.SIGNATURE:
                comp_msg = get_random_signature_message()
            else:
                comp_msg = get_random_component_message(component.name)

            self.add_message(comp_msg, is_user=False)
            completed = self.controller.draw_component(component.value, self.controller.component_draw_time)
            if not completed:
                self.update_gui_state(RobotState.IDLE, "Drawing ended early.", {"buttons_enabled": True})
                return

            if component == DrawingComponent.SIGNATURE:
                self.controller.finish_drawing()
                self.update_gui_state(RobotState.IDLE, "Drawing complete!", {"buttons_enabled": True})
                return
            else:
                st, msg, inf = self.controller.next_phase()
                if st in [
                    RobotState.TIRED, RobotState.LAZY, RobotState.REBELLIOUS,
                    RobotState.CYNICAL, RobotState.DEPRESSED, RobotState.LONELY
                ]:
                    behavior_entry_msg = get_random_behavior_entry_message(st.value)
                    if msg == f"Entering {st.value.lower()} state...":
                        msg = behavior_entry_msg

                self.update_gui_state(st, msg, inf)

                if st in [RobotState.SENTIENT, RobotState.ENLIGHTENED]:
                    special_name = st.value
                    behavior_msg = get_random_behavior_drawing_message(special_name)
                    self.add_message(behavior_msg, is_user=False)
                    self.controller.execute_drawing_behavior()
                    self.controller.finish_drawing()
                    self.update_gui_state(RobotState.IDLE, "Transcendence complete!", {"buttons_enabled": True})
                    return

                drawing_behavior = self.controller.get_drawing_behavior_for_state(st)

                if st in [RobotState.TIRED, RobotState.LAZY]:
                    start_wait = time.time()
                    while self.controller.drawing_in_progress and self.controller.state not in [RobotState.HAPPY, RobotState.IDLE]:
                        time.sleep(1)
                    if self.controller.state == RobotState.HAPPY:
                        st2, msg2, inf2 = self.controller.complete_component()
                        self.update_gui_state(st2, msg2, inf2)
                        time.sleep(1)

                elif drawing_behavior:
                    behavior_msg = get_random_behavior_drawing_message(st.value)
                    self.add_message(behavior_msg, is_user=False)

                    result = self.controller.execute_drawing_behavior()
                    if not result:
                        if self.controller.state == RobotState.HAPPY:
                            st2, msg2, inf2 = self.controller.complete_component()
                            self.update_gui_state(st2, msg2, inf2)
                            time.sleep(1)
                        else:
                            return
                    else:
                        if self.controller.behavior_active and not self.controller.behavior_resolved:
                            self.controller.finish_drawing()
                            timeout_msg = get_behavior_timeout_message(self.controller.state.value)
                            self.update_gui_state(RobotState.IDLE, timeout_msg, {"buttons_enabled": True})
                            return
                        else:
                            st2, msg2, inf2 = self.controller.complete_component()
                            self.update_gui_state(st2, msg2, inf2)
                            time.sleep(1)
                else:
                    pass

        self.update_gui_state(RobotState.IDLE, "Finished", {"buttons_enabled":True})

    def handle_interaction(self, is_positive: bool):
        message = "<3" if is_positive else "</3"
        self.add_message(message, is_user=True)

        st, msg, info = self.controller.handle_interaction(is_positive)
        if msg == "Noted.":
            pass

        self.update_gui_state(st, msg, info)

    def update_gui_state(self, state: RobotState, message: str, info: dict):
        if state == RobotState.IDLE or not self.controller.drawing_in_progress:
            if self.dialogue_active:
                self.close_dialogue_popup(no_response=False)

        previous_state = getattr(self, 'previous_state', None)
        self.previous_state = state

        self.state_label.config(text=state.value)
        self.face_label.config(text=faces.get(state.value, "._."))

        if message and message != "Noted.":
            self.add_message(message, is_user=False)

        if state == RobotState.IDLE and previous_state is not None:
            self.show_initial_instructions()

        button_state = 'disabled' if not info.get('buttons_enabled', True) else 'normal'
        self.positive_btn.config(state=button_state)
        self.negative_btn.config(state=button_state)
        self.start_button.config(state='disabled' if self.controller.drawing_in_progress else 'normal')

        self.update_behavior_popup()

    def update_behavior_popup(self):
        if not self.controller.behavior_active or not self.controller.drawing_in_progress:
            self.instruction_label.config(text="")
            return

        state = self.controller.state
        instruction = get_behavior_instruction(state.value)
        show_timer = state in [RobotState.TIRED, RobotState.LAZY]

        message = instruction
        if show_timer and self.controller.behavior_start_time and self.controller.behavior_timeout:
            elapsed = (datetime.now() - self.controller.behavior_start_time).total_seconds()
            remaining = int(self.controller.behavior_timeout - elapsed)
            if remaining < 0:
                remaining = 0
            message += f"\nTime left: {remaining}s"

        self.instruction_label.config(text=message)

    def check_behavior_timeout(self):
        if self.controller.drawing_in_progress:
            timeout_result = self.controller.behavior_timeout_check()
            if timeout_result:
                st, msg, info = timeout_result
                self.update_gui_state(st, msg, info)
        self.update_behavior_popup()
        self.root.after(1000, self.check_behavior_timeout)

    def check_dialogue(self):
        if self.controller.drawing_in_progress and not self.dialogue_active:
            if self.controller.should_ask_question():
                self.show_dialogue_popup()

        if self.dialogue_active:
            self.dialogue_countdown -= 1
            if self.dialogue_countdown <= 0:
                self.close_dialogue_popup(no_response=True)
            else:
                if self.dialogue_timer_label:
                    self.dialogue_timer_label.config(text=f"Time left: {self.dialogue_countdown}s")

        self.root.after(1000, self.check_dialogue)

    def show_dialogue_popup(self):
        if self.controller.state in [RobotState.SENTIENT, RobotState.ENLIGHTENED] or not self.controller.drawing_in_progress:
            return

        self.dialogue_active = True
        self.dialogue_popup = tk.Toplevel(self.root)
        self.dialogue_popup.overrideredirect(False)
        self.dialogue_popup.attributes('-topmost', True)
        self.dialogue_popup.title("Question")

        self.root.update_idletasks()
        face_x = self.face_frame.winfo_rootx()
        face_y = self.face_frame.winfo_rooty()

        popup_x = face_x
        popup_y = face_y + 200
        self.dialogue_popup.geometry(f"300x150+{popup_x}+{popup_y}")

        self.dialogue_question = get_random_question(self.controller.state)
        self.add_message(self.dialogue_question, is_user=False)
        q_label = tk.Label(self.dialogue_popup, text=self.dialogue_question, font=('Arial', 12), wraplength=280)
        q_label.pack(pady=10)

        self.dialogue_timer_label = tk.Label(self.dialogue_popup, text="", font=('Arial', 10))
        self.dialogue_timer_label.pack()

        button_frame = tk.Frame(self.dialogue_popup)
        button_frame.pack(pady=10)

        neg_btn = tk.Button(button_frame, text="</3", command=lambda: self.dialogue_answer(False))
        neg_btn.pack(side='left', padx=10)
        pos_btn = tk.Button(button_frame, text="<3", command=lambda: self.dialogue_answer(True))
        pos_btn.pack(side='left', padx=10)

        self.dialogue_countdown = self.controller.dialogue_response_timer
        self.update_dialogue_timer_display()

        self.controller.last_question_time = datetime.now()

    def update_dialogue_timer_display(self):
        if self.dialogue_active and self.dialogue_timer_label:
            self.dialogue_timer_label.config(text=f"Time left: {self.dialogue_countdown}s")

    def dialogue_answer(self, is_positive):
        if not self.dialogue_active:
            return
        self.controller.record_dialogue_interaction(is_positive)
        self.add_message("<3" if is_positive else "</3", is_user=True)

        self.close_dialogue_popup(no_response=False)

    def close_dialogue_popup(self, no_response=False):
        if not self.dialogue_active:
            return

        if no_response:
            self.add_message("No response...", is_user=False)
            self.controller.record_missed_dialogue()

        if self.dialogue_popup:
            self.dialogue_popup.destroy()
            self.dialogue_popup = None
        self.dialogue_active = False
        self.dialogue_timer_label = None
        self.dialogue_countdown = 0
        self.dialogue_question = ""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Creative BrachioGraph GUI.")
    parser.add_argument("--hardware", action="store_true", help="Run with the actual BrachioGraph hardware.")
    args = parser.parse_args()

    root = tk.Tk()
    style = ttk.Style(root)
    style.configure("UserMessage.TLabel", foreground="blue")
    style.configure("RobotMessage.TLabel", foreground="black")

    app = BrachioGraphGUI(root, fullscreen=False, debug=True)
    app.controller = RobotController(debug=True, hardware=args.hardware)
    root.mainloop()
