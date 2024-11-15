import os
import sys
import threading
import time
import json

current_dir = os.path.dirname(os.path.abspath(__file__))
brachiograph_dir = os.path.join(os.path.dirname(current_dir), 'BrachioGraphCaricature')
sys.path.insert(0, brachiograph_dir)

from brachiograph import BrachioGraph

class Robot:
    def __init__(self):
        """Initialize the BrachioGraph robot"""
        try:
            self.bg = BrachioGraph(
                servo_1_parked_pw=1570,
                servo_2_parked_pw=1450,
                bounds=[-8, 4, 6, 13]  # Set the drawing bounds
            )
            self.is_drawing = False
            self.current_line = 0
            self.total_lines = 0
            print("Robot initialized successfully")
        except Exception as e:
            print(f"Error initializing robot: {e}")
            self.bg = None

    def draw(self, json_path, progress_callback=None):
        """Start drawing in a background thread"""
        if not self.is_drawing and self.bg:
            self.is_drawing = True
            
            def drawing_thread():
                try:
                    # Get total lines for progress tracking
                    with open(json_path, 'r') as f:
                        lines = json.load(f)
                        total_lines = len(lines)
                    
                    if progress_callback:
                        progress_callback(0)  # Start progress

                    # Store original method
                    original_plot_lines = self.bg.plot_lines
                    
                    # Create wrapper that adds progress tracking
                    def plot_lines_with_progress(*args, **kwargs):
                        lines = args[0]
                        for i, line in enumerate(lines):
                            # Draw the line using original logic for a single line
                            original_plot_lines([line], *args[1:], **kwargs)
                            # Update progress
                            if progress_callback:
                                progress = ((i + 1) / total_lines) * 100
                                progress_callback(progress)
                    
                    # Replace method temporarily
                    self.bg.plot_lines = plot_lines_with_progress
                    
                    # Plot the file
                    self.bg.plot_file(json_path)
                    
                    # Restore original method
                    self.bg.plot_lines = original_plot_lines
                    
                    self.is_drawing = False
                    
                except Exception as e:
                    print(f"Error during drawing: {e}")
                    self.is_drawing = False
                    if self.bg:
                        self.bg.park()

            # Start drawing thread
            thread = threading.Thread(target=drawing_thread)
            thread.daemon = True
            thread.start()