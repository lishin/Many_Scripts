import tkinter as tk
from tkinter import ttk, font, messagebox
import json
import os
from abc import ABC, abstractmethod
from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import threading
import time

# =================== THEME SYSTEM ===================

class ThemeType(Enum):
    LIGHT = "light"
    DARK = "dark"
    CUSTOM = "custom"

@dataclass
class Theme:
    name: str
    type: ThemeType
    colors: Dict[str, str] = field(default_factory=dict)
    fonts: Dict[str, tuple] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.colors:
            self.colors = self._get_default_colors()
        if not self.fonts:
            self.fonts = self._get_default_fonts()
    
    def _get_default_colors(self) -> Dict[str, str]:
        if self.type == ThemeType.DARK:
            return {
                'bg_primary': '#2b2b2b',
                'bg_secondary': '#3c3c3c',
                'bg_tertiary': '#4d4d4d',
                'fg_primary': '#ffffff',
                'fg_secondary': '#cccccc',
                'accent': '#007acc',
                'accent_hover': '#1a8cdd',
                'success': '#28a745',
                'warning': '#ffc107',
                'error': '#dc3545',
                'border': '#555555',
                'hover': '#404040'
            }
        else:  # LIGHT
            return {
                'bg_primary': '#ffffff',
                'bg_secondary': '#f8f9fa',
                'bg_tertiary': '#e9ecef',
                'fg_primary': '#212529',
                'fg_secondary': '#6c757d',
                'accent': '#007bff',
                'accent_hover': '#0056b3',
                'success': '#28a745',
                'warning': '#ffc107',
                'error': '#dc3545',
                'border': '#dee2e6',
                'hover': '#f5f5f5'
            }
    
    def _get_default_fonts(self) -> Dict[str, tuple]:
        return {
            'default': ('Segoe UI', 9),
            'heading': ('Segoe UI', 12, 'bold'),
            'subheading': ('Segoe UI', 10, 'bold'),
            'small': ('Segoe UI', 8),
            'code': ('Consolas', 9)
        }

class ThemeManager:
    def __init__(self):
        self.themes = {
            'light': Theme('Light', ThemeType.LIGHT),
            'dark': Theme('Dark', ThemeType.DARK)
        }
        self.current_theme = self.themes['light']
        self.callbacks = []
    
    def set_theme(self, theme_name: str):
        if theme_name in self.themes:
            self.current_theme = self.themes[theme_name]
            self._notify_callbacks()
    
    def register_callback(self, callback: Callable):
        self.callbacks.append(callback)
    
    def _notify_callbacks(self):
        for callback in self.callbacks:
            callback(self.current_theme)
    
    def get_color(self, color_key: str) -> str:
        return self.current_theme.colors.get(color_key, '#000000')
    
    def get_font(self, font_key: str) -> tuple:
        return self.current_theme.fonts.get(font_key, ('Arial', 9))

# =================== STATE MANAGEMENT ===================

class StateManager:
    def __init__(self):
        self._state = {}
        self._subscribers = {}
    
    def set_state(self, key: str, value: Any):
        old_value = self._state.get(key)
        self._state[key] = value
        if key in self._subscribers:
            for callback in self._subscribers[key]:
                callback(value, old_value)
    
    def get_state(self, key: str, default=None):
        return self._state.get(key, default)
    
    def subscribe(self, key: str, callback: Callable):
        if key not in self._subscribers:
            self._subscribers[key] = []
        self._subscribers[key].append(callback)
    
    def unsubscribe(self, key: str, callback: Callable):
        if key in self._subscribers and callback in self._subscribers[key]:
            self._subscribers[key].remove(callback)

# =================== MODERN UI COMPONENTS ===================

