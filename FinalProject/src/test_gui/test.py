import tkinter as tk
from tkinter import ttk
import threading
import time
import logging
from datetime import datetime
from robot_logic import RobotController, RobotState, DrawingComponent, DrawingBehavior
import argparse
from chat import MessageWidget, ScrollableChatFrame

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
        self.root.title("Creative BrachioGraph")
        self.fullscreen = fullscreen

        # Center the window
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

        self.setup_gui()
        self.show_initial_instructions()
        self.root.after(1000, self.check_behavior_timeout)

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
        """Show initial paper placement instructions."""
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
        while self.controller.drawing_in_progress:
            component = self.controller.get_current_component()
            if not component:
                break

            self.add_message(f"Drawing {component.value}", is_user=False)
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
                self.update_gui_state(st, msg, inf)

                if st in [RobotState.SENTIENT, RobotState.ENLIGHTENED]:
                    special_name = "Sentient" if st == RobotState.SENTIENT else "Enlightened"
                    self.add_message(f"Drawing {special_name}", is_user=False)
                    result = self.controller.execute_drawing_behavior()
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
                    self.add_message(f"Drawing {drawing_behavior.value} Behavior...", is_user=False)
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
                            self.update_gui_state(RobotState.IDLE, "No interaction, finishing drawing after behavior.", {"buttons_enabled": True})
                            return
                        else:
                            st2, msg2, inf2 = self.controller.complete_component()
                            self.update_gui_state(st2, msg2, inf2)
                            time.sleep(1)
                else:
                    pass

        self.update_gui_state(RobotState.IDLE, "Finished", {"buttons_enabled":True})

    def handle_interaction(self, is_positive: bool):
        if not self.controller.drawing_in_progress and self.controller.state not in [RobotState.SENTIENT, RobotState.ENLIGHTENED]:
            return

        message = "<3" if is_positive else "</3"
        self.add_message(message, is_user=True)

        st, msg, info = self.controller.handle_interaction(is_positive)
        self.update_gui_state(st, msg, info)

    def update_gui_state(self, state: RobotState, message: str, info: dict):
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

    def check_behavior_timeout(self):
        if self.controller.drawing_in_progress:
            timeout_result = self.controller.behavior_timeout_check()
            if timeout_result:
                st, msg, info = timeout_result
                self.update_gui_state(st, msg, info)
        self.root.after(1000, self.check_behavior_timeout)


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
