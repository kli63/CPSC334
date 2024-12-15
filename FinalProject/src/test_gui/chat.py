import tkinter as tk
from tkinter import ttk
from datetime import datetime

class MessageWidget(ttk.Frame):
    def __init__(self, parent, message, timestamp, is_user=False, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.configure(height=80) 
        self.pack_propagate(False)
        
        container = ttk.Frame(self)
        container.pack(
            side=tk.RIGHT if is_user else tk.LEFT,
            anchor=tk.E if is_user else tk.W,
            padx=30 
        )
        
        bubble_frame = ttk.Frame(container)
        bubble_frame.pack(side=tk.TOP)
        
        bg_color = '#e3f2fd' if is_user else '#f5f5f5'
        
        self.content = tk.Label(
            bubble_frame,
            text=message,
            wraplength=600,
            justify=tk.LEFT,
            bg=bg_color,
            padx=20,
            pady=15,
            relief="solid",
            borderwidth=1,
            font=('Arial', 12)
        )
        self.content.pack(side=tk.TOP)
        
        if is_user:
            self.read_label = ttk.Label(
                container,
                text="Delivered",
                font=('Arial', 9),
                foreground='gray'
            )
            self.read_label.pack(pady=(4, 0))
            self.after(1500, self.mark_as_read)
    
    def mark_as_read(self):
        if hasattr(self, 'read_label'):
            current_time = datetime.now().strftime("%H:%M")
            self.read_label.configure(text=f"Read {current_time}")
    
    def set_wraplength(self, wraplength):
        new_wraplength = int(wraplength * 0.6)
        new_wraplength = max(400, min(new_wraplength, 800))
        self.content.configure(wraplength=new_wraplength)


class ScrollableChatFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        self.canvas = tk.Canvas(self, highlightthickness=1, highlightbackground="gray")
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        
        self.chat_frame = ttk.Frame(self.canvas)
        
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.chat_frame, anchor="nw")
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        self.chat_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        
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
        
        self.chat_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.yview_moveto(1.0)
        
    def adjust_message_wrap(self, event=None):
        width = self.chat_frame.winfo_width()
        for msg in self.messages:
            msg.set_wraplength(width)