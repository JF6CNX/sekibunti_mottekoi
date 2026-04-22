from core.nmr_reader import load_nmr_data
from core.excel_writer import write_excel

# ===== 設定 =====
base_dir = r"C:/Users/haruk/chem/nmr"
output_path = r"C:/Users/haruk/OneDrive - Kyushu Institute Of Technolgy/ドキュメント/lab/program/sekibunti_mottekoi/number_horizontal.xlsx"

# ===== 実行 =====
print("Excelを閉じてEnter")
input()

data, number_set, ppm_range = load_nmr_data(base_dir)

write_excel(data, number_set, ppm_range, output_path)