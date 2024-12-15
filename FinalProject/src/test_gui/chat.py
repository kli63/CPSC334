import tkinter as tk
from tkinter import ttk
from datetime import datetime
from tqdm import tqdm

class MessageWidget(ttk.Frame):
    def __init__(self, parent, message, timestamp, is_user=False, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Configure frame to expand horizontally
        self.pack_propagate(False)
        self.configure(height=50)  # Minimum height
        
        # Main message frame (no border)
        msg_frame = ttk.Frame(self)
        msg_frame.pack(side=tk.RIGHT if is_user else tk.LEFT, pady=2, padx=10)
        
        # Message background color
        if is_user:
            bg_color = '#e3f2fd'
            text = f"<3 {message}" if message == "Positive" else f"</3 {message}"
        else:
            bg_color = '#f5f5f5'
            text = message
            
        # Message container
        content_frame = ttk.Frame(msg_frame)
        content_frame.pack(padx=5, pady=5)
        
        # Message text
        content = tk.Label(
            content_frame,
            text=text,
            wraplength=300,
            justify=tk.LEFT,
            bg=bg_color,
            padx=10,
            pady=5
        )
        content.pack()
        
        # Info frame for timestamp and read receipt
        info_frame = ttk.Frame(msg_frame)
        info_frame.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        # Timestamp
        time_label = ttk.Label(
            info_frame,
            text=timestamp,
            font=('Arial', 8)
        )
        time_label.pack(side=tk.LEFT)
        
        # Read receipt (for user messages)
        if is_user:
            self.read_label = ttk.Label(
                info_frame,
                text="Delivered",  # Show "Delivered" right away
                font=('Arial', 8)
            )
            self.read_label.pack(side=tk.RIGHT)
    
    def mark_as_read(self):
        if hasattr(self, 'read_label'):
            current_time = datetime.now().strftime("%H:%M")
            self.read_label.config(text=f"Read {current_time}")

class ScrollableChatFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        # Create canvas with border
        self.canvas = tk.Canvas(self, highlightthickness=1, highlightbackground="gray")
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        
        # Create frame for messages
        self.chat_frame = ttk.Frame(self.canvas)
        self.chat_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        # Add inner frame to canvas
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.chat_frame, anchor="nw")
        
        # Configure canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Layout management
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Handle resize events
        self.canvas.bind('<Configure>', self.on_canvas_configure)
        
    def on_canvas_configure(self, event):
        # Update the width of canvas elements
        self.canvas.itemconfig(self.canvas_frame, width=event.width)
        # Scroll to bottom on resize
        self.canvas.yview_moveto(1)