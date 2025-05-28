import json
import os

class LanguageManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LanguageManager, cls).__new__(cls)
            cls._instance.translations = {}
            cls._instance.current_language = "en" # Default
            cls._instance.language_dir = os.path.join(os.path.dirname(__file__), "..", "languages")
        return cls._instance

    def load_language(self, lang_code):
        filepath = os.path.join(self.language_dir, f"{lang_code}.json")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.translations = json.load(f)
                self.current_language = lang_code
            print(f"Loaded language: {lang_code}")
        except FileNotFoundError:
            print(f"Language file not found: {filepath}. Loading English default.")
            if lang_code != "en": # Prevent infinite recursion if en.json is missing
                self.load_language("en") # Fallback to English
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {filepath}. Check file format.")
            if lang_code != "en":
                self.load_language("en")

    def get_text(self, key, *args):
        text = self.translations.get(key, f"MISSING_TEXT:{key}")
        return text.format(*args) if args else text

    def get_current_language(self):
        return self.current_language

    def set_language(self, lang_code):
        self.load_language(lang_code)