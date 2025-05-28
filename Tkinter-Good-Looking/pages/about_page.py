import tkinter as tk
from core.components import ModernButton

class AboutPage:
    def __init__(self, parent_frame, colors, lang_manager, open_website_cmd, open_docs_cmd, open_issues_cmd, open_support_cmd):
        self.parent_frame = parent_frame
        self.colors = colors
        self.lang = lang_manager
        self.open_website_cmd = open_website_cmd
        self.open_docs_cmd = open_docs_cmd
        self.open_issues_cmd = open_issues_cmd
        self.open_support_cmd = open_support_cmd

    def create_ui(self):
        # Center content
        center_frame = tk.Frame(self.parent_frame, bg=self.colors['background'])
        center_frame.pack(expand=True, fill=tk.BOTH)
        
        content = tk.Frame(center_frame, bg=self.colors['background'])
        content.place(relx=0.5, rely=0.5, anchor="center")
        
        # App icon
        app_icon = tk.Label(content, text="🚀", font=("Segoe UI Emoji", 80),
                            bg=self.colors['background'])
        app_icon.pack(pady=(0, 20))
        
        # App name
        app_name = tk.Label(content, text=self.lang.get_text("app_title"), 
                            font=("Segoe UI", 32, "bold"),
                            bg=self.colors['background'], fg=self.colors['text_primary'])
        app_name.pack()
        
        # Version
        version = tk.Label(content, text=self.lang.get_text("app_version"), font=("Segoe UI", 16),
                           bg=self.colors['background'], fg=self.colors['text_secondary'])
        version.pack(pady=10)
        
        # Description
        desc = tk.Label(content, text=self.lang.get_text("app_description"),
                        font=("Segoe UI", 14), bg=self.colors['background'], 
                        fg=self.colors['text_secondary'], justify=tk.CENTER)
        desc.pack(pady=20)
        
        # Links frame
        links_frame = tk.Frame(content, bg=self.colors['background'])
        links_frame.pack(pady=30)
        
        # Link buttons
        links = [
            (self.lang.get_text("link_website"), self.open_website_cmd),
            (self.lang.get_text("link_documentation"), self.open_docs_cmd),
            (self.lang.get_text("link_report_issue"), self.open_issues_cmd),
            (self.lang.get_text("link_support"), self.open_support_cmd)
        ]
        
        for text, command in links:
            btn = ModernButton(links_frame, text=text, command=command,
                               bg_color="#6b7280", hover_color="#4b5563",
                               padding=(15, 8))
            btn.pack(side=tk.LEFT, padx=5)
            
        # Copyright
        copyright_label = tk.Label(content, text=self.lang.get_text("copyright_info"),
                             font=("Segoe UI", 10), bg=self.colors['background'], 
                             fg=self.colors['text_muted'])
        copyright_label.pack(pady=(40, 0))