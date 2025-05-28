import tkinter as tk
from core.components import GlassCard

class StatisticsPage:
    def __init__(self, parent_frame, colors, lang_manager):
        self.parent_frame = parent_frame
        self.colors = colors
        self.lang = lang_manager

    def create_ui(self):
        # Page header
        header = tk.Frame(self.parent_frame, bg=self.colors['background'])
        header.pack(fill=tk.X, pady=(0, 30))
        
        title = tk.Label(header, text=self.lang.get_text("page_statistics_title"), font=("Segoe UI", 28, "bold"),
                         bg=self.colors['background'], fg=self.colors['text_primary'])
        title.pack(anchor="w")
        
        subtitle = tk.Label(header, text=self.lang.get_text("page_statistics_subtitle"),
                            font=("Segoe UI", 14), bg=self.colors['background'], 
                            fg=self.colors['text_secondary'])
        subtitle.pack(anchor="w", pady=(5, 0))
        
        # Statistics grid
        stats_grid = tk.Frame(self.parent_frame, bg=self.colors['background'])
        stats_grid.pack(fill=tk.BOTH, expand=True)
        stats_grid.grid_columnconfigure(0, weight=1)
        stats_grid.grid_columnconfigure(1, weight=1)
        stats_grid.grid_columnconfigure(2, weight=1)
        
        # Stats cards
        stats_data = [
            ("📦", self.lang.get_text("stat_total_builds"), "42", self.colors['primary']),
            ("✅", self.lang.get_text("stat_successful"), "38", self.colors['success']),
            ("⚠️", self.lang.get_text("stat_failed"), "4", self.colors['error']),
            ("⏱️", self.lang.get_text("stat_avg_time"), "2m 34s", self.colors['secondary']),
            ("💾", self.lang.get_text("stat_total_size"), "1.2 GB", self.colors['accent']),
            ("📅", self.lang.get_text("stat_last_build"), "2h ago", self.colors['text_secondary'])
        ]
        
        for i, (icon, label_key, value, color) in enumerate(stats_data):
            row, col = divmod(i, 3)
            self._create_stat_card(stats_grid, icon, label_key, value, color, row, col)
            
        # Recent builds card
        recent_card = GlassCard(stats_grid, title=self.lang.get_text("card_recent_builds_title"), subtitle=self.lang.get_text("card_recent_builds_subtitle"), colors=self.colors)
        recent_card.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(20, 0))
        
        recent_content = tk.Frame(recent_card, bg="white")
        recent_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 25))
        
        # Table headers
        headers_frame = tk.Frame(recent_content, bg="#f8fafc", height=35)
        headers_frame.pack(fill=tk.X, pady=(10, 0))
        headers_frame.pack_propagate(False)
        
        headers = [
            self.lang.get_text("table_header_project"),
            self.lang.get_text("table_header_status"),
            self.lang.get_text("table_header_size"),
            self.lang.get_text("table_header_time"),
            self.lang.get_text("table_header_date")
        ]
        for i, header_text in enumerate(headers):
            label = tk.Label(headers_frame, text=header_text, font=("Segoe UI", 11, "bold"),
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
                
    def _create_stat_card(self, parent, icon, label_key, value, color, row, col):
        """Create a statistics card"""
        card = GlassCard(parent, height=120, colors=self.colors)
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
        label_label = tk.Label(content, text=self.lang.get_text(label_key), font=("Segoe UI", 11),
                              bg="white", fg=self.colors['text_secondary'])
        label_label.pack(anchor="w")
