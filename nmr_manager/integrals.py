import os

def extract_numbers_and_ppm(dirs):
    numbers = set()
    ppm_map = {}

    for base in dirs:
        if not os.path.exists(base):
            continue

        for root, _, files in os.walk(base):
            for filename in files:
                if "integrals" not in filename.lower():
                    continue

                path = os.path.join(root, filename)

                try:
                    with open(path, encoding="utf-8", errors="ignore") as f:
                        for line in f:
                            parts = line.split()

                            if len(parts) < 4:
                                continue

                            try:
                                number = int(parts[0])
                                start = float(parts[1])
                                end = float(parts[2])

                                numbers.add(number)

                                if number not in ppm_map:
                                    ppm_map[number] = (start,end)

                            except Exception:
                                pass

                except Exception:
                    pass

    return sorted(numbers), ppm_map
