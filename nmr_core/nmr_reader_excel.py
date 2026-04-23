import os
import xml.etree.ElementTree as ET


def find_valid_experiments(base_path):
    valid = []

    for exp in os.listdir(base_path):
        exp_path = os.path.join(base_path, exp)
        pdata_path = os.path.join(exp_path, "pdata", "1")

        if not os.path.isdir(pdata_path):
            continue

        peak_xml = os.path.join(pdata_path, "peaklist.xml")

        if os.path.exists(peak_xml):
            valid.append(exp_path)

    return valid


def get_nucleus(acqus_path):
    with open(acqus_path) as f:
        for line in f:
            if "NUC1" in line:
                return line.split("=")[1].strip().replace("<", "").replace(">", "")


def read_peaklist_xml(path):
    tree = ET.parse(path)
    root = tree.getroot()

    peaks = []
    for peak in root.iter("Peak"):
        pos = peak.find("Position")
        if pos is not None:
            try:
                peaks.append(float(pos.text))
            except:
                pass

    return sorted(peaks, reverse=True)


def read_integrals(path):
    integrals = []

    with open(path) as f:
        for line in f:
            parts = line.split()
            if len(parts) >= 2:
                try:
                    integrals.append(float(parts[1]))
                except:
                    pass

    return integrals


def read_nmr_folder(base_path):
    results = {}

    experiments = find_valid_experiments(base_path)

    for exp_path in experiments:
        acqus = os.path.join(exp_path, "acqus")
        pdata = os.path.join(exp_path, "pdata", "1")

        nucleus = get_nucleus(acqus)

        peak_xml = os.path.join(pdata, "peaklist.xml")
        peaks = read_peaklist_xml(peak_xml)

        integrals = None
        int_file = os.path.join(pdata, "integrals.txt")

        if nucleus == "1H" and os.path.exists(int_file):
            integrals = read_integrals(int_file)

        results[nucleus] = {
            "peaks": peaks,
            "integrals": integrals
        }

    return results