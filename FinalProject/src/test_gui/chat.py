import tkinter as tk
from tkinter import ttk
from datetime import datetime

class MessageWidget(ttk.Frame):
    def __init__(self, parent, message, timestamp, is_user=False, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Configure base frame with larger height
        self.configure(height=80)  # Increased base height
        self.pack_propagate(False)
        
        # Container frame for message
        container = ttk.Frame(self)
        container.pack(
            side=tk.RIGHT if is_user else tk.LEFT,
            anchor=tk.E if is_user else tk.W,
            padx=30  # Increased side padding
        )
        
        # Message bubble
        bubble_frame = ttk.Frame(container)
        bubble_frame.pack(side=tk.TOP)
        
        # Background and text setup
        bg_color = '#e3f2fd' if is_user else '#f5f5f5'
        
        # Message content with background - larger text and padding
        self.content = tk.Label(
            bubble_frame,
            text=message,
            wraplength=600,  # Larger default wrap length
            justify=tk.LEFT,
            bg=bg_color,
            padx=20,  # Increased horizontal padding
            pady=15,  # Increased vertical padding
            relief="solid",
            borderwidth=1,
            font=('Arial', 12)  # Explicitly set larger font
        )
        self.content.pack(side=tk.TOP)
        
        # Read receipt only for user messages
        if is_user:
            self.read_label = ttk.Label(
                container,
                text="Delivered",
                font=('Arial', 9),  # Slightly larger font for receipt
                foreground='gray'
            )
            self.read_label.pack(pady=(4, 0))
            self.after(1500, self.mark_as_read)
    
    def mark_as_read(self):
        if hasattr(self, 'read_label'):
            current_time = datetime.now().strftime("%H:%M")
            self.read_label.configure(text=f"Read {current_time}")
    
    def set_wraplength(self, wraplength):
        # Set maximum width to 60% of window width
        new_wraplength = int(wraplength * 0.6)
        # Ensure minimum and maximum bounds
        new_wraplength = max(400, min(new_wraplength, 800))
        self.content.configure(wraplength=new_wraplength)


class ScrollableChatFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        # Create canvas with scrollbar
        self.canvas = tk.Canvas(self, highlightthickness=1, highlightbackground="gray")
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        
        # Create frame for messages
        self.chat_frame = ttk.Frame(self.canvas)
        
        # Add inner frame to canvas
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.chat_frame, anchor="nw")
        
        # Configure canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Layout management
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Bind events
        self.chat_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        
        # Bind mouse wheel events
        self.bind_all("<MouseWheel>", self._on_mousewheel)
        self.bind_all("<Button-4>", self._on_mousewheel)
        self.bind_all("<Button-5>", self._on_mousewheel)
        
        self.messages = []
        
    def _on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        width = self.canvas.winfo_width()
        self.canvas.itemconfig(self.canvas_frame, width=width)
        self.adjust_message_wrap()
        
    def _on_canvas_configure(self, event):
        width = event.width
        self.canvas.itemconfig(self.canvas_frame, width=width)
        self.adjust_message_wrap()
        
    def _on_mousewheel(self, event):
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")
        else:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def add_message(self, msg_widget):
        msg_widget.pack(fill=tk.X, pady=6)
        self.messages.append(msg_widget)
        
        # Update scroll region and scroll to bottom
        self.chat_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.yview_moveto(1.0)
        
    def adjust_message_wrap(self, event=None):
        width = self.chat_frame.winfo_width()
        for msg in self.messages:
            msg.set_wraplength(width)