class ModernButton(tk.Button):
    def __init__(self, parent, theme_manager: ThemeManager, **kwargs):
        self.theme_manager = theme_manager
        self.is_primary = kwargs.pop('primary', False)
        self.is_outline = kwargs.pop('outline', False)
        
        super().__init__(parent, **kwargs)
        self._setup_appearance()
        self._setup_hover_effects()
        self.theme_manager.register_callback(self._on_theme_change)
    
    def _setup_appearance(self):
        theme = self.theme_manager.current_theme
        if self.is_primary:
            bg_color = theme.colors['accent']
            fg_color = '#ffffff'
            hover_color = theme.colors['accent_hover']
        elif self.is_outline:
            bg_color = 'transparent'
            fg_color = theme.colors['accent']
            hover_color = theme.colors['hover']
        else:
            bg_color = theme.colors['bg_secondary']
            fg_color = theme.colors['fg_primary']
            hover_color = theme.colors['hover']
        
        self.config(
            bg=bg_color,
            fg=fg_color,
            font=theme.fonts['default'],
            relief='flat',
            borderwidth=0,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        self.hover_color = hover_color
        self.normal_color = bg_color
    
    def _setup_hover_effects(self):
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
    
    def _on_enter(self, event):
        self.config(bg=self.hover_color)
    
    def _on_leave(self, event):
        self.config(bg=self.normal_color)
    
    def _on_theme_change(self, theme):
        self._setup_appearance()

class ModernEntry(tk.Entry):
    def __init__(self, parent, theme_manager: ThemeManager, placeholder="", **kwargs):
        self.theme_manager = theme_manager
        self.placeholder = placeholder
        self.placeholder_active = False
        
        super().__init__(parent, **kwargs)
        self._setup_appearance()
        self._setup_placeholder()
        self.theme_manager.register_callback(self._on_theme_change)
    
    def _setup_appearance(self):
        theme = self.theme_manager.current_theme
        self.config(
            bg=theme.colors['bg_primary'],
            fg=theme.colors['fg_primary'],
            font=theme.fonts['default'],
            relief='solid',
            borderwidth=1,
            insertbackground=theme.colors['fg_primary']
        )
        self.config(highlightbackground=theme.colors['border'])
        self.config(highlightcolor=theme.colors['accent'])
    
    def _setup_placeholder(self):
        if self.placeholder:
            self.bind('<FocusIn>', self._on_focus_in)
            self.bind('<FocusOut>', self._on_focus_out)
            self._show_placeholder()
    
    def _show_placeholder(self):
        if not self.get():
            self.placeholder_active = True
            self.insert(0, self.placeholder)
            self.config(fg=self.theme_manager.get_color('fg_secondary'))
    
    def _hide_placeholder(self):
        if self.placeholder_active:
            self.placeholder_active = False
            self.delete(0, tk.END)
            self.config(fg=self.theme_manager.get_color('fg_primary'))
    
    def _on_focus_in(self, event):
        self._hide_placeholder()
    
    def _on_focus_out(self, event):
        if not self.get():
            self._show_placeholder()
    
    def _on_theme_change(self, theme):
        self._setup_appearance()

class ModernFrame(tk.Frame):
    def __init__(self, parent, theme_manager: ThemeManager, elevated=False, **kwargs):
        self.theme_manager = theme_manager
        self.elevated = elevated
        
        super().__init__(parent, **kwargs)
        self._setup_appearance()
        self.theme_manager.register_callback(self._on_theme_change)
    
    def _setup_appearance(self):
        theme = self.theme_manager.current_theme
        bg_color = theme.colors['bg_secondary'] if self.elevated else theme.colors['bg_primary']
        
        self.config(
            bg=bg_color,
            relief='flat' if not self.elevated else 'raised',
            borderwidth=0 if not self.elevated else 1
        )
    
    def _on_theme_change(self, theme):
        self._setup_appearance()

class Sidebar(ModernFrame):
    def __init__(self, parent, theme_manager: ThemeManager, width=250):
        super().__init__(parent, theme_manager, elevated=True)
        self.width = width
        self.is_collapsed = False
        self.menu_items = []
        
        self.config(width=width)
        self.pack_propagate(False)
        
        self._create_header()
        self._create_menu_area()
    
    def _create_header(self):
        self.header = ModernFrame(self, self.theme_manager)
        self.header.pack(fill='x', padx=10, pady=10)
        
        self.logo_label = tk.Label(
            self.header,
            text="App Framework",
            font=self.theme_manager.get_font('heading'),
            bg=self.theme_manager.get_color('bg_secondary'),
            fg=self.theme_manager.get_color('fg_primary')
        )
        self.logo_label.pack()
    
    def _create_menu_area(self):
        self.menu_frame = ModernFrame(self, self.theme_manager)
        self.menu_frame.pack(fill='both', expand=True, padx=5)
    
    def add_menu_item(self, text: str, command: Callable, icon: str = "•"):
        item_frame = ModernFrame(self.menu_frame, self.theme_manager)
        item_frame.pack(fill='x', pady=2)
        
        btn = tk.Button(
            item_frame,
            text=f"{icon}  {text}",
            command=command,
            bg=self.theme_manager.get_color('bg_secondary'),
            fg=self.theme_manager.get_color('fg_primary'),
            font=self.theme_manager.get_font('default'),
            relief='flat',
            anchor='w',
            padx=20,
            pady=8,
            cursor='hand2'
        )
        btn.pack(fill='x')
        
        # Hover effects
        def on_enter(e):
            btn.config(bg=self.theme_manager.get_color('hover'))
        
        def on_leave(e):
            btn.config(bg=self.theme_manager.get_color('bg_secondary'))
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        self.menu_items.append(btn)
        return btn

# =================== NAVIGATION SYSTEM ===================

class Page(ABC):
    def __init__(self, name: str, theme_manager: ThemeManager, state_manager: StateManager):
        self.name = name
        self.theme_manager = theme_manager
        self.state_manager = state_manager
        self.frame = None
        self.is_loaded = False
    
    @abstractmethod
    def create_content(self, parent) -> tk.Widget:
        pass
    
    def on_show(self):
        """Called when page becomes visible"""
        pass
    
    def on_hide(self):
        """Called when page becomes hidden"""
        pass
    
    def destroy(self):
        if self.frame:
            self.frame.destroy()
            self.frame = None
            self.is_loaded = False

class NavigationManager:
    def __init__(self, content_area, theme_manager: ThemeManager, state_manager: StateManager):
        self.content_area = content_area
        self.theme_manager = theme_manager
        self.state_manager = state_manager
        self.pages: Dict[str, Page] = {}
        self.current_page: Optional[Page] = None
        self.history: List[str] = []
    
    def register_page(self, page: Page):
        self.pages[page.name] = page
    
    def navigate_to(self, page_name: str):
        if page_name not in self.pages:
            return False
        
        # Hide current page
        if self.current_page:
            self.current_page.on_hide()
            if self.current_page.frame:
                self.current_page.frame.pack_forget()
        
        # Show new page
        page = self.pages[page_name]
        if not page.is_loaded:
            page.frame = page.create_content(self.content_area)
            page.is_loaded = True
        
        page.frame.pack(fill='both', expand=True)
        page.on_show()
        
        # Update history
        if not self.history or self.history[-1] != page_name:
            self.history.append(page_name)
        
        self.current_page = page
        self.state_manager.set_state('current_page', page_name)
        return True
    
    def go_back(self):
        if len(self.history) > 1:
            self.history.pop()  # Remove current page
            previous_page = self.history[-1]
            self.navigate_to(previous_page)

# =================== EXAMPLE PAGES ===================

class DashboardPage(Page):
    def create_content(self, parent) -> tk.Widget:
        frame = ModernFrame(parent, self.theme_manager)
        
        # Header
        header = tk.Label(
            frame,
            text="Dashboard",
            font=self.theme_manager.get_font('heading'),
            bg=self.theme_manager.get_color('bg_primary'),
            fg=self.theme_manager.get_color('fg_primary')
        )
        header.pack(pady=20)
        
        # Stats cards
        stats_frame = ModernFrame(frame, self.theme_manager)
        stats_frame.pack(fill='x', padx=20, pady=10)
        
        for i, (title, value, color) in enumerate([
            ("Total Users", "1,234", "accent"),
            ("Revenue", "$45,678", "success"),
            ("Orders", "89", "warning")
        ]):
            card = ModernFrame(stats_frame, self.theme_manager, elevated=True)
            card.pack(side='left', fill='both', expand=True, padx=10)
            
            tk.Label(
                card,
                text=title,
                font=self.theme_manager.get_font('small'),
                bg=self.theme_manager.get_color('bg_secondary'),
                fg=self.theme_manager.get_color('fg_secondary')
            ).pack(pady=(10, 5))
            
            tk.Label(
                card,
                text=value,
                font=self.theme_manager.get_font('heading'),
                bg=self.theme_manager.get_color('bg_secondary'),
                fg=self.theme_manager.get_color(color)
            ).pack(pady=(0, 10))
        
        # Chart placeholder
        chart_frame = ModernFrame(frame, self.theme_manager, elevated=True)
        chart_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(
            chart_frame,
            text="📊 Chart Area\n(Connect your preferred charting library)",
            font=self.theme_manager.get_font('default'),
            bg=self.theme_manager.get_color('bg_secondary'),
            fg=self.theme_manager.get_color('fg_secondary'),
            justify='center'
        ).pack(expand=True)
        
        return frame

class SettingsPage(Page):
    def create_content(self, parent) -> tk.Widget:
        frame = ModernFrame(parent, self.theme_manager)
        
        # Header
        header = tk.Label(
            frame,
            text="Settings",
            font=self.theme_manager.get_font('heading'),
            bg=self.theme_manager.get_color('bg_primary'),
            fg=self.theme_manager.get_color('fg_primary')
        )
        header.pack(pady=20)
        
        # Settings form
        form_frame = ModernFrame(frame, self.theme_manager, elevated=True)
        form_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Theme selector
        theme_frame = tk.Frame(form_frame, bg=self.theme_manager.get_color('bg_secondary'))
        theme_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Label(
            theme_frame,
            text="Theme:",
            font=self.theme_manager.get_font('subheading'),
            bg=self.theme_manager.get_color('bg_secondary'),
            fg=self.theme_manager.get_color('fg_primary')
        ).pack(anchor='w')
        
        theme_var = tk.StringVar(value='light')
        for theme_name in ['light', 'dark']:
            tk.Radiobutton(
                theme_frame,
                text=theme_name.title(),
                variable=theme_var,
                value=theme_name,
                command=lambda: self.theme_manager.set_theme(theme_var.get()),
                bg=self.theme_manager.get_color('bg_secondary'),
                fg=self.theme_manager.get_color('fg_primary'),
                selectcolor=self.theme_manager.get_color('accent'),
                font=self.theme_manager.get_font('default')
            ).pack(anchor='w', pady=2)
        
        # User preferences
        prefs_frame = tk.Frame(form_frame, bg=self.theme_manager.get_color('bg_secondary'))
        prefs_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Label(
            prefs_frame,
            text="User Preferences:",
            font=self.theme_manager.get_font('subheading'),
            bg=self.theme_manager.get_color('bg_secondary'),
            fg=self.theme_manager.get_color('fg_primary')
        ).pack(anchor='w', pady=(0, 10))
        
        # Username field
        tk.Label(
            prefs_frame,
            text="Username:",
            bg=self.theme_manager.get_color('bg_secondary'),
            fg=self.theme_manager.get_color('fg_primary'),
            font=self.theme_manager.get_font('default')
        ).pack(anchor='w')
        
        username_entry = ModernEntry(prefs_frame, self.theme_manager, placeholder="Enter username")
        username_entry.pack(fill='x', pady=(0, 10))
        
        # Email field
        tk.Label(
            prefs_frame,
            text="Email:",
            bg=self.theme_manager.get_color('bg_secondary'),
            fg=self.theme_manager.get_color('fg_primary'),
            font=self.theme_manager.get_font('default')
        ).pack(anchor='w')
        
        email_entry = ModernEntry(prefs_frame, self.theme_manager, placeholder="Enter email")
        email_entry.pack(fill='x', pady=(0, 20))
        
        # Save button
        save_btn = ModernButton(
            prefs_frame,
            self.theme_manager,
            text="Save Settings",
            primary=True,
            command=lambda: messagebox.showinfo("Settings", "Settings saved successfully!")
        )
        save_btn.pack()
        
        return frame

class DataPage(Page):
    def create_content(self, parent) -> tk.Widget:
        frame = ModernFrame(parent, self.theme_manager)
        
        # Header
        header = tk.Label(
            frame,
            text="Data Management",
            font=self.theme_manager.get_font('heading'),
            bg=self.theme_manager.get_color('bg_primary'),
            fg=self.theme_manager.get_color('fg_primary')
        )
        header.pack(pady=20)
        
        # Toolbar
        toolbar = ModernFrame(frame, self.theme_manager, elevated=True)
        toolbar.pack(fill='x', padx=20, pady=(0, 10))
        
        btn_frame = tk.Frame(toolbar, bg=self.theme_manager.get_color('bg_secondary'))
        btn_frame.pack(pady=10)
        
        ModernButton(btn_frame, self.theme_manager, text="Add", primary=True).pack(side='left', padx=(0, 10))
        ModernButton(btn_frame, self.theme_manager, text="Edit", outline=True).pack(side='left', padx=(0, 10))
        ModernButton(btn_frame, self.theme_manager, text="Delete").pack(side='left')
        
        # Data table area
        table_frame = ModernFrame(frame, self.theme_manager, elevated=True)
        table_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Create a simple table using Treeview
        style = ttk.Style()
        style.theme_use('clam')
        
        columns = ('ID', 'Name', 'Email', 'Status')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Define headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        # Add sample data
        sample_data = [
            (1, 'John Doe', 'john@example.com', 'Active'),
            (2, 'Jane Smith', 'jane@example.com', 'Inactive'),
            (3, 'Bob Johnson', 'bob@example.com', 'Active'),
            (4, 'Alice Brown', 'alice@example.com', 'Pending'),
        ]
        
        for item in sample_data:
            tree.insert('', tk.END, values=item)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        return frame

# =================== MAIN APPLICATION ===================

class ModernAppFramework:
    def __init__(self):
        self.root = tk.Tk()
        self.theme_manager = ThemeManager()
        self.state_manager = StateManager()
        
        self._setup_window()
        self._setup_layout()
        self._setup_navigation()
        self._setup_menu()
        
        # Initialize with dashboard
        self.nav_manager.navigate_to('dashboard')
    
    def _setup_window(self):
        self.root.title("Modern App Framework")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Configure styles
        self.root.configure(bg=self.theme_manager.get_color('bg_primary'))
        
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.root.winfo_screenheight() // 2) - (800 // 2)
        self.root.geometry(f"1200x800+{x}+{y}")
    
    def _setup_layout(self):
        # Main container
        self.main_container = ModernFrame(self.root, self.theme_manager)
        self.main_container.pack(fill='both', expand=True)
        
        # Sidebar
        self.sidebar = Sidebar(self.main_container, self.theme_manager)
        self.sidebar.pack(side='left', fill='y')
        
        # Content area
        self.content_area = ModernFrame(self.main_container, self.theme_manager)
        self.content_area.pack(side='right', fill='both', expand=True)
    
    def _setup_navigation(self):
        self.nav_manager = NavigationManager(
            self.content_area,
            self.theme_manager,
            self.state_manager
        )
        
        # Register pages
        pages = [
            DashboardPage('dashboard', self.theme_manager, self.state_manager),
            DataPage('data', self.theme_manager, self.state_manager),
            SettingsPage('settings', self.theme_manager, self.state_manager)
        ]
        
        for page in pages:
            self.nav_manager.register_page(page)
    
    def _setup_menu(self):
        menu_items = [
            ("Dashboard", lambda: self.nav_manager.navigate_to('dashboard'), "📊"),
            ("Data", lambda: self.nav_manager.navigate_to('data'), "📋"),
            ("Settings", lambda: self.nav_manager.navigate_to('settings'), "⚙️")
        ]
        
        for text, command, icon in menu_items:
            self.sidebar.add_menu_item(text, command, icon)
    
    def add_custom_page(self, page: Page):
        """Add a custom page to the application"""
        self.nav_manager.register_page(page)
    
    def add_menu_item(self, text: str, command: Callable, icon: str = "•"):
        """Add a custom menu item"""
        return self.sidebar.add_menu_item(text, command, icon)
    
    def run(self):
        """Start the application"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.root.quit()

# =================== EXAMPLE USAGE ===================

if __name__ == "__main__":
    # Create and run the application
    app = ModernAppFramework()
    
    # Example of adding a custom page
    class CustomPage(Page):
        def create_content(self, parent) -> tk.Widget:
            frame = ModernFrame(parent, self.theme_manager)
            
            tk.Label(
                frame,
                text="Custom Page",
                font=self.theme_manager.get_font('heading'),
                bg=self.theme_manager.get_color('bg_primary'),
                fg=self.theme_manager.get_color('fg_primary')
            ).pack(pady=50)
            
            tk.Label(
                frame,
                text="This is a custom page added to the framework!",
                font=self.theme_manager.get_font('default'),
                bg=self.theme_manager.get_color('bg_primary'),
                fg=self.theme_manager.get_color('fg_secondary')
            ).pack()
            
            return frame
    
    # Add custom page and menu item
    custom_page = CustomPage('custom', app.theme_manager, app.state_manager)
    app.add_custom_page(custom_page)
    app.add_menu_item("Custom", lambda: app.nav_manager.navigate_to('custom'), "🎨")
    
    # Run the application
    app.run()
