import tkinter as tk
from tkinter import ttk, filedialog
from core.components import ModernButton, GlassCard

class FileSettingsPage:
    def __init__(self, parent_frame, colors, lang_manager):
        self.parent_frame = parent_frame
        self.colors = colors
        self.lang = lang_manager
        self.include_listbox = None
        self.exclusion_vars = {}

    def create_ui(self):
        # Page header
        header = tk.Frame(self.parent_frame, bg=self.colors['background'])
        header.pack(fill=tk.X, pady=(0, 30))
        
        title = tk.Label(header, text=self.lang.get_text("page_file_settings_title"), font=("Segoe UI", 28, "bold"),
                         bg=self.colors['background'], fg=self.colors['text_primary'])
        title.pack(anchor="w")
        
        subtitle = tk.Label(header, text=self.lang.get_text("page_file_settings_subtitle"),
                            font=("Segoe UI", 14), bg=self.colors['background'], 
                            fg=self.colors['text_secondary'])
        subtitle.pack(anchor="w", pady=(5, 0))
        
        # Settings cards
        self._create_file_settings_cards()
        
    def _create_file_settings_cards(self):
        """Create file settings configuration cards"""
        grid = tk.Frame(self.parent_frame, bg=self.colors['background'])
        grid.pack(fill=tk.BOTH, expand=True)
        grid.grid_columnconfigure(0, weight=1)
        
        # Include files card
        include_card = GlassCard(grid, title=self.lang.get_text("card_include_files_title"),
                                         subtitle=self.lang.get_text("card_include_files_subtitle"), colors=self.colors)
        include_card.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        include_content = tk.Frame(include_card, bg="white")
        include_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 25))
        
        # File list with scrollbar
        list_frame = tk.Frame(include_content, bg="white")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.include_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set,
                                         font=("Segoe UI", 10), bg="#f8fafc",
                                         selectbackground=self.colors['primary'])
        self.include_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.include_listbox.yview)
        
        # Add/Remove buttons
        button_frame = tk.Frame(include_content, bg="white")
        button_frame.pack(fill=tk.X, pady=(15, 0))
        
        add_file_btn = ModernButton(button_frame, text=self.lang.get_text("btn_add_files"),
                                    command=self.add_include_files, padding=(15, 8),
                                    bg_color=self.colors['success'])
        add_file_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        add_dir_btn = ModernButton(button_frame, text=self.lang.get_text("btn_add_directory"),
                                    command=self.add_include_directory, padding=(15, 8),
                                    bg_color=self.colors['secondary'])
        add_dir_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        remove_btn = ModernButton(button_frame, text=self.lang.get_text("btn_remove"),
                                 command=self.remove_include_item, padding=(15, 8),
                                 bg_color=self.colors['error'])
        remove_btn.pack(side=tk.RIGHT)
        
        # Exclude patterns card
        exclude_card = GlassCard(grid, title=self.lang.get_text("card_exclude_patterns_title"),
                                         subtitle=self.lang.get_text("card_exclude_patterns_subtitle"), colors=self.colors)
        exclude_card.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        
        exclude_content = tk.Frame(exclude_card, bg="white")
        exclude_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 25))
        
        # Common exclusions with checkboxes
        common_frame = tk.Frame(exclude_content, bg="white")
        common_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(common_frame, text=self.lang.get_text("common_exclusions_label"), font=("Segoe UI", 12, "bold"),
                 bg="white", fg=self.colors['text_primary']).pack(anchor="w", pady=(0, 10))
        
        exclusions = [
            (self.lang.get_text("exclude_pycache"), "*.pyc, __pycache__/"),
            (self.lang.get_text("exclude_test_files"), "test_*, *_test.py"),
            (self.lang.get_text("exclude_documentation"), "*.md, docs/"),
            (self.lang.get_text("exclude_dev_tools"), ".git/, .vscode/")
        ]
        
        self.exclusion_vars = {}
        for name, pattern in exclusions:
            var = tk.BooleanVar(value=True)
            self.exclusion_vars[pattern] = var
            
            cb = tk.Checkbutton(common_frame, text=f"{name} ({pattern})",
                                 variable=var, font=("Segoe UI", 10),
                                 bg="white", fg=self.colors['text_secondary'])
            cb.pack(anchor="w", pady=2)

    def add_include_files(self):
        """Add files to include list"""
        files = filedialog.askopenfilenames(
            title=self.lang.get_text("select_files_to_include"), # Add to json
            filetypes=[(self.lang.get_text("file_types_all"), "*.*")]
        )
        
        for file in files:
            self.include_listbox.insert(tk.END, file)
            
    def add_include_directory(self):
        """Add directory to include list"""
        directory = filedialog.askdirectory(title=self.lang.get_text("select_directory_to_include")) # Add to json
        
        if directory:
            self.include_listbox.insert(tk.END, f"[DIR] {directory}")
            
    def remove_include_item(self):
        """Remove selected item from include list"""
        selection = self.include_listbox.curselection()
        if selection:
            self.include_listbox.delete(selection)
