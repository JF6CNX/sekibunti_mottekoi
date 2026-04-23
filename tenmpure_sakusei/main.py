import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from nmr_core.nmr_reader import read_nmr_folder
from core.word_writer import write_word


if __name__ == "__main__":
    folder = "sample_data"  # ← 自分のNMRフォルダに変更

    data = read_nmr_folder(folder)

    print(data)  # デバッグ用

    write_word(data, "output.docx")