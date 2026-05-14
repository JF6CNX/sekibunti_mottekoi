import datetime
import os

from nmr_excelsekibunti.core.excel_writer import write_excel_from_integrals_multi

def export_selected_samples(
        settings,
        selected_samples,
        sample_groups,
        sample_order_map,
        ):

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}.xlsx"

    output_path = os.path.join(settings["output_dir"], filename)

    count = 0

    for sample_name in selected_samples:
        dirs = [
            os.path.join(settings["input_dir"], dirname)
            for dirname in sample_groups[sample_name]
        ]

        order = sample_order_map.get(sample_name,[])

        if not order:
            continue

        write_excel_from_integrals_multi(
            dirs,
            output_path,
            number_order=order,
            append=(count > 0),
        )

        count += 1

    return output_path, filename, count




