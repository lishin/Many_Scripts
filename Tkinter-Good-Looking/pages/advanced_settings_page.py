import tkinter as tk
from tkinter import ttk
from core.components import GlassCard

class AdvancedSettingsPage:
    def __init__(self, parent_frame, colors, lang_manager):
        self.parent_frame = parent_frame
        self.colors = colors
        self.lang = lang_manager
        self.cores_var = tk.IntVar()
        self.memory_var = tk.DoubleVar()
        self.debug_vars = {}

    def create_ui(self):
        # Page header
        header = tk.Frame(self.parent_frame, bg=self.colors['background'])
        header.pack(fill=tk.X, pady=(0, 30))
        
        title = tk.Label(header, text=self.lang.get_text("page_advanced_settings_title"), font=("Segoe UI", 28, "bold"),
                         bg=self.colors['background'], fg=self.colors['text_primary'])
        title.pack(anchor="w")
        
        subtitle = tk.Label(header, text=self.lang.get_text("page_advanced_settings_subtitle"),
                            font=("Segoe UI", 14), bg=self.colors['background'], 
                            fg=self.colors['text_secondary'])
        subtitle.pack(anchor="w", pady=(5, 0))
        
        self._create_advanced_settings_cards()
        
    def _create_advanced_settings_cards(self):
        """Create advanced configuration cards"""
        grid = tk.Frame(self.parent_frame, bg=self.colors['background'])
        grid.pack(fill=tk.BOTH, expand=True)
        grid.grid_columnconfigure(0, weight=1)
        
        # Performance tuning card
        perf_card = GlassCard(grid, title=self.lang.get_text("card_perf_tuning_title"), 
                                     subtitle=self.lang.get_text("card_perf_tuning_subtitle"), colors=self.colors)
        perf_card.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        perf_content = tk.Frame(perf_card, bg="white")
        perf_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 25))
        
        # CPU cores slider
        cores_frame = tk.Frame(perf_content, bg="white")
        cores_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(cores_frame, text=self.lang.get_text("build_threads_label"), font=("Segoe UI", 12, "bold"),
                 bg="white", fg=self.colors['text_primary']).pack(anchor="w")
        
        self.cores_var.set(4) # Default value
        cores_scale = tk.Scale(cores_frame, from_=1, to=16, orient=tk.HORIZONTAL,
                               variable=self.cores_var, font=("Segoe UI", 10),
                               bg="white", fg=self.colors['text_secondary'],
                               highlightthickness=0, length=300)
        cores_scale.pack(anchor="w", pady=5)
        
        # Memory usage
        memory_frame = tk.Frame(perf_content, bg="white")
        memory_frame.pack(fill=tk.X, pady=15)
        
        tk.Label(memory_frame, text=self.lang.get_text("memory_limit_label"), font=("Segoe UI", 12, "bold"),
                 bg="white", fg=self.colors['text_primary']).pack(anchor="w")
        
        self.memory_var.set(2.0) # Default value
        memory_scale = tk.Scale(memory_frame, from_=0.5, to=8.0, resolution=0.5,
                                orient=tk.HORIZONTAL, variable=self.memory_var,
                                font=("Segoe UI", 10), bg="white", 
                                fg=self.colors['text_secondary'],
                                highlightthickness=0, length=300)
        memory_scale.pack(anchor="w", pady=5)
        
        # Debug options card
        debug_card = GlassCard(grid, title=self.lang.get_text("card_debug_logging_title"), 
                                      subtitle=self.lang.get_text("card_debug_logging_subtitle"), colors=self.colors)
        debug_card.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        
        debug_content = tk.Frame(debug_card, bg="white")
        debug_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 25))
        
        # Debug options
        debug_options = [
            (self.lang.get_text("debug_mode_checkbox"), "debug_mode"),
            (self.lang.get_text("verbose_output_checkbox"), "verbose"),
            (self.lang.get_text("show_progress_checkbox"), "show_progress"),
            (self.lang.get_text("generate_report_checkbox"), "generate_report")
        ]
        
        self.debug_vars = {}
        for text_key, key in debug_options:
            var = tk.BooleanVar(value=(key == "show_progress"))
            self.debug_vars[key] = var
            cb = tk.Checkbutton(debug_content, text=self.lang.get_text(text_key), variable=var,
                                 font=("Segoe UI", 11), bg="white",
                                 fg=self.colors['text_primary'])
            cb.pack(anchor="w", pady=5)
