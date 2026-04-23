import os
import sys

# ===== パス設定 =====
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

from nmr_excelsekibunti.core.excel_writer import write_excel_from_integrals

# ===== 入力 =====
base_dir = r"C:/Users/haruk/chem/nmr"

# ===== 出力フォルダ =====
output_dir = os.path.join(os.path.dirname(__file__), "..", "output")
os.makedirs(output_dir, exist_ok=True)

# ===== 出力ファイル（固定）=====
output_path = os.path.join(output_dir, "result.xlsx")

print("====================================")
print("Excelファイルを閉じてください")
print("====================================")
input("Enterで開始")

write_excel_from_integrals(base_dir, output_path)

print("保存完了:", output_path)