import tkinter as tk
from core.components import ModernButton, GlassCard

class GlobalSettingsPage:
    def __init__(self, parent_frame, colors, lang_manager, browse_path_cmd):
        self.parent_frame = parent_frame
        self.colors = colors
        self.lang = lang_manager
        self.browse_path_cmd = browse_path_cmd
        self.theme_var = tk.StringVar()
        self.behavior_vars = {}
        self.path_vars = {}

    def create_ui(self):
        # Page header
        header = tk.Frame(self.parent_frame, bg=self.colors['background'])
        header.pack(fill=tk.X, pady=(0, 30))
        
        title = tk.Label(header, text=self.lang.get_text("page_global_settings_title"), font=("Segoe UI", 28, "bold"),
                         bg=self.colors['background'], fg=self.colors['text_primary'])
        title.pack(anchor="w")
        
        subtitle = tk.Label(header, text=self.lang.get_text("page_global_settings_subtitle"),
                            font=("Segoe UI", 14), bg=self.colors['background'], 
                            fg=self.colors['text_secondary'])
        subtitle.pack(anchor="w", pady=(5, 0))
        
        self._create_global_settings_cards()
        
    def _create_global_settings_cards(self):
        """Create global settings cards"""
        grid = tk.Frame(self.parent_frame, bg=self.colors['background'])
        grid.pack(fill=tk.BOTH, expand=True)
        grid.grid_columnconfigure(0, weight=1)
        grid.grid_columnconfigure(1, weight=1)
        
        # Appearance card
        appearance_card = GlassCard(grid, title=self.lang.get_text("card_appearance_title"), subtitle=self.lang.get_text("card_appearance_subtitle"), colors=self.colors)
        appearance_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=(0, 20))
        
        appearance_content = tk.Frame(appearance_card, bg="white")
        appearance_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 25))
        
        # Theme selection
        tk.Label(appearance_content, text=self.lang.get_text("theme_label"), font=("Segoe UI", 12, "bold"),
                 bg="white", fg=self.colors['text_primary']).pack(anchor="w", pady=(10, 5))
        
        self.theme_var.set("light") # Default value
        theme_frame = tk.Frame(appearance_content, bg="white")
        theme_frame.pack(anchor="w", padx=(20, 0))
        
        for value, text_key in [("light", "theme_light"), ("dark", "theme_dark"), ("auto", "theme_auto")]:
            rb = tk.Radiobutton(theme_frame, text=self.lang.get_text(text_key), 
                                variable=self.theme_var, value=value,
                                font=("Segoe UI", 10), bg="white",
                                fg=self.colors['text_secondary'])
            rb.pack(anchor="w", pady=2)
            
        # Behavior card
        behavior_card = GlassCard(grid, title=self.lang.get_text("card_behavior_title"), subtitle=self.lang.get_text("card_behavior_subtitle"), colors=self.colors)
        behavior_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=(0, 20))
        
        behavior_content = tk.Frame(behavior_card, bg="white")
        behavior_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 25))
        
        # Behavior options
        behavior_options = [
            (self.lang.get_text("behavior_auto_save"), "auto_save"),
            (self.lang.get_text("behavior_check_updates"), "check_updates"),
            (self.lang.get_text("behavior_notifications"), "notifications"),
            (self.lang.get_text("behavior_remember_size"), "remember_size")
        ]
        
        self.behavior_vars = {}
        for text_key, key in behavior_options:
            var = tk.BooleanVar(value=True)
            self.behavior_vars[key] = var
            cb = tk.Checkbutton(behavior_content, text=self.lang.get_text(text_key), variable=var,
                                 font=("Segoe UI", 11), bg="white",
                                 fg=self.colors['text_primary'])
            cb.pack(anchor="w", pady=(10, 5))
            
        # Paths card
        paths_card = GlassCard(grid, title=self.lang.get_text("card_default_paths_title"), subtitle=self.lang.get_text("card_default_paths_subtitle"), colors=self.colors)
        paths_card.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        
        paths_content = tk.Frame(paths_card, bg="white")
        paths_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 25))
        
        # Default paths
        path_items = [
            (self.lang.get_text("path_output_dir_label"), "output_dir"),
            (self.lang.get_text("path_temp_dir_label"), "temp_dir"),
            (self.lang.get_text("path_projects_dir_label"), "projects_dir")
        ]
        
        self.path_vars = {}
        for label_key, key in path_items:
            frame = tk.Frame(paths_content, bg="white")
            frame.pack(fill=tk.X, pady=10)
            
            tk.Label(frame, text=self.lang.get_text(label_key), font=("Segoe UI", 11, "bold"),
                     bg="white", fg=self.colors['text_primary']).pack(anchor="w")
            
            path_frame = tk.Frame(frame, bg="white")
            path_frame.pack(fill=tk.X, pady=(5, 0))
            
            var = tk.StringVar(value=f"C:/Users/Default/{key}")
            self.path_vars[key] = var
            
            entry = tk.Entry(path_frame, textvariable=var, font=("Segoe UI", 10),
                             relief="solid", bd=1, width=50)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            browse_btn = ModernButton(path_frame, text=self.lang.get_text("browse_button_symbol"), command=lambda k=key: self.browse_path_cmd(k),
                                      bg_color="#6b7280", hover_color="#4b5563", padding=(10, 5))
            browse_btn.pack(side=tk.RIGHT, padx=(10, 0))
