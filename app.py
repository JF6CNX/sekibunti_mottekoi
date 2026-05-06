import flet as ft
import os
import sys
import json
import re

BASE_DIR = os.path.dirname(__file__)
sys.path.append(BASE_DIR)

from nmr_excelsekibunti.core.excel_writer import write_excel_from_integrals_multi

CONFIG_PATH = "config.json"
INPUT_DIR = r"C:/Users/haruk/chem/nmr"


def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    return {"templates": {"default": [1,2,3,4]}}


def save_config(cfg):
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=2)


def main(page: ft.Page):
    page.title = "NMR Tool"
    page.scroll = ft.ScrollMode.AUTO   # ★重要

    config = load_config()
    selected_samples = set()

    number_field = ft.TextField(label="ナンバー順 (例: 1,2,3,4)")
    template_name = ft.TextField(label="テンプレ名")
    log = ft.TextField(multiline=True, read_only=True, height=200)

    template_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(k) for k in config["templates"].keys()],
        label="テンプレ選択"
    )

    sample_list = ft.ListView(expand=True, spacing=5)  # ★重要

    def write_log(msg):
        log.value += msg + "\n"
        page.update()

    # ===== サンプル取得 =====
    samples_raw = [
        d for d in os.listdir(INPUT_DIR)
        if os.path.isdir(os.path.join(INPUT_DIR, d)) and d.startswith("TTH")
    ]

    sample_groups = {}
    for name in samples_raw:
        base = name.split("_")[0]
        sample_groups.setdefault(base, []).append(name)

    samples = sorted(sample_groups.keys())

    def toggle(e):
        if e.control.value:
            selected_samples.add(e.control.label)
        else:
            selected_samples.discard(e.control.label)

    for s in samples:
        sample_list.controls.append(ft.Checkbox(label=s, on_change=toggle))

    # ===== テンプレ保存 =====
    def save_template(e):
        try:
            nums = list(map(int, number_field.value.split(",")))
            name = template_name.value or "new_template"

            config["templates"][name] = nums
            save_config(config)

            template_dropdown.options = [
                ft.dropdown.Option(k) for k in config["templates"].keys()
            ]

            write_log(f"保存: {name}")
            page.update()

        except:
            write_log("保存失敗")

    # ===== テンプレ読み込み =====
    def load_template(e):
        name = template_dropdown.value
        if name in config["templates"]:
            number_field.value = ",".join(map(str, config["templates"][name]))
            page.update()

    template_dropdown.on_change = load_template

    # ===== 実行 =====
    def run(e):
        if not selected_samples:
            write_log("サンプル未選択")
            return

        try:
            numbers = list(map(int, number_field.value.split(",")))
        except:
            numbers = [1,2,3,4]

        output_dir = os.path.join(BASE_DIR, "output")
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, "result.xlsx")

        try:
            all_dirs = []

            for sample in selected_samples:
                targets = sample_groups[sample]

                def sort_key(x):
                    m = re.search(r"(\d+)", x)
                    return int(m.group(1)) if m else 0

                targets = sorted(targets, key=lambda x: ("re" in x, sort_key(x)))

                for t in targets:
                    all_dirs.append(os.path.join(INPUT_DIR, t))

            write_excel_from_integrals_multi(
                all_dirs,
                output_path,
                number_order=numbers
            )

            write_log("完了")
            os.startfile(output_path)

        except Exception as err:
            write_log(f"エラー: {err}")

    # ===== UI（ここが最重要修正） =====
    page.add(
        ft.Row(
            [
                ft.Container(
                    ft.Column([
                        ft.Text("サンプル選択"),
                        sample_list
                    ], expand=True),
                    expand=1
                ),

                ft.Container(
                    ft.Column([
                        ft.Text("設定"),
                        number_field,
                        template_name,
                        template_dropdown,
                        ft.Row([
                            ft.Button("保存", on_click=save_template),
                            ft.Button("実行", on_click=run)
                        ]),
                        log
                    ], expand=True),
                    expand=2
                )
            ],
            expand=True   # ★重要
        )
    )


ft.run(main)