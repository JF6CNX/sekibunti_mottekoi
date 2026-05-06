import flet as ft
import os
import sys
import datetime
import json

BASE_DIR = os.path.dirname(__file__)
sys.path.append(BASE_DIR)

from nmr_excelsekibunti.core.excel_writer import write_excel_from_integrals_multi

INPUT_DIR = r"C:/Users/haruk/chem/nmr"
TEMPLATE_FILE = os.path.join(BASE_DIR, "templates.json")


# =========================
# テンプレ管理
# =========================
def load_templates():
    if os.path.exists(TEMPLATE_FILE):
        with open(TEMPLATE_FILE, "r") as f:
            return json.load(f)
    return {}


def save_templates(data):
    with open(TEMPLATE_FILE, "w") as f:
        json.dump(data, f, indent=2)


# =========================
# ナンバー + ppm 抽出
# =========================
def extract_numbers_and_ppm(dirs):
    numbers = set()
    ppm_map = {}

    for base in dirs:
        for root, _, files in os.walk(base):
            for file in files:
                if "integrals" in file.lower():

                    path = os.path.join(root, file)

                    try:
                        with open(path, encoding="utf-8", errors="ignore") as f:
                            for line in f:
                                parts = line.split()

                                if len(parts) >= 4:
                                    try:
                                        num = int(parts[0])
                                        start = float(parts[1])
                                        end = float(parts[2])

                                        numbers.add(num)

                                        if num not in ppm_map:
                                            ppm_map[num] = (start, end)

                                    except:
                                        pass
                    except:
                        pass

    return sorted(numbers), ppm_map


# =========================
# メイン
# =========================
def main(page: ft.Page):

    page.title = "NMR Tool"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#1e1e1e"

    templates = load_templates()

    # ===== サンプル取得 =====
    sample_groups = {}

    for d in os.listdir(INPUT_DIR):
        full = os.path.join(INPUT_DIR, d)

        if os.path.isdir(full) and d.startswith("TTH"):
            base = d.split("_")[0]
            sample_groups.setdefault(base, []).append(d)

    samples = sorted(sample_groups.keys())
    selected_samples = set()

    # ===== UI =====
    sample_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    selected_numbers = []
    number_grid = ft.GridView(expand=True, max_extent=90)

    number_count_text = ft.Text("ナンバー数: 0", color="white")
    selected_display = ft.Text("選択順: ", color="white")

    log = ft.Text(color="white")

    # =========================
    # 表示更新
    # =========================
    def update_selected_display():
        selected_display.value = "選択順: " + " → ".join(map(str, selected_numbers))

    # =========================
    # ナンバークリック
    # =========================
    def toggle_number(e):
        n = int(e.control.data)

        if n in selected_numbers:
            selected_numbers.remove(n)
            e.control.bgcolor = "#333333"
        else:
            selected_numbers.append(n)
            e.control.bgcolor = "#42a5f5"

        update_selected_display()
        page.update()

    # =========================
    # ナンバーUI生成
    # =========================
    def build_number_grid(nums, ppm_map):
        number_grid.controls.clear()
        selected_numbers.clear()

        number_count_text.value = f"ナンバー数: {len(nums)}"

        for n in nums:

            ppm_text = ""
            if n in ppm_map:
                s, e = ppm_map[n]
                ppm_text = f"{s:.2f}-{e:.2f}"

            number_grid.controls.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(str(n), size=16, color="white"),
                            ft.Text(ppm_text, size=10, color="#aaaaaa"),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    alignment=ft.Alignment(0, 0),
                    bgcolor="#333333",
                    border_radius=8,
                    padding=6,
                    data=str(n),
                    on_click=toggle_number,
                )
            )

        update_selected_display()

    # =========================
    # テンプレ適用
    # =========================
    def apply_template(sample):
        return templates.get(sample, [])

    # =========================
    # サンプル選択
    # =========================
    def toggle_sample(e):
        if e.control.value:
            selected_samples.add(e.control.label)
        else:
            selected_samples.discard(e.control.label)

        dirs = []
        for s in selected_samples:
            for d in sample_groups[s]:
                dirs.append(os.path.join(INPUT_DIR, d))

        nums, ppm_map = extract_numbers_and_ppm(dirs)

        build_number_grid(nums, ppm_map)

        # ★テンプレ自動適用（単一選択時）
        if len(selected_samples) == 1:
            s = list(selected_samples)[0]
            template = apply_template(s)

            for n in template:
                if n in nums:
                    selected_numbers.append(n)

            update_selected_display()

        page.update()

    # =========================
    # テンプレ保存
    # =========================
    def save_template(e):
        if not selected_samples or not selected_numbers:
            log.value = "保存条件不足"
            page.update()
            return

        for s in selected_samples:
            templates[s] = selected_numbers.copy()

        save_templates(templates)

        log.value = "テンプレ保存完了"
        page.update()

    # =========================
    # 実行
    # =========================
    def run(e):

        if not selected_samples:
            log.value = "サンプル未選択"
            page.update()
            return

        if not selected_numbers:
            log.value = "ナンバー未選択"
            page.update()
            return

        output_dir = os.path.join(BASE_DIR, "output")
        os.makedirs(output_dir, exist_ok=True)

        path = os.path.join(
            output_dir,
            f"result_{datetime.datetime.now().strftime('%H%M%S')}.xlsx"
        )

        dirs = []
        for s in selected_samples:
            for d in sample_groups[s]:
                dirs.append(os.path.join(INPUT_DIR, d))

        try:
            write_excel_from_integrals_multi(
                dirs,
                path,
                number_order=selected_numbers,
            )

            os.startfile(path)
            log.value = "完了"

        except Exception as err:
            log.value = f"エラー: {err}"

        page.update()

    # =========================
    # UI構築
    # =========================
    for s in samples:
        sample_list.controls.append(
            ft.Checkbox(label=s, on_change=toggle_sample)
        )

    page.add(
        ft.Row(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("サンプル一覧", color="white"),
                            sample_list,
                        ],
                        expand=True,
                    ),
                    bgcolor="#2b2b2b",
                    padding=10,
                    border_radius=10,
                    width=320,
                ),

                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("ナンバー選択", color="white"),
                            number_count_text,
                            selected_display,
                            number_grid,
                            ft.Row(
                                [
                                    ft.Button(content=ft.Text("実行"), on_click=run),
                                    ft.Button(content=ft.Text("テンプレ保存"), on_click=save_template),
                                ]
                            ),
                            log,
                        ],
                        expand=True,
                    ),
                    bgcolor="#2b2b2b",
                    padding=10,
                    border_radius=10,
                    expand=True,
                ),
            ],
            expand=True,
        )
    )


ft.run(main)