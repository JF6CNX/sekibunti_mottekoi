def format_1H(data):

    peaks = sorted(data, key=lambda x: -x["ppm"])

    parts = []
    for p in peaks:
        ppm = f"{p['ppm']:.2f}"
        mult = p.get("mult", "s")
        H = p.get("H", 1)

        parts.append(f"{ppm} ({mult}, {H}H)")

    return ", ".join(parts)


def format_13C(data):

    peaks = sorted(data, reverse=True)
    return ", ".join([f"{p:.1f}" for p in peaks])


def build_template(exp_id, data):

    h_text = format_1H(data.get("1H", []))
    c_text = format_13C(data.get("13C", []))

    return {
        "id": exp_id,
        "structure": "",
        "H1": f"1H NMR (500 MHz, CDCl3) δ {h_text}." if h_text else "",
        "C13": f"13C{{1H}} NMR (125 MHz, CDCl3) δ {c_text}." if c_text else "",
        "F19": ""
    }