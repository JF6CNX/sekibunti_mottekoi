import json
import os

from nmr_manager.paths import TEMPLATE_FILE, ensure_data_dir

def load_templates():
    ensure_data_dir()

    if os.path.exists(TEMPLATE_FILE):
        try:
            with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
            
        except Exception:
            return {}
        
    return {}

def save_templates(data):
    ensure_data_dir()

    with open(TEMPLATE_FILE, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False,
        )