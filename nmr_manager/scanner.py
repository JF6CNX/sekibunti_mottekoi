import os
import re

def scan_samples(input_dir):
    sample_groups = {}

    if not os.path.exists(input_dir):
        return {}
    
    for dirname in os.listdir(input_dir):
        full_path = os.path.join(input_dir, dirname)

        if not os.path.isdir(full_path):
            continue

        name_clean = os.path.splitext(dirname)[0]

        pattern = (
            r"^([A-Za-z0-9]+"
            r"[-_・ｿ]"
            r"[A-Za-z0-9]+"
            r"[-_・ｿ]"
            r"\d{3})"
        )

        match = re.match(pattern, name_clean)

        if match:
            base = match.group(1)
        else:
            split_match = re.search(
                r"^(.*)[-_・ｿ][^-_・ｿ]+$",
                name_clean,
            )

            base = split_match.group(1) if split_match else name_clean

        sample_groups.setdefault(base, []).append(dirname)

    return sample_groups
