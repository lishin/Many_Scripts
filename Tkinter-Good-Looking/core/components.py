import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw, ImageFilter
import math

class ModernButton(tk.Frame):
    def __init__(self, parent, text, command=None, bg_color="#00a89d", hover_color="#008a7a", 
                 text_color="white", font=("Segoe UI", 12), padding=(20, 12), **kwargs):
        super().__init__(parent, **kwargs)
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.padding = padding
        
        self.button = tk.Label(self, text=text, font=font, bg=bg_color, fg=text_color,
                               cursor="hand2", padx=padding[0], pady=padding[1])
        self.button.pack(fill=tk.BOTH, expand=True)
        
        self.button.bind("<Button-1>", self._on_click)
        self.button.bind("<Enter>", self._on_enter)
        self.button.bind("<Leave>", self._on_leave)
        
        self.configure(bg=bg_color)
        
    def _on_click(self, event):
        if self.command:
            self.command()
            
    def _on_enter(self, event):
        self.button.configure(bg=self.hover_color)
        self.configure(bg=self.hover_color)
        
    def _on_leave(self, event):
        self.button.configure(bg=self.bg_color)
        self.configure(bg=self.bg_color)

class AnimatedProgress(tk.Frame):
    def __init__(self, parent, width=400, height=8, bg_color="#e1e5e9", fill_color="#00a89d", **kwargs):
        super().__init__(parent, **kwargs)
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.fill_color = fill_color
        self.progress = 0
        
        self.canvas = tk.Canvas(self, width=width, height=height, highlightthickness=0)
        self.canvas.pack()
        
        self.bg_rect = self.canvas.create_rectangle(0, 0, width, height, fill=bg_color, outline="")
        self.progress_rect = self.canvas.create_rectangle(0, 0, 0, height, fill=fill_color, outline="")
        
    def set_progress(self, value):
        self.progress = max(0, min(100, value))
        progress_width = (self.progress / 100) * self.width
        self.canvas.coords(self.progress_rect, 0, 0, progress_width, self.height)
        self.update()

class GlassCard(tk.Frame):
    def __init__(self, parent, title="", subtitle="", colors=None, **kwargs):
        super().__init__(parent, bg="white", relief="flat", bd=0, **kwargs)
        self.configure(highlightbackground="#e1e5e9", highlightthickness=1)
        self.colors = colors

        if title or subtitle:
            # Card header
            header = tk.Frame(self, bg="white")
            header.pack(fill=tk.X, padx=30, pady=(25, 15))

            if title:
                title_label = tk.Label(header, text=title, font=("Segoe UI", 18, "bold"),
                                       bg="white", fg=self.colors.get('text_primary', 'black') if self.colors else 'black')
                title_label.pack(anchor="w")

            if subtitle:
                subtitle_label = tk.Label(header, text=subtitle, font=("Segoe UI", 11),
                                         bg="white", fg=self.colors.get('text_secondary', 'gray') if self.colors else 'gray')
                subtitle_label.pack(anchor="w", pady=(5, 0))
