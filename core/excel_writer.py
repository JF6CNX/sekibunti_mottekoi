import re
from openpyxl import Workbook
from collections import defaultdict

def write_excel(data, number_set, ppm_range, output_path):

    number_list = sorted(number_set)
    wb = Workbook()
    wb.remove(wb.active)

    for sample, time_dict in data.items():
        ws = wb.create_sheet(title=sample)

        ws.append(["time"] + number_list)

        ppm_row = ["ppm"]
        for num in number_list:
            if num in ppm_range[sample]:
                s, e = ppm_range[sample][num]
                ppm_row.append(f"{s:.2f}–{e:.2f}")
            else:
                ppm_row.append("")
        ws.append(ppm_row)

        def time_sort(t):
            return int(re.findall(r"\d+", t)[0])

        for time in sorted(time_dict.keys(), key=time_sort):
            row = [time]
            for num in number_list:
                row.append(data[sample][time].get(num, ""))
            ws.append(row)

    while True:
        try:
            wb.save(output_path)
            print("保存完了")
            print(output_path)
            break
        except PermissionError:
            input("Excelを閉じてEnter")