import os
import re
from collections import defaultdict
from openpyxl import Workbook


def write_excel_from_integrals_multi(base_dirs, output_path, number_order=None):

    data = defaultdict(lambda: defaultdict(dict))
    number_set = set()
    ppm_range = defaultdict(dict)

    # ===== 複数フォルダ対応 =====
    for base_dir in base_dirs:

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

                        time_label = parts[-1]
                        sample = "_".join(parts[:-1])

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

    # ===== Excel =====
    wb = Workbook()
    wb.remove(wb.active)

    number_list = number_order if number_order else sorted(number_set)

    for sample, time_dict in data.items():
        ws = wb.create_sheet(title=sample[:31])

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
            m = re.findall(r"\d+", t)
            return int(m[0]) if m else 0

        for time in sorted(time_dict.keys(), key=time_sort):
            row = [time]
            for num in number_list:
                row.append(data[sample][time].get(num, ""))
            ws.append(row)

    wb.save(output_path)