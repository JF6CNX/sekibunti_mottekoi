import json
import os

from nmr_manager.paths import OUTPUT_DIR, SETTINGS_FILE, ensure_data_dir

DEFAULT_SETTINGS = {
    "input_dir" : r"C:/Users/haruk/chem/nmr",
    "output_dir" : OUTPUT_DIR,
    "theme_mode" : "dark",
    "auto_open_excel" : True,
}

def load_settings():
    ensure_data_dir()

    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            for key, value in DEFAULT_SETTINGS.items():
                if key not in data:
                    data[key] = value

            return data
        
        except Exception:
            return DEFAULT_SETTINGS.copy()
        
    return DEFAULT_SETTINGS.copy()

def save_settings(data):
    ensure_data_dir()

    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False,
        )

