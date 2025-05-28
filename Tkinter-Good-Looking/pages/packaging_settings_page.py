import tkinter as tk
from tkinter import ttk
from core.components import GlassCard

class PackagingSettingsPage:
    def __init__(self, parent_frame, colors, lang_manager):
        self.parent_frame = parent_frame
        self.colors = colors
        self.lang = lang_manager
        self.single_file_var = tk.BooleanVar()
        self.console_var = tk.BooleanVar()
        self.optimization_var = tk.StringVar()
        self.threading_var = tk.BooleanVar()
        self.plugin_vars = {}
        self.output_name_var = tk.StringVar()

    def create_ui(self):
        # Page header
        header = tk.Frame(self.parent_frame, bg=self.colors['background'])
        header.pack(fill=tk.X, pady=(0, 30))
        
        title = tk.Label(header, text=self.lang.get_text("page_packaging_settings_title"), font=("Segoe UI", 28, "bold"),
                         bg=self.colors['background'], fg=self.colors['text_primary'])
        title.pack(anchor="w")
        
        subtitle = tk.Label(header, text=self.lang.get_text("page_packaging_settings_subtitle"),
                            font=("Segoe UI", 14), bg=self.colors['background'], 
                            fg=self.colors['text_secondary'])
        subtitle.pack(anchor="w", pady=(5, 0))
        
        self._create_packaging_settings_cards()
        
    def _create_packaging_settings_cards(self):
        """Create packaging configuration cards"""
        grid = tk.Frame(self.parent_frame, bg=self.colors['background'])
        grid.pack(fill=tk.BOTH, expand=True)
        grid.grid_columnconfigure(0, weight=1)
        grid.grid_columnconfigure(1, weight=1)
        
        # Basic options card
        basic_card = GlassCard(grid, title=self.lang.get_text("card_basic_options_title"), subtitle=self.lang.get_text("card_basic_options_subtitle"))
        basic_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=(0, 20))
        
        basic_content = tk.Frame(basic_card, bg="white")
        basic_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 25))
        
        # Single file option
        self.single_file_var.set(True) # Default value
        single_file_cb = tk.Checkbutton(basic_content, text=self.lang.get_text("single_executable_checkbox"), 
                                        variable=self.single_file_var, font=("Segoe UI", 12),
                                        bg="white", fg=self.colors['text_primary'])
        single_file_cb.pack(anchor="w", pady=(10, 5))
        
        single_file_desc = tk.Label(basic_content, text=self.lang.get_text("single_executable_desc"),
                                    font=("Segoe UI", 10), bg="white", 
                                    fg=self.colors['text_secondary'])
        single_file_desc.pack(anchor="w", padx=(25, 0), pady=(0, 15))
        
        # Console window option
        self.console_var.set(False) # Default value
        console_cb = tk.Checkbutton(basic_content, text=self.lang.get_text("show_console_checkbox"), 
                                    variable=self.console_var, font=("Segoe UI", 12),
                                    bg="white", fg=self.colors['text_primary'])
        console_cb.pack(anchor="w", pady=5)
        
        console_desc = tk.Label(basic_content, text=self.lang.get_text("show_console_desc"),
                                font=("Segoe UI", 10), bg="white", 
                                fg=self.colors['text_secondary'])
        console_desc.pack(anchor="w", padx=(25, 0), pady=(0, 15))
        
        # Optimization level
        tk.Label(basic_content, text=self.lang.get_text("optimization_level_label"), font=("Segoe UI", 12, "bold"),
                 bg="white", fg=self.colors['text_primary']).pack(anchor="w", pady=(10, 5))
        
        self.optimization_var.set("balanced") # Default value
        opt_frame = tk.Frame(basic_content, bg="white")
        opt_frame.pack(anchor="w", padx=(25, 0))
        
        for value, text_key in [("fast", "opt_fast_build"), ("balanced", "opt_balanced"), ("size", "opt_smaller_size")]:
            rb = tk.Radiobutton(opt_frame, text=self.lang.get_text(text_key), variable=self.optimization_var, 
                                value=value, font=("Segoe UI", 10), bg="white",
                                fg=self.colors['text_secondary'])
            rb.pack(anchor="w", pady=2)
            
        # Advanced options card
        advanced_card = GlassCard(grid, title=self.lang.get_text("card_advanced_options_title"), subtitle=self.lang.get_text("card_advanced_options_subtitle"))
        advanced_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=(0, 20))
        
        advanced_content = tk.Frame(advanced_card, bg="white")
        advanced_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 25))
        
        # Threading option
        self.threading_var.set(True) # Default value
        threading_cb = tk.Checkbutton(advanced_content, text=self.lang.get_text("enable_threading_checkbox"), 
                                      variable=self.threading_var, font=("Segoe UI", 12),
                                      bg="white", fg=self.colors['text_primary'])
        threading_cb.pack(anchor="w", pady=(10, 5))
        
        # Plugin selection
        tk.Label(advanced_content, text=self.lang.get_text("plugins_label"), font=("Segoe UI", 12, "bold"),
                 bg="white", fg=self.colors['text_primary']).pack(anchor="w", pady=(15, 5))
        
        plugins = ["numpy", "scipy", "matplotlib", "tkinter", "qt-plugins"]
        self.plugin_vars = {}
        
        for plugin in plugins:
            var = tk.BooleanVar()
            self.plugin_vars[plugin] = var
            cb = tk.Checkbutton(advanced_content, text=plugin, variable=var,
                                 font=("Segoe UI", 10), bg="white", 
                                 fg=self.colors['text_secondary'])
            cb.pack(anchor="w", padx=(25, 0), pady=2)
            
        # Output naming card
        naming_card = GlassCard(grid, title=self.lang.get_text("card_output_config_title"), subtitle=self.lang.get_text("card_output_config_subtitle"))
        naming_card.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        
        naming_content = tk.Frame(naming_card, bg="white")
        naming_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 25))
        
        # Output name
        name_frame = tk.Frame(naming_content, bg="white")
        name_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(name_frame, text=self.lang.get_text("output_name_label"), font=("Segoe UI", 12, "bold"),
                 bg="white", fg=self.colors['text_primary']).pack(side=tk.LEFT)
        
        self.output_name_var.set("MyApplication") # Default value
        name_entry = tk.Entry(name_frame, textvariable=self.output_name_var, 
                              font=("Segoe UI", 11), width=30, relief="solid", bd=1)
        name_entry.pack(side=tk.LEFT, padx=(10, 0))