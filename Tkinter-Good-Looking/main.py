import tkinter as tk
from core.gui_app import PremiumNuitkaGUI
from core.language_manager import LanguageManager

def main():
    root = tk.Tk()
    
    # Initialize language manager
    lang_manager = LanguageManager()
    lang_manager.load_language("zh-TW") # Default language
    
    app = PremiumNuitkaGUI(root, lang_manager)
    root.mainloop()

if __name__ == "__main__":
    main()