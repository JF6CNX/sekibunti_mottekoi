import os
import re
from collections import defaultdict

def load_nmr_data(base_dir):
    data = defaultdict(lambda: defaultdict(dict))
    number_set = set()
    ppm_range = defaultdict(dict)

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file != "integrals.txt":
                continue

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
                        if len(parts) != 4:
                            continue

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

    return data, number_set, ppm_range