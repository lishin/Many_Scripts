import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import time
from PIL import Image, ImageTk, ImageDraw # Removed ImageFilter, math as they are not directly used in gui_app.py
import os

# Import components and language manager
from core.components import ModernButton, AnimatedProgress, GlassCard
from core.language_manager import LanguageManager

# Import page classes
from pages.home_page import HomePage
from pages.file_settings_page import FileSettingsPage
from pages.packaging_settings_page import PackagingSettingsPage
from pages.advanced_settings_page import AdvancedSettingsPage
from pages.statistics_page import StatisticsPage
from pages.about_page import AboutPage
from pages.global_settings_page import GlobalSettingsPage

class PremiumNuitkaGUI:
    def __init__(self, master, lang_manager: LanguageManager):
        self.master = master
        self.lang = lang_manager # Language manager instance
        master.title(self.lang.get_text("app_title"))
        master.geometry("1400x900")
        master.minsize(1200, 800)
        master.configure(bg="#f8fafc")
        
        # We are *not* removing default window decorations, so no overrideredirect(True)
        # master.overrideredirect(False) # Already False by default, so can be removed or kept for clarity.
        
        # State variables
        self.current_page = None
        self.selected_file = None
        self.output_path = None
        self.icon_path = None
        self.is_maximized = False # This variable is not used if not creating custom titlebar
        self.animation_running = False
        
        self.setup_styles()
        # self.create_custom_titlebar() # REMOVED THIS CALL as requested
        self.create_sidebar()
        self.create_main_content_area()
        self.create_bottom_panel()
        
        # Initialize pages FIRST, before showing any page
        self.pages = {
            "home": HomePage(self.content_frame, self.colors, self.lang, self.choose_file, self.choose_output_path, self.choose_icon, self.update_file_display),
            "file_settings": FileSettingsPage(self.content_frame, self.colors, self.lang),
            "packaging_settings": PackagingSettingsPage(self.content_frame, self.colors, self.lang),
            "advanced_settings": AdvancedSettingsPage(self.content_frame, self.colors, self.lang),
            "statistics": StatisticsPage(self.content_frame, self.colors, self.lang),
            "about": AboutPage(self.content_frame, self.colors, self.lang, self.open_website, self.open_docs, self.open_issues, self.open_support),
            "global_settings": GlobalSettingsPage(self.content_frame, self.colors, self.lang, self.browse_path)
        }

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
        
    # REMOVED create_custom_titlebar, create_window_control, start_drag, on_drag, minimize_window, toggle_maximize, close_window methods entirely.
        
    def create_sidebar(self):
        """Create an elegant sidebar with smooth animations"""
        self.sidebar = tk.Frame(self.master, bg=self.colors['sidebar'], width=280)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        
        # Sidebar header
        header_frame = tk.Frame(self.sidebar, bg=self.colors['sidebar'], height=80)
        header_frame.pack(fill=tk.X, pady=(20, 30))
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(header_frame, text=self.lang.get_text("sidebar_navigation"), 
                               font=("Segoe UI", 16, "bold"), 
                               bg=self.colors['sidebar'], fg="white")
        header_label.pack(pady=20)
        
        # Navigation items
        nav_items = [
            ("🏠", self.lang.get_text("nav_home"), self.show_home_page),
            ("📁", self.lang.get_text("nav_file_settings"), self.show_file_settings_page),
            ("⚙️", self.lang.get_text("nav_packaging"), self.show_packaging_settings_page),
            ("🔧", self.lang.get_text("nav_advanced"), self.show_advanced_settings_page),
            ("📊", self.lang.get_text("nav_statistics"), self.show_statistics_page),
            ("ℹ️", self.lang.get_text("nav_about"), self.show_about_page),
        ]
        
        self.nav_buttons = []
        self.active_nav_button = None
        
        for icon, text, command in nav_items:
            self.create_nav_button(icon, text, command)
            
        # Bottom section
        bottom_frame = tk.Frame(self.sidebar, bg=self.colors['sidebar'])
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)
        
        self.create_nav_button("⚙️", self.lang.get_text("nav_global_settings"), self.show_global_settings_page, bottom_frame)
            
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
        
        toggle_label = tk.Label(left_frame, text=self.lang.get_text("bottom_multi_file_mode"), 
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
            text=self.lang.get_text("btn_start_packaging"),
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
        # This helper method is no longer needed in gui_app.py if pages create their own cards
        # However, keeping it here for clarity if you intend to reuse it directly in gui_app
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
        
    # Page display methods will now call the respective page class's create_ui method
    def show_home_page(self):
        self.clear_content()
        self.current_page = "home"
        self.pages["home"].create_ui(self.selected_file, self.output_path, self.icon_path)

    def show_file_settings_page(self):
        self.clear_content()
        self.current_page = "file_settings"
        self.pages["file_settings"].create_ui()

    def show_packaging_settings_page(self):
        self.clear_content()
        self.current_page = "packaging_settings"
        self.pages["packaging_settings"].create_ui()

    def show_advanced_settings_page(self):
        self.clear_content()
        self.current_page = "advanced_settings"
        self.pages["advanced_settings"].create_ui()

    def show_statistics_page(self):
        self.clear_content()
        self.current_page = "statistics"
        self.pages["statistics"].create_ui()
        
    def show_about_page(self):
        self.clear_content()
        self.current_page = "about"
        self.pages["about"].create_ui()

    def show_global_settings_page(self):
        self.clear_content()
        self.current_page = "global_settings"
        self.pages["global_settings"].create_ui()

    # Event handlers and utility methods (keep these in gui_app.py as they interact with overall app state)
    def on_window_configure(self, event):
        """Handle window resize events"""
        if event.widget == self.master:
            # Add any resize handling logic here
            pass
            
    def choose_file(self):
        """Open file dialog to select Python file"""
        file_types = [
            (self.lang.get_text("file_types_python"), "*.py"),
            (self.lang.get_text("file_types_all"), "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title=self.lang.get_text("select_python_file_title"),
            filetypes=file_types,
            initialdir="."
        )
        
        if filename:
            self.selected_file = filename
            # Update the home page's file display directly
            self.pages["home"].update_file_display(filename)
            
    def update_file_display(self, filename):
        """A pass-through to the HomePage's update_file_display"""
        if "home" in self.pages and self.pages["home"]:
            self.pages["home"].update_file_display(filename)

    def choose_output_path(self):
        """Open directory dialog to select output path"""
        directory = filedialog.askdirectory(
            title=self.lang.get_text("select_output_directory_title"),
            initialdir="."
        )
        
        if directory:
            self.output_path = directory
            # Update the home page's output display directly
            self.pages["home"].update_output_display(directory)
            
    def choose_icon(self):
        """Open file dialog to select icon file"""
        file_types = [
            (self.lang.get_text("file_types_icon"), "*.ico"),
            (self.lang.get_text("file_types_image"), "*.png *.jpg *.jpeg *.gif *.bmp"),
            (self.lang.get_text("file_types_all"), "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title=self.lang.get_text("select_icon_file_title"),
            filetypes=file_types,
            initialdir="."
        )
        
        if filename:
            self.icon_path = filename
            # Update icon preview if possible
            self.pages["home"].update_icon_preview(filename)
            
    # Add these placeholder methods or link to actual browser/app calls
    def open_website(self):
        messagebox.showinfo(self.lang.get_text("msg_website_title"), self.lang.get_text("msg_website_body"))
        # import webbrowser
        # webbrowser.open("https://nuitka.net")
        
    def open_docs(self):
        messagebox.showinfo(self.lang.get_text("msg_documentation_title"), self.lang.get_text("msg_documentation_body"))
        # import webbrowser
        # webbrowser.open("https://nuitka.net/doc/user-manual.html")
        
    def open_issues(self):
        messagebox.showinfo(self.lang.get_text("msg_issues_title"), self.lang.get_text("msg_issues_body"))
        # import webbrowser
        # webbrowser.open("https://github.com/Nuitka/Nuitka/issues")
        
    def open_support(self):
        messagebox.showinfo(self.lang.get_text("msg_support_title"), self.lang.get_text("msg_support_body"))
        # import webbrowser
        # webbrowser.open("https://nuitka.net/pages/support.html")

    def browse_path(self, path_key):
        """Browse for path setting (used in global settings)"""
        directory = filedialog.askdirectory(title=self.lang.get_text("select_path_for", path_key.replace('_', ' ').title()))
        
        if directory:
            # Assuming self.pages["global_settings"].path_vars exists and is accessible
            if "global_settings" in self.pages and self.pages["global_settings"]:
                self.pages["global_settings"].path_vars[path_key].set(directory)
            
    def start_packaging(self):
        """Start the packaging process with animated progress"""
        if not self.selected_file:
            messagebox.showwarning(self.lang.get_text("msg_no_file_selected_title"), 
                                  self.lang.get_text("msg_no_file_selected_body"))
            return
            
        # Create progress dialog
        self.show_packaging_progress()
        
    def show_packaging_progress(self):
        """Show animated packaging progress"""
        progress_window = tk.Toplevel(self.master)
        progress_window.title(self.lang.get_text("packaging_progress_title"))
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
        tk.Label(content, text=self.lang.get_text("packaging_title"), font=("Segoe UI", 18, "bold"),
                 bg="white", fg=self.colors['text_primary']).pack(pady=(10, 20))
        
        # File name being packaged
        tk.Label(content, text=self.lang.get_text("packaging_file", os.path.basename(self.selected_file)), font=("Segoe UI", 11),
                 bg="white", fg=self.colors['text_secondary'], wraplength=400).pack(pady=(0, 10))
        
        # Progress bar
        self.progress_bar = AnimatedProgress(content, width=400, height=12,
                                             bg_color="#e1e5e9", fill_color=self.colors['primary'])
        self.progress_bar.pack(pady=20)
        
        # Status label
        self.status_label = tk.Label(content, text=self.lang.get_text("packaging_initializing"), font=("Segoe UI", 10),
                                      bg="white", fg=self.colors['text_muted'])
        self.status_label.pack(pady=(10, 0))
        
        # Cancel button
        cancel_button = ModernButton(
            content,
            text=self.lang.get_text("btn_cancel"),
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
            (self.lang.get_text("packaging_analyzing"), 10),
            (self.lang.get_text("packaging_optimizing"), 30),
            (self.lang.get_text("packaging_compiling"), 60),
            (self.lang.get_text("packaging_bundling"), 85),
            (self.lang.get_text("packaging_finalizing"), 95),
            (self.lang.get_text("packaging_complete"), 100)
        ]
        
        for i, (status_text, progress_value) in enumerate(steps):
            if not self.animation_running:
                break
            
            self.status_label.configure(text=status_text)
            self.progress_bar.set_progress(progress_value)
            time.sleep(1 + (i * 0.2)) # Simulate work
            
        if self.animation_running:
            self.status_label.configure(text=self.lang.get_text("packaging_success_status"), fg=self.colors['success'])
            self.progress_bar.set_progress(100)
            messagebox.showinfo(self.lang.get_text("packaging_success_dialog_title"), self.lang.get_text("packaging_success_dialog_body"))
            progress_window.after(1000, progress_window.destroy) # Close after a short delay
        else:
            self.status_label.configure(text=self.lang.get_text("packaging_cancelled_status"), fg=self.colors['error'])
            messagebox.showinfo(self.lang.get_text("packaging_cancelled_dialog_title"), self.lang.get_text("packaging_cancelled_dialog_body"))
            progress_window.after(500, progress_window.destroy)

    def cancel_packaging(self, progress_window):
        """Cancel the packaging process."""
        self.animation_running = False # Signal the thread to stop
        messagebox.showinfo(self.lang.get_text("msg_cancelling"), self.lang.get_text("msg_attempt_cancel"))