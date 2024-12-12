import pygame
import tkinter as tk
import os
from PIL import Image, ImageTk
import io

class PygameEmbed(tk.Frame):
    def __init__(self, parent, width, height):
        tk.Frame.__init__(self, parent, width=width, height=height)
        
        os.environ['SDL_WINDOWID'] = '0'
        
        self.screen = pygame.Surface((width, height))
        self.width = width
        self.height = height
        
        self.eye_blink = 0
        self.mouth_state = 0
        self.current_emotion = "HAPPY"
        
        self.pack_propagate(0)
        
        self.canvas = tk.Canvas(self, width=width, height=height)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        self.animation_loop()
    
    def pygame_surface_to_image(self, surface):
        # Convert pygame surface to bytes
        image_bytes = pygame.image.tostring(surface, 'RGB')
        
        # Create PIL image from bytes
        image = Image.frombytes('RGB', (self.width, self.height), image_bytes)
        
        # Convert PIL image to PhotoImage
        return ImageTk.PhotoImage(image)
    
    def draw_face(self):
        self.screen.fill((255, 255, 255))
        
        if self.current_emotion == "HAPPY":
            self.draw_happy_face()
        elif self.current_emotion == "LAZY":
            self.draw_lazy_face()
        elif self.current_emotion == "REBELLIOUS":
            self.draw_rebellious_face()
            
        # Convert Pygame surface to tkinter-compatible image
        photo_image = self.pygame_surface_to_image(self.screen)
        
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=photo_image, anchor=tk.NW)
        self.canvas.photo = photo_image  # Keep a reference!

    def draw_happy_face(self):
        eye_state = abs((self.eye_blink % 40) - 20) / 20
        pygame.draw.ellipse(self.screen, (0, 0, 0), (100, 100, 40, int(40 * eye_state)))
        pygame.draw.ellipse(self.screen, (0, 0, 0), (260, 100, 40, int(40 * eye_state)))
        
        mouth_state = abs((self.mouth_state % 60) - 30) / 30
        pygame.draw.arc(self.screen, (0, 0, 0), (120, 160, 160, 100), 0, 3.14, 3)

    def draw_lazy_face(self):
        pygame.draw.line(self.screen, (0, 0, 0), (100, 120), (140, 120), 3)
        pygame.draw.line(self.screen, (0, 0, 0), (260, 120), (300, 120), 3)
        pygame.draw.arc(self.screen, (0, 0, 0), (120, 180, 160, 80), 0.5, 2.64, 3)

    def draw_rebellious_face(self):
        pygame.draw.line(self.screen, (0, 0, 0), (100, 100), (140, 120), 3)
        pygame.draw.line(self.screen, (0, 0, 0), (100, 120), (140, 100), 3)
        pygame.draw.line(self.screen, (0, 0, 0), (260, 100), (300, 120), 3)
        pygame.draw.line(self.screen, (0, 0, 0), (260, 120), (300, 100), 3)
        pygame.draw.arc(self.screen, (0, 0, 0), (120, 180, 160, 80), 3.64, 5.78, 3)

    def animation_loop(self):
        self.eye_blink += 1
        self.mouth_state += 1
        self.draw_face()
        self.after(50, self.animation_loop)
    
    def set_emotion(self, emotion):
        self.current_emotion = emotion