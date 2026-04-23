import os
import xml.etree.ElementTree as ET


def read_integrals(file_path):
    data = []
    with open(file_path, "r") as f:
        for line in f:
            parts = line.split()
            if len(parts) != 4:
                continue
            try:
                start = float(parts[1])
                end = float(parts[2])
                integral = float(parts[3])
                center = (start + end) / 2
                data.append({"ppm": center, "H": round(integral)})
            except:
                continue
    return data


def read_multiplet(file_path):
    mults = []
    with open(file_path, "r") as f:
        for line in f:
            parts = line.split()
            if len(parts) >= 2:
                try:
                    ppm = float(parts[0])
                    mult = parts[1]
                    mults.append({"ppm": ppm, "mult": mult})
                except:
                    continue
    return mults


def read_peaklist(xml_path):
    peaks = []
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        for peak in root.iter("Peak"):
            ppm = float(peak.attrib.get("F1", 0))
            peaks.append(ppm)
    except:
        pass
    return peaks


def read_nmr_folder(base_path):

    result = {
        "1H": [],
        "13C": []
    }

    for root, dirs, files in os.walk(base_path):

        if "integrals.txt" in files:
            integrals = read_integrals(os.path.join(root, "integrals.txt"))

            multiplet = []
            if "multiplet.txt" in files:
                multiplet = read_multiplet(os.path.join(root, "multiplet.txt"))

            # マージ（ppm近いもの同士）
            for i, peak in enumerate(integrals):
                entry = peak.copy()

                if i < len(multiplet):
                    entry["mult"] = multiplet[i]["mult"]
                else:
                    entry["mult"] = "s"

                result["1H"].append(entry)

        if "peaklist.xml" in files and "13C" in root:
            peaks = read_peaklist(os.path.join(root, "peaklist.xml"))
            result["13C"] = peaks

    return result