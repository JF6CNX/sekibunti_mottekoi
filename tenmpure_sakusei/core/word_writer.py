from docx import Document


def write_word(data, output_path="nmr_output.docx"):
    doc = Document()

    # 1H
    if "1H" in data:
        peaks = data["1H"]["peaks"]
        integrals = data["1H"]["integrals"]

        if integrals:
            text = ", ".join(
                f"{p:.2f} ({i:.1f}H)"
                for p, i in zip(peaks, integrals)
            )
        else:
            text = ", ".join(f"{p:.2f}" for p in peaks)

        doc.add_paragraph(f"1H NMR δ: {text}")

    # 13C
    if "13C" in data:
        peaks = data["13C"]["peaks"]
        text = ", ".join(f"{p:.1f}" for p in peaks)
        doc.add_paragraph(f"13C NMR δ: {text}")

    # 19F
    if "19F" in data:
        peaks = data["19F"]["peaks"]
        text = ", ".join(f"{p:.1f}" for p in peaks)
        doc.add_paragraph(f"19F NMR δ: {text}")

    doc.save(output_path)