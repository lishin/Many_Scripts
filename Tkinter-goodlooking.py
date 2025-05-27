import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import time
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
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg="white", relief="flat", bd=0, **kwargs)
        self.configure(highlightbackground="#e1e5e9", highlightthickness=1)

class PremiumNuitkaGUI:
    def __init__(self, master):
        self.master = master
        master.title("Nuitka Premium Studio")
        master.geometry("1400x900")
        master.minsize(1200, 800)
        master.configure(bg="#f8fafc")
        
        # Remove default window decorations
        master.overrideredirect(False)
        
        # State variables
        self.current_page = None
        self.selected_file = None
        self.output_path = None
        self.icon_path = None
        self.is_maximized = False
        self.animation_running = False
        
        self.setup_styles()
        self.create_custom_titlebar()
        self.create_sidebar()
        self.create_main_content_area()
        self.create_bottom_panel()
        
        # Initialize with home page
        self.show_home_page()
        
        # Bind window events
        master.bind('<Configure>', self.on_window_configure)
        
    def setup_styles(self):
        """Setup custom styles and colors"""
        self.colors = {
            'primary': '#00a89d',
            'primary_hover': '#008a7a',
            'secondary': '#6366f1',
            'accent': '#f59e0b',
            'success': '#10b981',
            'warning': '#f59e0b',
            'error': '#ef4444',
            'surface': '#ffffff',
            'background': '#f8fafc',
            'sidebar': '#1e293b',
            'sidebar_hover': '#334155',
            'text_primary': '#1f2937',
            'text_secondary': '#6b7280',
            'text_muted': '#9ca3af',
            'border': '#e5e7eb'
        }
        
        # Configure ttk styles
        style = ttk.Style()
        style.theme_use('clam')
        
    def create_custom_titlebar(self):
        """Create a modern custom title bar"""
        self.titlebar = tk.Frame(self.master, bg=self.colors['surface'], height=50)
        self.titlebar.pack(fill=tk.X)
        self.titlebar.pack_propagate(False)
        
        # Left side - Logo and title
        left_frame = tk.Frame(self.titlebar, bg=self.colors['surface'])
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20)
        
        # App icon
        icon_label = tk.Label(left_frame, text="🚀", font=("Segoe UI Emoji", 20), 
                              bg=self.colors['surface'])
        icon_label.pack(side=tk.LEFT, pady=12)
        
        # App title
        title_label = tk.Label(left_frame, text="Nuitka Premium Studio", 
                               font=("Segoe UI", 14, "bold"), 
                               bg=self.colors['surface'], fg=self.colors['text_primary'])
        title_label.pack(side=tk.LEFT, padx=(10, 0), pady=15)
        
        # Right side - Window controls
        controls_frame = tk.Frame(self.titlebar, bg=self.colors['surface'])
        controls_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Window control buttons with hover effects
        self.create_window_control("🗕", self.minimize_window, controls_frame)
        self.create_window_control("🗖", self.toggle_maximize, controls_frame)
        self.create_window_control("🗙", self.close_window, controls_frame, hover_color="#ef4444")
        
        # Make titlebar draggable
        self.titlebar.bind('<Button-1>', self.start_drag)
        self.titlebar.bind('<B1-Motion>', self.on_drag)
        title_label.bind('<Button-1>', self.start_drag)
        title_label.bind('<B1-Motion>', self.on_drag)
        
    def create_window_control(self, symbol, command, parent, hover_color="#e5e7eb"):
        control = tk.Label(parent, text=symbol, font=("Segoe UI", 12), 
                           bg=self.colors['surface'], fg=self.colors['text_secondary'],
                           width=3, height=2, cursor="hand2")
        control.pack(side=tk.RIGHT)
        control.bind('<Button-1>', command)
        control.bind('<Enter>', lambda e: control.configure(bg=hover_color))
        control.bind('<Leave>', lambda e: control.configure(bg=self.colors['surface']))
        
    def start_drag(self, event):
        self.drag_start_x = event.x_root
        self.drag_start_y = event.y_root
        
    def on_drag(self, event):
        x = self.master.winfo_x() + (event.x_root - self.drag_start_x)
        y = self.master.winfo_y() + (event.y_root - self.drag_start_y)
        self.master.geometry(f"+{x}+{y}")
        self.drag_start_x = event.x_root
        self.drag_start_y = event.y_root
        
    def minimize_window(self, event=None):
        self.master.iconify()
        
    def toggle_maximize(self, event=None):
        if self.is_maximized:
            self.master.state('normal')
        else:
            self.master.state('zoomed')
        self.is_maximized = not self.is_maximized
        
    def close_window(self, event=None):
        self.master.quit()
        
    def create_sidebar(self):
        """Create an elegant sidebar with smooth animations"""
        self.sidebar = tk.Frame(self.master, bg=self.colors['sidebar'], width=280)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        
        # Sidebar header
        header_frame = tk.Frame(self.sidebar, bg=self.colors['sidebar'], height=80)
        header_frame.pack(fill=tk.X, pady=(20, 30))
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(header_frame, text="Navigation", 
                               font=("Segoe UI", 16, "bold"), 
                               bg=self.colors['sidebar'], fg="white")
        header_label.pack(pady=20)
        
        # Navigation items
        nav_items = [
            ("🏠", "Home", self.show_home_page),
            ("📁", "File Settings", self.show_file_settings_page),
            ("⚙️", "Packaging", self.show_packaging_settings_page),
            ("🔧", "Advanced", self.show_advanced_settings_page),
            ("📊", "Statistics", self.show_statistics_page),
            ("ℹ️", "About", self.show_about_page),
        ]
        
        self.nav_buttons = []
        self.active_nav_button = None
        
        for icon, text, command in nav_items:
            self.create_nav_button(icon, text, command)
            
        # Bottom section
        bottom_frame = tk.Frame(self.sidebar, bg=self.colors['sidebar'])
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)
        
        self.create_nav_button("⚙️", "Global Settings", self.show_global_settings_page, bottom_frame)
        
    def create_nav_button(self, icon, text, command, parent=None):
        if parent is None:
            parent = self.sidebar
            
        button_frame = tk.Frame(parent, bg=self.colors['sidebar'], cursor="hand2", height=50)
        button_frame.pack(fill=tk.X, padx=15, pady=2)
        button_frame.pack_propagate(False)
        
        # Icon
        icon_label = tk.Label(button_frame, text=icon, font=("Segoe UI Emoji", 16),
                              bg=self.colors['sidebar'], fg="#94a3b8", width=3)
        icon_label.pack(side=tk.LEFT, padx=(15, 10), pady=12)
        
        # Text
        text_label = tk.Label(button_frame, text=text, font=("Segoe UI", 12),
                              bg=self.colors['sidebar'], fg="#94a3b8", anchor="w")
        text_label.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=12)
        
        # Bind events
        for widget in [button_frame, icon_label, text_label]:
            widget.bind('<Button-1>', lambda e, cmd=command, btn=button_frame: self.on_nav_click(cmd, btn))
            widget.bind('<Enter>', lambda e, btn=button_frame: self.on_nav_hover(btn, True))
            widget.bind('<Leave>', lambda e, btn=button_frame: self.on_nav_hover(btn, False))
            
        self.nav_buttons.append((button_frame, icon_label, text_label))
        
        # Set first button as active
        if len(self.nav_buttons) == 1:
            self.set_active_nav_button(button_frame)
            
    def on_nav_click(self, command, button_frame):
        self.set_active_nav_button(button_frame)
        command()
        
    def set_active_nav_button(self, active_button):
        # Reset all buttons
        for button_frame, icon_label, text_label in self.nav_buttons:
            button_frame.configure(bg=self.colors['sidebar'])
            icon_label.configure(bg=self.colors['sidebar'], fg="#94a3b8")
            text_label.configure(bg=self.colors['sidebar'], fg="#94a3b8")
            
        # Set active button
        for button_frame, icon_label, text_label in self.nav_buttons:
            if button_frame == active_button:
                button_frame.configure(bg=self.colors['primary'])
                icon_label.configure(bg=self.colors['primary'], fg="white")
                text_label.configure(bg=self.colors['primary'], fg="white")
                break
                
        self.active_nav_button = active_button
        
    def on_nav_hover(self, button_frame, entering):
        if button_frame == self.active_nav_button:
            return
            
        if entering:
            color = self.colors['sidebar_hover']
            text_color = "white"
        else:
            color = self.colors['sidebar']
            text_color = "#94a3b8"
            
        for bf, icon_label, text_label in self.nav_buttons:
            if bf == button_frame:
                bf.configure(bg=color)
                icon_label.configure(bg=color, fg=text_color)
                text_label.configure(bg=color, fg=text_color)
                break
                
    def create_main_content_area(self):
        """Create the main content area with smooth transitions"""
        self.main_container = tk.Frame(self.master, bg=self.colors['background'])
        self.main_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Content frame with padding
        self.content_frame = tk.Frame(self.main_container, bg=self.colors['background'])
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
    def create_bottom_panel(self):
        """Create a modern bottom panel"""
        self.bottom_panel = tk.Frame(self.main_container, bg=self.colors['surface'], height=80)
        self.bottom_panel.pack(fill=tk.X, side=tk.BOTTOM)
        self.bottom_panel.pack_propagate(False)
        
        # Left side - Toggle switch
        left_frame = tk.Frame(self.bottom_panel, bg=self.colors['surface'])
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=30)
        
        toggle_label = tk.Label(left_frame, text="Multi-file Mode", 
                               font=("Segoe UI", 12), bg=self.colors['surface'], 
                               fg=self.colors['text_secondary'])
        toggle_label.pack(side=tk.LEFT, pady=25)
        
        # Modern toggle switch
        self.toggle_state = False
        self.toggle_frame = tk.Frame(left_frame, bg="#e5e7eb", width=50, height=24, cursor="hand2")
        self.toggle_frame.pack(side=tk.LEFT, padx=(15, 0), pady=28)
        self.toggle_frame.pack_propagate(False)
        
        self.toggle_circle = tk.Label(self.toggle_frame, text="", bg="white", width=2, height=1)
        self.toggle_circle.place(x=2, y=2, width=20, height=20)
        
        self.toggle_frame.bind('<Button-1>', self.toggle_multi_file)
        self.toggle_circle.bind('<Button-1>', self.toggle_multi_file)
        
        # Right side - Package button
        self.package_button = ModernButton(
            self.bottom_panel, 
            text="🚀 Start Packaging",
            command=self.start_packaging,
            bg_color=self.colors['primary'],
            hover_color=self.colors['primary_hover'],
            font=("Segoe UI", 14, "bold"),
            padding=(40, 15)
        )
        self.package_button.pack(side=tk.RIGHT, padx=30, pady=15)
        
    def toggle_multi_file(self, event=None):
        self.toggle_state = not self.toggle_state
        if self.toggle_state:
            self.toggle_frame.configure(bg=self.colors['primary'])
            self.toggle_circle.place(x=28, y=2)
        else:
            self.toggle_frame.configure(bg="#e5e7eb")
            self.toggle_circle.place(x=2, y=2)
            
    def clear_content(self):
        """Clear main content area"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
    def create_card(self, parent, title, subtitle="", height=None):
        """Create a modern glass-morphism card"""
        card = GlassCard(parent)
        if height:
            card.configure(height=height)
            card.pack_propagate(False)
            
        # Card header
        if title:
            header = tk.Frame(card, bg="white")
            header.pack(fill=tk.X, padx=30, pady=(25, 15))
            
            title_label = tk.Label(header, text=title, font=("Segoe UI", 18, "bold"),
                                   bg="white", fg=self.colors['text_primary'])
            title_label.pack(anchor="w")
            
            if subtitle:
                subtitle_label = tk.Label(header, text=subtitle, font=("Segoe UI", 11),
                                         bg="white", fg=self.colors['text_secondary'])
                subtitle_label.pack(anchor="w", pady=(5, 0))
                
        return card
        
    def show_home_page(self):
        """Display the enhanced home page"""
        self.clear_content()
        self.current_page = "home"
        
        # Page title
        title_frame = tk.Frame(self.content_frame, bg=self.colors['background'])
        title_frame.pack(fill=tk.X, pady=(0, 30))
        
        page_title = tk.Label(title_frame, text="Python Application Packager", 
                              font=("Segoe UI", 28, "bold"), 
                              bg=self.colors['background'], fg=self.colors['text_primary'])
        page_title.pack(anchor="w")
        
        subtitle = tk.Label(title_frame, text="Transform your Python scripts into professional desktop applications", 
                            font=("Segoe UI", 14), 
                            bg=self.colors['background'], fg=self.colors['text_secondary'])
        subtitle.pack(anchor="w", pady=(5, 0))
        
        # Main grid layout
        main_grid = tk.Frame(self.content_frame, bg=self.colors['background'])
        main_grid.pack(fill=tk.BOTH, expand=True)
        main_grid.grid_columnconfigure(0, weight=1)
        main_grid.grid_columnconfigure(1, weight=1)
        main_grid.grid_rowconfigure(1, weight=1)
        
        # File selection card (full width)
        file_card = self.create_card(main_grid, "Select Python File", 
                                     "Choose the main Python file for your application")
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
        
        drop_text = tk.Label(drop_area, text="Drag & drop your Python file here or click to browse",
                             font=("Segoe UI", 12), bg="#f8fafc", fg=self.colors['text_secondary'])
        drop_text.pack()
        
        # File info display
        self.file_info_frame = tk.Frame(file_content, bg="white")
        self.file_info_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Browse button
        browse_button = ModernButton(file_content, text="📂 Browse Files", 
                                     command=self.choose_file, padding=(20, 10))
        browse_button.pack(pady=15)
        
        # Make drop area clickable
        for widget in [drop_area, drop_icon, drop_text]:
            widget.bind('<Button-1>', lambda e: self.choose_file())
            widget.configure(cursor="hand2")
            
        # Output path card
        output_card = self.create_card(main_grid, "Output Directory", 
                                       "Choose where to save the packaged application")
        output_card.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        
        output_content = tk.Frame(output_card, bg="white")
        output_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 25))
        
        # Output path display
        self.output_display = tk.Label(output_content, text="📁 Auto-selected (same as source file)",
                                       font=("Segoe UI", 11), bg="white", 
                                       fg=self.colors['text_secondary'], anchor="w")
        self.output_display.pack(fill=tk.X, pady=(10, 15))
        
        output_button = ModernButton(output_content, text="📂 Choose Directory",
                                     command=self.choose_output_path, padding=(15, 8),
                                     bg_color="#6b7280", hover_color="#4b5563")
        output_button.pack(pady=10)
        
        # Icon settings card
        icon_card = self.create_card(main_grid, "Application Icon", 
                                     "Customize your application's appearance")
        icon_card.grid(row=1, column=1, sticky="nsew", padx=(10, 0))
        
        icon_content = tk.Frame(icon_card, bg="white")
        icon_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 25))
        
        # Icon preview
        icon_preview_frame = tk.Frame(icon_content, bg="white")
        icon_preview_frame.pack(fill=tk.X, pady=(10, 15))
        
        self.icon_preview = tk.Label(icon_preview_frame, text="🚀", font=("Segoe UI Emoji", 48),
                                     bg="white", fg=self.colors['primary'])
        self.icon_preview.pack()
        
        icon_status = tk.Label(icon_preview_frame, text="Default icon will be used",
                               font=("Segoe UI", 10), bg="white", 
                               fg=self.colors['text_secondary'])
        icon_status.pack(pady=(5, 0))
        
        icon_button = ModernButton(icon_content, text="🎨 Choose Icon",
                                   command=self.choose_icon, padding=(15, 8),
                                   bg_color="#6b7280", hover_color="#4b5563")
        icon_button.pack(pady=10)
        
    def show_file_settings_page(self):
        self.clear_content()
        self.current_page = "file_settings"
        
        # Page header
        header = tk.Frame(self.content_frame, bg=self.colors['background'])
        header.pack(fill=tk.X, pady=(0, 30))
        
        title = tk.Label(header, text="File Settings", font=("Segoe UI", 28, "bold"),
                         bg=self.colors['background'], fg=self.colors['text_primary'])
        title.pack(anchor="w")
        
        subtitle = tk.Label(header, text="Configure additional files and dependencies",
                            font=("Segoe UI", 14), bg=self.colors['background'], 
                            fg=self.colors['text_secondary'])
        subtitle.pack(anchor="w", pady=(5, 0))
        
        # Settings cards
        self.create_file_settings_cards()
        
    def create_file_settings_cards(self):
        """Create file settings configuration cards"""
        grid = tk.Frame(self.content_frame, bg=self.colors['background'])
        grid.pack(fill=tk.BOTH, expand=True)
        grid.grid_columnconfigure(0, weight=1)
        
        # Include files card
        include_card = self.create_card(grid, "Include Additional Files",
                                         "Add extra files and directories to your package")
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
        
        add_file_btn = ModernButton(button_frame, text="➕ Add Files",
                                    command=self.add_include_files, padding=(15, 8),
                                    bg_color=self.colors['success'])
        add_file_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        add_dir_btn = ModernButton(button_frame, text="📁 Add Directory",
                                    command=self.add_include_directory, padding=(15, 8),
                                    bg_color=self.colors['secondary'])
        add_dir_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        remove_btn = ModernButton(button_frame, text="🗑️ Remove",
                                 command=self.remove_include_item, padding=(15, 8),
                                 bg_color=self.colors['error'])
        remove_btn.pack(side=tk.RIGHT)
        
        # Exclude patterns card
        exclude_card = self.create_card(grid, "Exclude Patterns",
                                         "Specify files and patterns to exclude from packaging")
        exclude_card.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        
        exclude_content = tk.Frame(exclude_card, bg="white")
        exclude_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 25))
        
        # Common exclusions with checkboxes
        common_frame = tk.Frame(exclude_content, bg="white")
        common_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(common_frame, text="Common exclusions:", font=("Segoe UI", 12, "bold"),
                 bg="white", fg=self.colors['text_primary']).pack(anchor="w", pady=(0, 10))
        
        exclusions = [
            ("__pycache__ directories", "*.pyc, __pycache__/"),
            ("Test files", "test_*, *_test.py"),
            ("Documentation", "*.md, docs/"),
            ("Development tools", ".git/, .vscode/")
        ]
        
        self.exclusion_vars = {}
        for name, pattern in exclusions:
            var = tk.BooleanVar(value=True)
            self.exclusion_vars[pattern] = var
            
            cb = tk.Checkbutton(common_frame, text=f"{name} ({pattern})",
                                 variable=var, font=("Segoe UI", 10),
                                 bg="white", fg=self.colors['text_secondary'])
            cb.pack(anchor="w", pady=2)
            
    def show_packaging_settings_page(self):
        self.clear_content()
        self.current_page = "packaging_settings"
        
        # Page header
        header = tk.Frame(self.content_frame, bg=self.colors['background'])
        header.pack(fill=tk.X, pady=(0, 30))
        
        title = tk.Label(header, text="Packaging Configuration", font=("Segoe UI", 28, "bold"),
                         bg=self.colors['background'], fg=self.colors['text_primary'])
        title.pack(anchor="w")
        
        subtitle = tk.Label(header, text="Fine-tune your application packaging settings",
                            font=("Segoe UI", 14), bg=self.colors['background'], 
                            fg=self.colors['text_secondary'])
        subtitle.pack(anchor="w", pady=(5, 0))
        
        self.create_packaging_settings_cards()
        
    def create_packaging_settings_cards(self):
        """Create packaging configuration cards"""
        grid = tk.Frame(self.content_frame, bg=self.colors['background'])
        grid.pack(fill=tk.BOTH, expand=True)
        grid.grid_columnconfigure(0, weight=1)
        grid.grid_columnconfigure(1, weight=1)
        
        # Basic options card
        basic_card = self.create_card(grid, "Basic Options", "Core packaging settings")
        basic_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=(0, 20))
        
        basic_content = tk.Frame(basic_card, bg="white")
        basic_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 25))
        
        # Single file option
        self.single_file_var = tk.BooleanVar(value=True)
        single_file_cb = tk.Checkbutton(basic_content, text="📦 Single executable file", 
                                        variable=self.single_file_var, font=("Segoe UI", 12),
                                        bg="white", fg=self.colors['text_primary'])
        single_file_cb.pack(anchor="w", pady=(10, 5))
        
        single_file_desc = tk.Label(basic_content, text="Package everything into one executable file",
                                    font=("Segoe UI", 10), bg="white", 
                                    fg=self.colors['text_secondary'])
        single_file_desc.pack(anchor="w", padx=(25, 0), pady=(0, 15))
        
        # Console window option
        self.console_var = tk.BooleanVar(value=False)
        console_cb = tk.Checkbutton(basic_content, text="💻 Show console window", 
                                    variable=self.console_var, font=("Segoe UI", 12),
                                    bg="white", fg=self.colors['text_primary'])
        console_cb.pack(anchor="w", pady=5)
        
        console_desc = tk.Label(basic_content, text="Display console for debugging output",
                                font=("Segoe UI", 10), bg="white", 
                                fg=self.colors['text_secondary'])
        console_desc.pack(anchor="w", padx=(25, 0), pady=(0, 15))
        
        # Optimization level
        tk.Label(basic_content, text="🚀 Optimization Level:", font=("Segoe UI", 12, "bold"),
                 bg="white", fg=self.colors['text_primary']).pack(anchor="w", pady=(10, 5))
        
        self.optimization_var = tk.StringVar(value="balanced")
        opt_frame = tk.Frame(basic_content, bg="white")
        opt_frame.pack(anchor="w", padx=(25, 0))
        
        for value, text in [("fast", "Fast Build"), ("balanced", "Balanced"), ("size", "Smaller Size")]:
            rb = tk.Radiobutton(opt_frame, text=text, variable=self.optimization_var, 
                                value=value, font=("Segoe UI", 10), bg="white",
                                fg=self.colors['text_secondary'])
            rb.pack(anchor="w", pady=2)
            
        # Advanced options card
        advanced_card = self.create_card(grid, "Advanced Options", "Expert configuration settings")
        advanced_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=(0, 20))
        
        advanced_content = tk.Frame(advanced_card, bg="white")
        advanced_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 25))
        
        # Threading option
        self.threading_var = tk.BooleanVar(value=True)
        threading_cb = tk.Checkbutton(advanced_content, text="⚡ Enable threading", 
                                      variable=self.threading_var, font=("Segoe UI", 12),
                                      bg="white", fg=self.colors['text_primary'])
        threading_cb.pack(anchor="w", pady=(10, 5))
        
        # Plugin selection
        tk.Label(advanced_content, text="🔌 Plugins:", font=("Segoe UI", 12, "bold"),
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
        naming_card = self.create_card(grid, "🏷️ Output Configuration", "Customize output file settings")
        naming_card.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        
        naming_content = tk.Frame(naming_card, bg="white")
        naming_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 25))
        
        # Output name
        name_frame = tk.Frame(naming_content, bg="white")
        name_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(name_frame, text="Output Name:", font=("Segoe UI", 12, "bold"),
                 bg="white", fg=self.colors['text_primary']).pack(side=tk.LEFT)
        
        self.output_name_var = tk.StringVar(value="MyApplication")
        name_entry = tk.Entry(name_frame, textvariable=self.output_name_var, 
                              font=("Segoe UI", 11), width=30, relief="solid", bd=1)
        name_entry.pack(side=tk.LEFT, padx=(10, 0))
        
    def show_advanced_settings_page(self):
        self.clear_content()
        self.current_page = "advanced_settings"
        
        # Page header
        header = tk.Frame(self.content_frame, bg=self.colors['background'])
        header.pack(fill=tk.X, pady=(0, 30))
        
        title = tk.Label(header, text="Advanced Configuration", font=("Segoe UI", 28, "bold"),
                         bg=self.colors['background'], fg=self.colors['text_primary'])
        title.pack(anchor="w")
        
        subtitle = tk.Label(header, text="Expert settings for power users",
                            font=("Segoe UI", 14), bg=self.colors['background'], 
                            fg=self.colors['text_secondary'])
        subtitle.pack(anchor="w", pady=(5, 0))
        
        # Create advanced settings cards
        self.create_advanced_settings_cards()
        
    def create_advanced_settings_cards(self):
        """Create advanced configuration cards"""
        grid = tk.Frame(self.content_frame, bg=self.colors['background'])
        grid.pack(fill=tk.BOTH, expand=True)
        grid.grid_columnconfigure(0, weight=1)
        
        # Performance tuning card
        perf_card = self.create_card(grid, "⚡ Performance Tuning", 
                                     "Optimize build performance and output")
        perf_card.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        perf_content = tk.Frame(perf_card, bg="white")
        perf_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 25))
        
        # CPU cores slider
        cores_frame = tk.Frame(perf_content, bg="white")
        cores_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(cores_frame, text="Build Threads:", font=("Segoe UI", 12, "bold"),
                 bg="white", fg=self.colors['text_primary']).pack(anchor="w")
        
        self.cores_var = tk.IntVar(value=4)
        cores_scale = tk.Scale(cores_frame, from_=1, to=16, orient=tk.HORIZONTAL,
                               variable=self.cores_var, font=("Segoe UI", 10),
                               bg="white", fg=self.colors['text_secondary'],
                               highlightthickness=0, length=300)
        cores_scale.pack(anchor="w", pady=5)
        
        # Memory usage
        memory_frame = tk.Frame(perf_content, bg="white")
        memory_frame.pack(fill=tk.X, pady=15)
        
        tk.Label(memory_frame, text="Memory Limit (GB):", font=("Segoe UI", 12, "bold"),
                 bg="white", fg=self.colors['text_primary']).pack(anchor="w")
        
        self.memory_var = tk.DoubleVar(value=2.0)
        memory_scale = tk.Scale(memory_frame, from_=0.5, to=8.0, resolution=0.5,
                                orient=tk.HORIZONTAL, variable=self.memory_var,
                                font=("Segoe UI", 10), bg="white", 
                                fg=self.colors['text_secondary'],
                                highlightthickness=0, length=300)
        memory_scale.pack(anchor="w", pady=5)
        
        # Debug options card
        debug_card = self.create_card(grid, "🐛 Debug & Logging", 
                                      "Configure debugging and logging options")
        debug_card.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        
        debug_content = tk.Frame(debug_card, bg="white")
        debug_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 25))
        
        # Debug options
        debug_options = [
            ("Enable debug mode", "debug_mode"),
            ("Verbose output", "verbose"),
            ("Show progress", "show_progress"),
            ("Generate report", "generate_report")
        ]
        
        self.debug_vars = {}
        for text, key in debug_options:
            var = tk.BooleanVar(value=key == "show_progress")
            self.debug_vars[key] = var
            cb = tk.Checkbutton(debug_content, text=text, variable=var,
                                 font=("Segoe UI", 11), bg="white",
                                 fg=self.colors['text_primary'])
            cb.pack(anchor="w", pady=5)
            
    def show_statistics_page(self):
        self.clear_content()
        self.current_page = "statistics"
        
        # Page header
        header = tk.Frame(self.content_frame, bg=self.colors['background'])
        header.pack(fill=tk.X, pady=(0, 30))
        
        title = tk.Label(header, text="📊 Build Statistics", font=("Segoe UI", 28, "bold"),
                         bg=self.colors['background'], fg=self.colors['text_primary'])
        title.pack(anchor="w")
        
        subtitle = tk.Label(header, text="Track your packaging history and performance",
                            font=("Segoe UI", 14), bg=self.colors['background'], 
                            fg=self.colors['text_secondary'])
        subtitle.pack(anchor="w", pady=(5, 0))
        
        # Statistics grid
        stats_grid = tk.Frame(self.content_frame, bg=self.colors['background'])
        stats_grid.pack(fill=tk.BOTH, expand=True)
        stats_grid.grid_columnconfigure(0, weight=1)
        stats_grid.grid_columnconfigure(1, weight=1)
        stats_grid.grid_columnconfigure(2, weight=1)
        
        # Stats cards
        stats_data = [
            ("📦", "Total Builds", "42", self.colors['primary']),
            ("✅", "Successful", "38", self.colors['success']),
            ("⚠️", "Failed", "4", self.colors['error']),
            ("⏱️", "Avg. Time", "2m 34s", self.colors['secondary']),
            ("💾", "Total Size", "1.2 GB", self.colors['accent']),
            ("📅", "Last Build", "2h ago", self.colors['text_secondary'])
        ]
        
        for i, (icon, label, value, color) in enumerate(stats_data):
            row, col = divmod(i, 3)
            self.create_stat_card(stats_grid, icon, label, value, color, row, col)
            
        # Recent builds card
        recent_card = self.create_card(stats_grid, "Recent Builds", "Your latest packaging activities")
        recent_card.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(20, 0))
        
        recent_content = tk.Frame(recent_card, bg="white")
        recent_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 25))
        
        # Table headers
        headers_frame = tk.Frame(recent_content, bg="#f8fafc", height=35)
        headers_frame.pack(fill=tk.X, pady=(10, 0))
        headers_frame.pack_propagate(False)
        
        headers = ["Project", "Status", "Size", "Time", "Date"]
        for i, header in enumerate(headers):
            label = tk.Label(headers_frame, text=header, font=("Segoe UI", 11, "bold"),
                             bg="#f8fafc", fg=self.colors['text_primary'])
            label.place(x=50 + i*150, y=8)
            
        # Sample data rows
        builds = [
            ("MyApp v1.0", "✅ Success", "45.2 MB", "1m 23s", "2 hours ago"),
            ("DataProcessor", "✅ Success", "23.1 MB", "2m 45s", "1 day ago"),
            ("GameEngine", "⚠️ Failed", "—", "—", "2 days ago"),
            ("WebScraper", "✅ Success", "12.8 MB", "45s", "3 days ago")
        ]
        
        for i, (project, status, size, time, date) in enumerate(builds):
            row_frame = tk.Frame(recent_content, bg="white", height=40)
            row_frame.pack(fill=tk.X, pady=1)
            row_frame.pack_propagate(False)
            
            data = [project, status, size, time, date]
            for j, text in enumerate(data):
                color = self.colors['success'] if "Success" in text else (
                    self.colors['error'] if "Failed" in text else self.colors['text_secondary'])
                label = tk.Label(row_frame, text=text, font=("Segoe UI", 10),
                                 bg="white", fg=color)
                label.place(x=50 + j*150, y=12)
                
    def create_stat_card(self, parent, icon, label, value, color, row, col):
        """Create a statistics card"""
        card = GlassCard(parent, height=120)
        card.grid(row=row, column=col, sticky="ew", padx=5, pady=5)
        
        content = tk.Frame(card, bg="white")
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Icon
        icon_label = tk.Label(content, text=icon, font=("Segoe UI Emoji", 24),
                              bg="white", fg=color)
        icon_label.pack(anchor="w")
        
        # Value
        value_label = tk.Label(content, text=value, font=("Segoe UI", 20, "bold"),
                              bg="white", fg=self.colors['text_primary'])
        value_label.pack(anchor="w", pady=(5, 0))
        
        # Label
        label_label = tk.Label(content, text=label, font=("Segoe UI", 11),
                              bg="white", fg=self.colors['text_secondary'])
        label_label.pack(anchor="w")
        
    def show_about_page(self):
        self.clear_content()
        self.current_page = "about"
        
        # Center content
        center_frame = tk.Frame(self.content_frame, bg=self.colors['background'])
        center_frame.pack(expand=True, fill=tk.BOTH)
        
        content = tk.Frame(center_frame, bg=self.colors['background'])
        content.place(relx=0.5, rely=0.5, anchor="center")
        
        # App icon
        app_icon = tk.Label(content, text="🚀", font=("Segoe UI Emoji", 80),
                            bg=self.colors['background'])
        app_icon.pack(pady=(0, 20))
        
        # App name
        app_name = tk.Label(content, text="Nuitka Premium Studio", 
                            font=("Segoe UI", 32, "bold"),
                            bg=self.colors['background'], fg=self.colors['text_primary'])
        app_name.pack()
        
        # Version
        version = tk.Label(content, text="Version 2.0.0", font=("Segoe UI", 16),
                           bg=self.colors['background'], fg=self.colors['text_secondary'])
        version.pack(pady=10)
        
        # Description
        desc = tk.Label(content, text="Professional Python Application Packager\nPowered by Nuitka Engine",
                        font=("Segoe UI", 14), bg=self.colors['background'], 
                        fg=self.colors['text_secondary'], justify=tk.CENTER)
        desc.pack(pady=20)
        
        # Links frame
        links_frame = tk.Frame(content, bg=self.colors['background'])
        links_frame.pack(pady=30)
        
        # Link buttons
        links = [
            ("🌐 Website", self.open_website),
            ("📚 Documentation", self.open_docs),
            ("🐛 Report Issue", self.open_issues),
            ("💝 Support", self.open_support)
        ]
        
        for text, command in links:
            btn = ModernButton(links_frame, text=text, command=command,
                               bg_color="#6b7280", hover_color="#4b5563",
                               padding=(15, 8))
            btn.pack(side=tk.LEFT, padx=5)
            
        # Copyright
        copyright = tk.Label(content, text="© 2025 Nuitka Premium Studio. All rights reserved.",
                             font=("Segoe UI", 10), bg=self.colors['background'], 
                             fg=self.colors['text_muted'])
        copyright.pack(pady=(40, 0))
        
    def show_global_settings_page(self):
        self.clear_content()
        self.current_page = "global_settings"
        
        # Page header
        header = tk.Frame(self.content_frame, bg=self.colors['background'])
        header.pack(fill=tk.X, pady=(0, 30))
        
        title = tk.Label(header, text="⚙️ Global Settings", font=("Segoe UI", 28, "bold"),
                         bg=self.colors['background'], fg=self.colors['text_primary'])
        title.pack(anchor="w")
        
        subtitle = tk.Label(header, text="Configure application preferences and behavior",
                            font=("Segoe UI", 14), bg=self.colors['background'], 
                            fg=self.colors['text_secondary'])
        subtitle.pack(anchor="w", pady=(5, 0))
        
        # Settings cards
        self.create_global_settings_cards()
        
    def create_global_settings_cards(self):
        """Create global settings cards"""
        grid = tk.Frame(self.content_frame, bg=self.colors['background'])
        grid.pack(fill=tk.BOTH, expand=True)
        grid.grid_columnconfigure(0, weight=1)
        grid.grid_columnconfigure(1, weight=1)
        
        # Appearance card
        appearance_card = self.create_card(grid, "🎨 Appearance", "Customize the application look")
        appearance_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=(0, 20))
        
        appearance_content = tk.Frame(appearance_card, bg="white")
        appearance_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 25))
        
        # Theme selection
        tk.Label(appearance_content, text="Theme:", font=("Segoe UI", 12, "bold"),
                 bg="white", fg=self.colors['text_primary']).pack(anchor="w", pady=(10, 5))
        
        self.theme_var = tk.StringVar(value="light")
        theme_frame = tk.Frame(appearance_content, bg="white")
        theme_frame.pack(anchor="w", padx=(20, 0))
        
        for theme in ["light", "dark", "auto"]:
            rb = tk.Radiobutton(theme_frame, text=theme.capitalize(), 
                                variable=self.theme_var, value=theme,
                                font=("Segoe UI", 10), bg="white",
                                fg=self.colors['text_secondary'])
            rb.pack(anchor="w", pady=2)
            
        # Behavior card
        behavior_card = self.create_card(grid, "⚡ Behavior", "Application behavior settings")
        behavior_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=(0, 20))
        
        behavior_content = tk.Frame(behavior_card, bg="white")
        behavior_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 25))
        
        # Behavior options
        behavior_options = [
            ("Auto-save settings", "auto_save"),
            ("Check for updates", "check_updates"),
            ("Show notifications", "notifications"),
            ("Remember window size", "remember_size")
        ]
        
        self.behavior_vars = {}
        for text, key in behavior_options:
            var = tk.BooleanVar(value=True)
            self.behavior_vars[key] = var
            cb = tk.Checkbutton(behavior_content, text=text, variable=var,
                                 font=("Segoe UI", 11), bg="white",
                                 fg=self.colors['text_primary'])
            cb.pack(anchor="w", pady=(10, 5))
            
        # Paths card
        paths_card = self.create_card(grid, "📁 Default Paths", "Configure default directories")
        paths_card.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        
        paths_content = tk.Frame(paths_card, bg="white")
        paths_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 25))
        
        # Default paths
        path_items = [
            ("Default Output Directory:", "output_dir"),
            ("Temporary Files Directory:", "temp_dir"),
            ("Projects Directory:", "projects_dir")
        ]
        
        self.path_vars = {}
        for label, key in path_items:
            frame = tk.Frame(paths_content, bg="white")
            frame.pack(fill=tk.X, pady=10)
            
            tk.Label(frame, text=label, font=("Segoe UI", 11, "bold"),
                     bg="white", fg=self.colors['text_primary']).pack(anchor="w")
            
            path_frame = tk.Frame(frame, bg="white")
            path_frame.pack(fill=tk.X, pady=(5, 0))
            
            var = tk.StringVar(value=f"C:/Users/Default/{key}")
            self.path_vars[key] = var
            
            entry = tk.Entry(path_frame, textvariable=var, font=("Segoe UI", 10),
                             relief="solid", bd=1, width=50)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            browse_btn = ModernButton(path_frame, text="📂", command=lambda k=key: self.browse_path(k),
                                      bg_color="#6b7280", hover_color="#4b5563", padding=(10, 5))
            browse_btn.pack(side=tk.RIGHT, padx=(10, 0))
            
    # Event handlers and utility methods
    def on_window_configure(self, event):
        """Handle window resize events"""
        if event.widget == self.master:
            # Add any resize handling logic here
            pass
            
    def choose_file(self):
        """Open file dialog to select Python file"""
        file_types = [
            ("Python files", "*.py"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Select Python File",
            filetypes=file_types,
            initialdir="."
        )
        
        if filename:
            self.selected_file = filename
            self.update_file_display(filename)
            
    def update_file_display(self, filename):
        """Update file display in the UI"""
        import os
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
        
        name_label = tk.Label(file_details, text=f"Selected: {basename}",
                              font=("Segoe UI", 12, "bold"), bg="#e8f5e8",
                              fg=self.colors['text_primary'])
        name_label.pack(anchor="w")
        
        path_label = tk.Label(file_details, text=f"Path: {filename}",
                              font=("Segoe UI", 9), bg="#e8f5e8",
                              fg=self.colors['text_secondary'])
        path_label.pack(anchor="w")
        
    def choose_output_path(self):
        """Open directory dialog to select output path"""
        directory = filedialog.askdirectory(
            title="Select Output Directory",
            initialdir="."
        )
        
        if directory:
            self.output_path = directory
            self.output_display.configure(text=f"📁 {directory}")
            
    def choose_icon(self):
        """Open file dialog to select icon file"""
        file_types = [
            ("Icon files", "*.ico"),
            ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Select Icon File",
            filetypes=file_types,
            initialdir="."
        )
        
        if filename:
            self.icon_path = filename
            # Update icon preview if possible
            self.icon_preview.configure(text="🎨")
            
    def add_include_files(self):
        """Add files to include list"""
        files = filedialog.askopenfilenames(
            title="Select Files to Include",
            filetypes=[("All files", "*.*")]
        )
        
        for file in files:
            self.include_listbox.insert(tk.END, file)
            
    def add_include_directory(self):
        """Add directory to include list"""
        directory = filedialog.askdirectory(title="Select Directory to Include")
        
        if directory:
            self.include_listbox.insert(tk.END, f"[DIR] {directory}")
            
    def remove_include_item(self):
        """Remove selected item from include list"""
        selection = self.include_listbox.curselection()
        if selection:
            self.include_listbox.delete(selection)
            
    def browse_path(self, path_key):
        """Browse for path setting"""
        directory = filedialog.askdirectory(title=f"Select {path_key.replace('_', ' ').title()}")
        
        if directory:
            self.path_vars[path_key].set(directory)
            
    # Link handlers
    def open_website(self):
        messagebox.showinfo("Website", "Opening website...")
        
    def open_docs(self):
        messagebox.showinfo("Documentation", "Opening documentation...")
        
    def open_issues(self):
        messagebox.showinfo("Issues", "Opening issue tracker...")
        
    def open_support(self):
        messagebox.showinfo("Support", "Opening support page...")
        
    def start_packaging(self):
        """Start the packaging process with animated progress"""
        if not self.selected_file:
            messagebox.showwarning("No File Selected", 
                                  "Please select a Python file to package first.")
            return
            
        # Create progress dialog
        self.show_packaging_progress()
        
    def show_packaging_progress(self):
        """Show animated packaging progress"""
        progress_window = tk.Toplevel(self.master)
        progress_window.title("Packaging Progress")
        progress_window.geometry("500x300")
        progress_window.configure(bg="white")
        progress_window.transient(self.master)
        progress_window.grab_set()
        
        # Center the window
        progress_window.geometry("+{}+{}".format(
            self.master.winfo_rootx() + 450,
            self.master.winfo_rooty() + 300
        ))
        
        # Progress content
        content = tk.Frame(progress_window, bg="white")
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Title
        tk.Label(content, text="🚀 Packaging Your Application...", font=("Segoe UI", 18, "bold"),
                 bg="white", fg=self.colors['text_primary']).pack(pady=(10, 20))
        
        # File name being packaged
        tk.Label(content, text=f"File: {self.selected_file}", font=("Segoe UI", 11),
                 bg="white", fg=self.colors['text_secondary'], wraplength=400).pack(pady=(0, 10))
        
        # Progress bar
        self.progress_bar = AnimatedProgress(content, width=400, height=12,
                                             bg_color="#e1e5e9", fill_color=self.colors['primary'])
        self.progress_bar.pack(pady=20)
        
        # Status label
        self.status_label = tk.Label(content, text="Initializing...", font=("Segoe UI", 10),
                                      bg="white", fg=self.colors['text_muted'])
        self.status_label.pack(pady=(10, 0))
        
        # Cancel button
        cancel_button = ModernButton(
            content,
            text="❌ Cancel",
            command=lambda: self.cancel_packaging(progress_window),
            bg_color=self.colors['error'],
            hover_color="#c23b3b",
            font=("Segoe UI", 12),
            padding=(20, 10)
        )
        cancel_button.pack(pady=20)
        
        # Start packaging in a separate thread
        self.packaging_thread = threading.Thread(target=self._simulate_packaging, args=(progress_window,))
        self.packaging_thread.start()

    def _simulate_packaging(self, progress_window):
        """Simulate the packaging process with progress updates."""
        self.animation_running = True
        steps = [
            ("Analyzing dependencies...", 10),
            ("Optimizing code...", 30),
            ("Compiling modules...", 60),
            ("Bundling resources...", 85),
            ("Finalizing executable...", 95),
            ("Packaging complete!", 100)
        ]
        
        for i, (status_text, progress_value) in enumerate(steps):
            if not self.animation_running:
                break
            
            self.status_label.configure(text=status_text)
            self.progress_bar.set_progress(progress_value)
            time.sleep(1 + (i * 0.2)) # Simulate work
            
        if self.animation_running:
            self.status_label.configure(text="Packaging completed successfully!", fg=self.colors['success'])
            self.progress_bar.set_progress(100)
            messagebox.showinfo("Packaging Complete", "Your application has been packaged successfully!")
            progress_window.after(1000, progress_window.destroy) # Close after a short delay
        else:
            self.status_label.configure(text="Packaging cancelled.", fg=self.colors['error'])
            messagebox.showinfo("Packaging Cancelled", "Packaging process was cancelled.")
            progress_window.after(500, progress_window.destroy)

    def cancel_packaging(self, progress_window):
        """Cancel the packaging process."""
        self.animation_running = False # Signal the thread to stop
        messagebox.showinfo("Cancelling...", "Attempting to cancel packaging. Please wait...")

if __name__ == "__main__":
    root = tk.Tk()
    app = PremiumNuitkaGUI(root)
    root.mainloop()