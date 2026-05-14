import os
import sys

def get_base_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__),"..")
        )

BASE_DIR = get_base_dir()
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")
TEMPLATE_FILE = os.path.join(DATA_DIR, "nmr_v12_final.json")

def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)
