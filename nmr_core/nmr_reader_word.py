import os
import re


def read_integrals(file_path):
    values = []

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            try:
                values.append(float(line.strip()))
            except:
                continue

    return values


def read_peaks(file_path):
    peaks = []
    j_values = []

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            nums = re.findall(r"[-+]?\d*\.\d+|\d+", line)

            if len(nums) >= 1:
                peaks.append(float(nums[0]))

            if len(nums) >= 2:
                j_values.append(float(nums[1]))

    return peaks, j_values


def read_nmr_folder(folder_path):
    result = {}

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file == "integrals.txt":
                result.setdefault("1H", {})["integrals"] = read_integrals(
                    os.path.join(root, file)
                )

            elif file == "peaks":
                peaks, j = read_peaks(os.path.join(root, file))
                result.setdefault("1H", {})["peaks"] = peaks
                result["1H"]["J"] = j

    return result