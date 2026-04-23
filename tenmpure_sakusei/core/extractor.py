def format_H1_nmr(h1_data):
    """
    1H NMRを論文形式の文字列に変換
    """
    if not h1_data:
        return ""

    parts = []

    for ppm, info in sorted(h1_data.items(), key=lambda x: float(x[0])):
        mult = info.get("mult", "")
        J = info.get("J", "")
        H = info.get("H", "")

        text = f"{ppm} ({mult}"

        if J:
            text += f", J = {J} Hz"

        if H:
            text += f", {H}H"

        text += ")"

        parts.append(text)

    return ", ".join(parts)


def format_C13_nmr(c13_list):
    """
    13C NMR（単純リスト想定）
    """
    if not c13_list:
        return ""

    return ", ".join([str(x) for x in sorted(c13_list)])


def format_F19_nmr(f19_data):
    """
    19F NMR
    """
    if not f19_data:
        return ""

    parts = []

    for ppm, info in sorted(f19_data.items(), key=lambda x: float(x[0])):
        mult = info.get("mult", "s")
        H = info.get("H", "")

        text = f"{ppm} ({mult}"

        if H:
            text += f", {H}F"

        text += ")"

        parts.append(text)

    return ", ".join(parts)


def extract_nmr_text(raw_data):
    """
    raw_data → Word用フォーマット辞書
    """

    return {
        "1H": format_H1_nmr(raw_data.get("1H", {})),
        "13C": format_C13_nmr(raw_data.get("13C", [])),
        "19F": format_F19_nmr(raw_data.get("19F", {})),
    }