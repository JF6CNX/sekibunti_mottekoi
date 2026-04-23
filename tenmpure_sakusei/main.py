import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

from nmr_core.nmr_reader_word import read_nmr_folder
from tenmpure_sakusei.core.formatter import build_template
from tenmpure_sakusei.core.word_writer import write_word


input_dir = os.path.join(BASE_DIR, "input")
output_dir = os.path.join(BASE_DIR, "output")

os.makedirs(output_dir, exist_ok=True)


for folder in os.listdir(input_dir):

    folder_path = os.path.join(input_dir, folder)

    if not os.path.isdir(folder_path):
        continue

    try:
        raw_data = read_nmr_folder(folder_path)

        template = build_template(folder, raw_data)

        output_path = os.path.join(output_dir, f"{folder}.docx")

        if os.path.exists(output_path):
            try:
                os.remove(output_path)
            except:
                print("閉じてください:", output_path)
                continue

        write_word(template, output_path)

        print("OK:", folder)

    except Exception as e:
        print("ERROR:", folder, e)

