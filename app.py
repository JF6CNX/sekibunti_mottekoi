import flet as ft
import os
import sys
import datetime

BASE_DIR = os.path.dirname(__file__)
sys.path.append(BASE_DIR)

from nmr_excelsekibunti.core.excel_writer import write_excel_from_integrals_multi

INPUT_DIR = r"C:/Users/haruk/chem/nmr"


# =========================
# ナンバー抽出（強化版）
# =========================
def extract_numbers(dirs):
    numbers = set()

    for base in dirs:
        for root, _, files in os.walk(base):
            for file in files:

                if "integrals" in file.lower():

                    path = os.path.join(root, file)
                    print("FOUND:", path)

                    try:
                        with open(path, encoding="utf-8", errors="ignore") as f:
                            for line in f:
                                parts = line.split()

                                if len(parts) >= 4:
                                    try:
                                        numbers.add(int(parts[0]))
                                    except:
                                        pass
                    except Exception as e:
                        print("READ ERROR:", e)

    print("NUMBERS:", numbers)
    return sorted(numbers)


# =========================
# メイン
# =========================
def main(page: ft.Page):

    page.title = "NMR Tool"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#1e1e1e"

    # ===== サンプル取得 =====
    sample_groups = {}

    for d in os.listdir(INPUT_DIR):
        full = os.path.join(INPUT_DIR, d)

        if os.path.isdir(full) and d.startswith("TTH"):
            base = d.split("_")[0]
            sample_groups.setdefault(base, []).append(d)

    samples = sorted(sample_groups.keys())
    selected_samples = set()

    # ===== UI：サンプル =====
    sample_list = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    # ===== ナンバーUI =====
    selected_numbers = []
    number_grid = ft.GridView(expand=True, max_extent=80)

    number_count_text = ft.Text("ナンバー数: 0", color="white")
    selected_display = ft.Text("選択順: ", color="white")

    def update_selected_display():
        selected_display.value = "選択順: " + " → ".join(map(str, selected_numbers))

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

    def build_number_grid(nums):
        number_grid.controls.clear()
        selected_numbers.clear()

        number_count_text.value = f"ナンバー数: {len(nums)}"

        for n in nums:
            number_grid.controls.append(
                ft.Container(
                    content=ft.Text(str(n), color="white"),
                    alignment=ft.Alignment(0, 0),
                    bgcolor="#333333",
                    border_radius=8,
                    padding=10,
                    data=str(n),
                    on_click=toggle_number,
                )
            )

        update_selected_display()

    # ===== サンプル選択 =====
    def toggle_sample(e):
        if e.control.value:
            selected_samples.add(e.control.label)
        else:
            selected_samples.discard(e.control.label)

        dirs = []
        for s in selected_samples:
            for d in sample_groups[s]:
                dirs.append(os.path.join(INPUT_DIR, d))

        print("DIRS:", dirs)

        nums = extract_numbers(dirs)
        build_number_grid(nums)

        page.update()

    # サンプル表示
    for s in samples:
        sample_list.controls.append(
            ft.Checkbox(label=s, on_change=toggle_sample)
        )

    # ===== 実行 =====
    log = ft.Text(color="white")

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

    # ===== UI配置 =====
    page.add(
        ft.Row(
            [
                # 左：サンプル
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

                # 右：ナンバー
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("ナンバー選択", color="white"),
                            number_count_text,
                            selected_display,
                            number_grid,
                            ft.Button(
                                content=ft.Text("実行"),
                                on_click=run
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