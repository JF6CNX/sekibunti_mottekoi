import datetime
import os
import shutil

from nmr_manager.paths import DATA_DIR, ensure_data_dir


def _normalize_output_dir(output_dir):
    return os.path.abspath(output_dir)


def _is_excel_file(path):
    return os.path.isfile(path) and path.lower().endswith(".xlsx")


def _is_inside_output_dir(path, output_dir):
    path = os.path.abspath(path)
    output_dir = _normalize_output_dir(output_dir)
    return os.path.commonpath([path, output_dir]) == output_dir


def list_excel_files(output_dir):
    output_dir = _normalize_output_dir(output_dir)

    if not os.path.exists(output_dir):
        return []

    files = []

    for filename in os.listdir(output_dir):
        path = os.path.join(output_dir, filename)

        if not _is_excel_file(path):
            continue

        modified_at = os.path.getmtime(path)
        files.append(
            {
                "name": filename,
                "path": path,
                "size": os.path.getsize(path),
                "modified_at": modified_at,
                "modified_label": datetime.datetime.fromtimestamp(
                    modified_at
                ).strftime("%Y-%m-%d %H:%M"),
            }
        )

    return sorted(files, key=lambda item: item["modified_at"], reverse=True)


def format_file_size(size):
    if size < 1024:
        return f"{size} B"

    if size < 1024 * 1024:
        return f"{size / 1024:.1f} KB"

    return f"{size / (1024 * 1024):.1f} MB"


def delete_excel_file(path, output_dir):
    if not _is_inside_output_dir(path, output_dir):
        raise ValueError("File is outside the output folder")

    if not _is_excel_file(path):
        raise ValueError("File is not an Excel file")

    os.remove(path)


def delete_all_excel_files(output_dir):
    deleted_count = 0

    for item in list_excel_files(output_dir):
        delete_excel_file(item["path"], output_dir)
        deleted_count += 1

    return deleted_count


def get_excel_trash_dir():
    ensure_data_dir()
    trash_dir = os.path.join(DATA_DIR, "excel_trash")
    os.makedirs(trash_dir, exist_ok=True)
    return trash_dir


def move_excel_file_to_trash(path, output_dir):
    if not _is_inside_output_dir(path, output_dir):
        raise ValueError("File is outside the output folder")

    if not _is_excel_file(path):
        raise ValueError("File is not an Excel file")

    trash_dir = get_excel_trash_dir()
    filename = os.path.basename(path)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    trash_path = os.path.join(trash_dir, f"{timestamp}_{filename}")
    shutil.move(path, trash_path)

    return {
        "original_path": path,
        "trash_path": trash_path,
    }


def move_all_excel_files_to_trash(output_dir):
    moved_files = []

    for item in list_excel_files(output_dir):
        moved_files.append(move_excel_file_to_trash(item["path"], output_dir))

    return moved_files


def restore_excel_files(moved_files):
    restored_count = 0

    for item in moved_files:
        original_path = item["original_path"]
        trash_path = item["trash_path"]

        if not os.path.exists(trash_path):
            continue

        os.makedirs(os.path.dirname(original_path), exist_ok=True)

        if os.path.exists(original_path):
            root, ext = os.path.splitext(original_path)
            original_path = f"{root}_restored{ext}"

        shutil.move(trash_path, original_path)
        restored_count += 1

    return restored_count
