import os
import re
from collections import defaultdict
from openpyxl import Workbook

# ===== 事前確認 =====
print("====================================")
print("Excelファイルを閉じてください")
print("閉じたら Enter を押すと処理を開始します")
print("====================================")
input(">>> Enterで開始：")

# ===== 設定 =====
base_dir = r"C:/Users/haruk/chem/nmr"
output_path = r"C:/Users/haruk/OneDrive - Kyushu Institute Of Technolgy/ドキュメント/lab/program/sekibunti_mottekoi/number_horizontal.xlsx"

# ===== データ構造 =====
data = defaultdict(lambda: defaultdict(dict))
number_set = set()

# ★ サンプルごとppm範囲
ppm_range = defaultdict(dict)

# ===== ファイル探索 =====
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file == "integrals.txt":

            try:
                folder_name = os.path.basename(
                    os.path.dirname(os.path.dirname(os.path.dirname(root)))
                )

                parts = folder_name.split("_")
                if len(parts) < 2:
                    continue

                # ===== reも含めてそのまま使う =====
                time_label = parts[-1]
                sample = "_".join(parts[:-1])

                # ===== 時間データのみ =====
                if not re.match(r"\d+[dh]", time_label, re.IGNORECASE):
                    continue

                file_path = os.path.join(root, file)

                with open(file_path, "r") as f:
                    for line in f:
                        parts = line.split()

                        if len(parts) == 4:
                            try:
                                number = int(parts[0])
                                start = float(parts[1])
                                end = float(parts[2])
                                integral = float(parts[3])

                                data[sample][time_label][number] = integral
                                number_set.add(number)

                                if number not in ppm_range[sample]:
                                    ppm_range[sample][number] = (start, end)

                            except:
                                continue

            except:
                continue

# ===== Number一覧 =====
number_list = sorted(number_set)

# ===== Excel作成 =====
wb = Workbook()
wb.remove(wb.active)

for sample, time_dict in data.items():
    ws = wb.create_sheet(title=sample)

    # 1行目
    ws.append(["time"] + number_list)

    # 2行目（ppm）
    ppm_row = ["ppm"]
    for num in number_list:
        if num in ppm_range[sample]:
            s, e = ppm_range[sample][num]
            ppm_row.append(f"{s:.2f}–{e:.2f}")
        else:
            ppm_row.append("")
    ws.append(ppm_row)

    # 時間順
    def time_sort(t):
        return int(re.findall(r"\d+", t)[0])

    for time in sorted(time_dict.keys(), key=time_sort):
        row = [time]
        for num in number_list:
            row.append(data[sample][time].get(num, ""))
        ws.append(row)

# ===== 保存 =====
while True:
    try:
        wb.save(output_path)
        print("\n 保存完了")
        print(f"保存先: {output_path}")
        break
    except PermissionError:
        input("\n Excelを閉じてからEnterを押してください：")