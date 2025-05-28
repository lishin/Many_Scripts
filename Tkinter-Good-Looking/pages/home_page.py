import tkinter as tk
import os
from core.components import ModernButton, GlassCard

class HomePage:
    def __init__(self, parent_frame, colors, lang_manager, choose_file_cmd, choose_output_path_cmd, choose_icon_cmd, update_file_display_func):
        self.parent_frame = parent_frame
        self.colors = colors
        self.lang = lang_manager
        self.choose_file_cmd = choose_file_cmd
        self.choose_output_path_cmd = choose_output_path_cmd
        self.choose_icon_cmd = choose_icon_cmd
        self.update_file_display_func = update_file_display_func # Function to update file display in GUI_App
        
        self.file_info_frame = None
        self.output_display = None
        self.icon_preview = None

    def create_ui(self, selected_file, output_path, icon_path):
        # Page title
        title_frame = tk.Frame(self.parent_frame, bg=self.colors['background'])
        title_frame.pack(fill=tk.X, pady=(0, 30))
        
        page_title = tk.Label(title_frame, text=self.lang.get_text("page_home_title"), 
                              font=("Segoe UI", 28, "bold"), 
                              bg=self.colors['background'], fg=self.colors['text_primary'])
        page_title.pack(anchor="w")
        
        subtitle = tk.Label(title_frame, text=self.lang.get_text("page_home_subtitle"), 
                            font=("Segoe UI", 14), 
                            bg=self.colors['background'], fg=self.colors['text_secondary'])
        subtitle.pack(anchor="w", pady=(5, 0))
        
        # Main grid layout
        main_grid = tk.Frame(self.parent_frame, bg=self.colors['background'])
        main_grid.pack(fill=tk.BOTH, expand=True)
        main_grid.grid_columnconfigure(0, weight=1)
        main_grid.grid_columnconfigure(1, weight=1)
        main_grid.grid_rowconfigure(1, weight=1)
        
        # File selection card (full width)
        file_card = self._create_card(main_grid, self.lang.get_text("card_select_file_title"), 
                                     self.lang.get_text("card_select_file_subtitle"))
        file_card.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        
        file_content = tk.Frame(file_card, bg="white")
        file_content.pack(fill=tk.X, padx=30, pady=(0, 25))
        
        # Drag and drop area
        drop_area = tk.Frame(file_content, bg="#f8fafc", height=120, relief="solid", bd=2, 
                             highlightbackground="#d1d5db", highlightthickness=1)
        drop_area.pack(fill=tk.X, pady=10)
        drop_area.pack_propagate(False)
        
        drop_icon = tk.Label(drop_area, text="📁", font=("Segoe UI Emoji", 32),
                             bg="#f8fafc", fg=self.colors['primary'])
        drop_icon.pack(pady=(20, 5))
        
        drop_text = tk.Label(drop_area, text=self.lang.get_text("drag_drop_file_text"),
                             font=("Segoe UI", 12), bg="#f8fafc", fg=self.colors['text_secondary'])
        drop_text.pack()
        
        # File info display
        self.file_info_frame = tk.Frame(file_content, bg="white")
        self.file_info_frame.pack(fill=tk.X, pady=(10, 0))
        
        # If a file is already selected, display it
        if selected_file:
            self.update_file_display(selected_file)

        # Browse button
        browse_button = ModernButton(file_content, text=self.lang.get_text("btn_browse_files"), 
                                     command=self.choose_file_cmd, padding=(20, 10))
        browse_button.pack(pady=15)
        
        # Make drop area clickable
        for widget in [drop_area, drop_icon, drop_text]:
            widget.bind('<Button-1>', lambda e: self.choose_file_cmd())
            widget.configure(cursor="hand2")
            
        # Output path card
        output_card = self._create_card(main_grid, self.lang.get_text("card_output_dir_title"), 
                                       self.lang.get_text("card_output_dir_subtitle"))
        output_card.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        
        output_content = tk.Frame(output_card, bg="white")
        output_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 25))
        
        # Output path display
        self.output_display = tk.Label(output_content, text=self.lang.get_text("output_auto_selected"),
                                       font=("Segoe UI", 11), bg="white", 
                                       fg=self.colors['text_secondary'], anchor="w")
        self.output_display.pack(fill=tk.X, pady=(10, 15))

        # If output path is already set, display it
        if output_path:
            self.update_output_display(output_path)
        
        output_button = ModernButton(output_content, text=self.lang.get_text("btn_choose_directory"),
                                     command=self.choose_output_path_cmd, padding=(15, 8),
                                     bg_color="#6b7280", hover_color="#4b5563")
        output_button.pack(pady=10)
        
        # Icon settings card
        icon_card = self._create_card(main_grid, self.lang.get_text("card_app_icon_title"), 
                                     self.lang.get_text("card_app_icon_subtitle"))
        icon_card.grid(row=1, column=1, sticky="nsew", padx=(10, 0))
        
        icon_content = tk.Frame(icon_card, bg="white")
        icon_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 25))
        
        # Icon preview
        icon_preview_frame = tk.Frame(icon_content, bg="white")
        icon_preview_frame.pack(fill=tk.X, pady=(10, 15))
        
        self.icon_preview = tk.Label(icon_preview_frame, text="🚀", font=("Segoe UI Emoji", 48),
                                     bg="white", fg=self.colors['primary'])
        self.icon_preview.pack()
        
        icon_status = tk.Label(icon_preview_frame, text=self.lang.get_text("icon_default_status"),
                               font=("Segoe UI", 10), bg="white", 
                               fg=self.colors['text_secondary'])
        icon_status.pack(pady=(5, 0))

        # If icon path is already set, display it
        if icon_path:
            self.update_icon_preview(icon_path)
        
        icon_button = ModernButton(icon_content, text=self.lang.get_text("btn_choose_icon"),
                                   command=self.choose_icon_cmd, padding=(15, 8),
                                   bg_color="#6b7280", hover_color="#4b5563")
        icon_button.pack(pady=10)

    def _create_card(self, parent, title, subtitle="", height=None):
        # Pass the colors dictionary to GlassCard
        return GlassCard(parent, title=title, subtitle=subtitle, height=height, colors=self.colors)

    def update_file_display(self, filename):
        """Update file display in the UI"""
        basename = os.path.basename(filename)
        
        # Clear existing file info
        for widget in self.file_info_frame.winfo_children():
            widget.destroy()
            
        # Create new file info display
        info_frame = tk.Frame(self.file_info_frame, bg="#e8f5e8", relief="solid", bd=1)
        info_frame.pack(fill=tk.X, pady=10)
        
        file_icon = tk.Label(info_frame, text="✅", font=("Segoe UI Emoji", 16),
                             bg="#e8f5e8", fg=self.colors['success'])
        file_icon.pack(side=tk.LEFT, padx=15, pady=10)
        
        file_details = tk.Frame(info_frame, bg="#e8f5e8")
        file_details.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=10)
        
        name_label = tk.Label(file_details, text=f"{self.lang.get_text('file_info_selected')} {basename}",
                              font=("Segoe UI", 12, "bold"), bg="#e8f5e8",
                              fg=self.colors['text_primary'])
        name_label.pack(anchor="w")
        
        path_label = tk.Label(file_details, text=f"{self.lang.get_text('file_info_path')} {filename}",
                              font=("Segoe UI", 9), bg="#e8f5e8",
                              fg=self.colors['text_secondary'])
        path_label.pack(anchor="w")
        
    def update_output_display(self, directory):
        self.output_display.configure(text=f"📁 {directory}")
            
    def update_icon_preview(self, filename):
        try:
            # Open image using PIL
            img = Image.open(filename)
            img = img.resize((64, 64), Image.Resampling.LANCZOS) # Resize for preview
            self.icon_photo = ImageTk.PhotoImage(img)
            self.icon_preview.config(image=self.icon_photo, text="")
        except Exception as e:
            print(f"Could not load icon: {e}")
            self.icon_preview.configure(text="🎨") # Fallback to default emoji
