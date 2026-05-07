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


# ==========================================
# テンプレ読み込み
# ==========================================
def load_templates():

    if os.path.exists(TEMPLATE_FILE):

        try:
            with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)

        except:
            return {}

    return {}


# ==========================================
# テンプレ保存
# ==========================================
def save_templates(data):

    with open(TEMPLATE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ==========================================
# ナンバー + ppm 抽出
# ==========================================
def extract_numbers_and_ppm(dirs):

    numbers = set()
    ppm_map = {}

    for base in dirs:

        for root, _, files in os.walk(base):

            for file in files:

                if "integrals" not in file.lower():
                    continue

                path = os.path.join(root, file)

                try:
                    with open(path, encoding="utf-8", errors="ignore") as f:

                        for line in f:

                            parts = line.split()

                            if len(parts) < 4:
                                continue

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


# ==========================================
# メイン
# ==========================================
def main(page: ft.Page):

    page.title = "NMR Tool"

    page.theme_mode = ft.ThemeMode.DARK

    page.bgcolor = "#1e1e1e"

    page.padding = 10

    templates = load_templates()

    # ==========================================
    # サンプル探索
    # ==========================================
    sample_groups = {}

    for d in os.listdir(INPUT_DIR):

        full = os.path.join(INPUT_DIR, d)

        if os.path.isdir(full) and d.startswith("TTH"):

            base = d.split("_")[0]

            sample_groups.setdefault(base, []).append(d)

    samples = sorted(sample_groups.keys())

    selected_samples = set()

    selected_numbers_by_sample = {}

    sample_list = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=2,
    )

    number_panels = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    log = ft.Text(color="white")

    # ==========================================
    # ナンバークリック
    # ==========================================
    def toggle_number(e):

        sample = e.control.data["sample"]

        number = e.control.data["number"]

        selected = selected_numbers_by_sample.setdefault(sample, [])

        if number in selected:

            selected.remove(number)

        else:

            selected.append(number)

        update_panels()

    # ==========================================
    # パネル更新
    # ==========================================
    def update_panels():

        number_panels.controls.clear()

        for sample in selected_samples:

            dirs = []

            for d in sample_groups[sample]:
                dirs.append(os.path.join(INPUT_DIR, d))

            nums, ppm_map = extract_numbers_and_ppm(dirs)

            if sample not in selected_numbers_by_sample:
                selected_numbers_by_sample[sample] = []

            selected = selected_numbers_by_sample[sample]

            # ===== テンプレ自動適用 =====
            if not selected and sample in templates:

                for n in templates[sample]:

                    if n in nums:
                        selected.append(n)

            chips = []

            for n in nums:

                ppm_text = ""

                if n in ppm_map:

                    s, e = ppm_map[n]

                    ppm_text = f"{s:.2f}-{e:.2f}"

                is_selected = n in selected

                chips.append(

                    ft.Container(

                        content=ft.Column(

                            [

                                ft.Text(
                                    str(n),
                                    color="white",
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                ),

                                ft.Text(
                                    ppm_text,
                                    color="#bbbbbb",
                                    size=10,
                                ),

                            ],

                            spacing=2,

                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                        ),

                        bgcolor="#1976d2" if is_selected else "#333333",

                        border_radius=10,

                        padding=8,

                        width=90,

                        height=70,

                        alignment=ft.Alignment(0, 0),

                        data={
                            "sample": sample,
                            "number": n,
                        },

                        on_click=toggle_number,
                    )
                )

            selected_text = " → ".join(map(str, selected))

            panel = ft.Container(

                content=ft.Column(

                    [

                        ft.Text(
                            sample,
                            color="white",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                        ),

                        ft.Text(
                            f"ナンバー数: {len(nums)}",
                            color="#cccccc",
                        ),

                        ft.Text(
                            f"選択順: {selected_text}",
                            color="#90caf9",
                        ),

                        ft.GridView(
                            controls=chips,
                            runs_count=5,
                            max_extent=100,
                            child_aspect_ratio=1.2,
                            spacing=10,
                            run_spacing=10,
                            height=250,
                        ),

                    ],

                    spacing=10,

                ),

                bgcolor="#2b2b2b",

                border_radius=12,

                padding=15,

            )

            number_panels.controls.append(panel)

        page.update()

    # ==========================================
    # サンプル選択
    # ==========================================
    def toggle_sample(e):

        sample = e.control.label

        if e.control.value:
            selected_samples.add(sample)

        else:
            selected_samples.discard(sample)

        update_panels()

    # ==========================================
    # テンプレ保存
    # ==========================================
    def save_template(e):

        for sample, nums in selected_numbers_by_sample.items():

            if nums:
                templates[sample] = nums

        save_templates(templates)

        log.value = "テンプレ保存完了"

        page.update()

    # ==========================================
    # 実行
    # ==========================================
    def run(e):

        if not selected_samples:

            log.value = "サンプル未選択"

            page.update()

            return

        output_dir = os.path.join(BASE_DIR, "output")

        os.makedirs(output_dir, exist_ok=True)

        path = os.path.join(
            output_dir,
            f"result_{datetime.datetime.now().strftime('%H%M%S')}.xlsx"
        )

        try:

            first = True

            for sample in selected_samples:

                dirs = []

                for d in sample_groups[sample]:
                    dirs.append(os.path.join(INPUT_DIR, d))

                write_excel_from_integrals_multi(
                    dirs,
                    path,
                    number_order=selected_numbers_by_sample.get(sample, []),
                    append=not first,
                )

                first = False

            os.startfile(path)

            log.value = "Excel保存完了"

        except Exception as err:

            log.value = f"エラー: {err}"

        page.update()

    # ==========================================
    # サンプル一覧
    # ==========================================
    for s in samples:

        sample_list.controls.append(

            ft.Checkbox(
                label=s,
                value=False,
                on_change=toggle_sample,
                label_style=ft.TextStyle(color="white"),
            )
        )

    # ==========================================
    # UI
    # ==========================================
    page.add(

        ft.Row(

            [

                ft.Container(

                    content=ft.Column(

                        [

                            ft.Text(
                                "サンプル一覧",
                                color="white",
                                size=22,
                                weight=ft.FontWeight.BOLD,
                            ),

                            sample_list,

                        ],

                        expand=True,

                    ),

                    bgcolor="#2b2b2b",

                    border_radius=12,

                    padding=10,

                    width=320,

                ),

                ft.Container(

                    content=ft.Column(

                        [

                            ft.Row(

                                [

                                    ft.Button(
                                        content=ft.Text("実行"),
                                        on_click=run,
                                    ),

                                    ft.Button(
                                        content=ft.Text("テンプレ保存"),
                                        on_click=save_template,
                                    ),

                                ]
                            ),

                            number_panels,

                            log,

                        ],

                        expand=True,

                    ),

                    bgcolor="#1e1e1e",

                    expand=True,

                    padding=10,

                ),

            ],

            expand=True,

        )
    )


ft.run(main)