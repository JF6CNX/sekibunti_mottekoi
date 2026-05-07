import flet as ft
import os
import sys
import datetime
import json

# ==========================================
# 設定
# ==========================================
BASE_DIR = os.path.dirname(__file__)
INPUT_DIR = r"C:/Users/haruk/chem/nmr"
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)
TEMPLATE_FILE = os.path.join(DATA_DIR, "nmr_v12_final.json")

def load_templates():
    if os.path.exists(TEMPLATE_FILE):
        with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
            try: return json.load(f)
            except: return {}
    return {}

def save_templates(data):
    with open(TEMPLATE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def extract_numbers_and_ppm(dirs):
    numbers, ppm_map = set(), {}
    for base in dirs:
        if not os.path.exists(base): continue
        for root, _, files in os.walk(base):
            for file in files:
                if "integrals" not in file.lower(): continue
                try:
                    with open(os.path.join(root, file), encoding="utf-8", errors="ignore") as f:
                        for line in f:
                            parts = line.split()
                            if len(parts) < 4: continue
                            try:
                                num = int(parts[0])
                                numbers.add(num)
                                if num not in ppm_map:
                                    ppm_map[num] = (float(parts[1]), float(parts[2]))
                            except: pass
                except: pass
    return sorted(numbers), ppm_map

# ==========================================
# メイン
# ==========================================
def main(page: ft.Page):
    page.title = "NMR Manager - Rebuild Mode v12"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 1500
    page.window_height = 900
    page.padding = 20

    custom_templates = load_templates()
    selected_samples = []
    sample_order_map = {} 
    checkbox_refs = {} # 左側のチェックボックスを操作するための参照用

    # フォルダスキャン
    sample_groups = {} 
    if os.path.exists(INPUT_DIR):
        for d in os.listdir(INPUT_DIR):
            full = os.path.join(INPUT_DIR, d)
            if os.path.isdir(full) and d.startswith("TTH"):
                base = d.split("_")[0]
                sample_groups.setdefault(base, []).append(d)
    samples_keys = sorted(sample_groups.keys())

    # --- UI要素 ---
    main_display_col = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True)
    check_list_col = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True)
    template_list_col = ft.Column(spacing=5)
    tmp_input = ft.TextField(label="保存名", width=150, dense=True)
    log = ft.Text("", color="orange", weight="bold")

    def remove_sample_direct(s_name):
        """中央の×ボタンから解除する処理"""
        if s_name in selected_samples:
            selected_samples.remove(s_name)
        # 左側のチェックボックスの状態も更新する
        if s_name in checkbox_refs:
            checkbox_refs[s_name].value = False
        rebuild_main_view()

    def rebuild_main_view():
        new_controls = []
        for s_name in selected_samples:
            dirs = [os.path.join(INPUT_DIR, d) for d in sample_groups[s_name]]
            nums, ppm_map = extract_numbers_and_ppm(dirs)
            order = sample_order_map.get(s_name, [])
            
            cards = []
            for n in nums:
                is_sel = n in order
                ppm_val = f"{ppm_map[n][0]:.1f}-{ppm_map[n][1]:.1f}" if n in ppm_map else ""
                card = ft.Container(
                    content=ft.Column([
                        ft.Text(f"#{order.index(n)+1}" if is_sel else "", size=10, weight="bold", color="yellow"),
                        ft.Text(str(n), size=22, weight="bold"),
                        ft.Text(ppm_val, size=9),
                    ], alignment="center", horizontal_alignment="center", spacing=0),
                    width=80, height=100,
                    bgcolor="#1976D2" if is_sel else "#333333",
                    border=ft.border.all(2, "white") if is_sel else None,
                    border_radius=8,
                    on_click=lambda e, sn=s_name, num=n: toggle_number(sn, num)
                )
                cards.append(card)
            
            new_controls.append(
                ft.Container(
                    content=ft.Column([
                        # ここに解除ボタンを追加
                        ft.Row([
                            ft.Text(s_name, size=16, weight="bold", color="#4DABF7", expand=True),
                            ft.ElevatedButton(
                                content=ft.Text("× 解除", size=11), 
                                bgcolor="#444444", 
                                color="white",
                                on_click=lambda e, sn=s_name: remove_sample_direct(sn),
                                height=30
                            )
                        ]),
                        ft.Row(controls=cards, scroll=ft.ScrollMode.ALWAYS, height=120),
                        ft.Divider(height=1, color="white24")
                    ]),
                    padding=10
                )
            )
        main_display_col.controls = new_controls
        page.update()

    def toggle_number(s_name, num):
        if s_name not in sample_order_map: sample_order_map[s_name] = []
        lst = sample_order_map[s_name]
        if num in lst: lst.remove(num)
        else: lst.append(num)
        rebuild_main_view()

    def on_check(e):
        s_name = e.control.data
        if e.control.value:
            if s_name not in selected_samples: selected_samples.append(s_name)
        else:
            if s_name in selected_samples: selected_samples.remove(s_name)
        rebuild_main_view()

    # --- テンプレート操作 ---
    def save_t(e):
        name = tmp_input.value.strip()
        if name and selected_samples:
            ref = selected_samples[0]
            custom_templates[name] = list(sample_order_map.get(ref, []))
            save_templates(custom_templates)
            tmp_input.value = ""
            update_tmp_ui()

    def apply_t(name):
        order = custom_templates[name]
        for s_name in selected_samples:
            sample_order_map[s_name] = list(order)
        rebuild_main_view()

    def del_t(name):
        if name in custom_templates:
            del custom_templates[name]
            save_templates(custom_templates)
            update_tmp_ui()

    def update_tmp_ui():
        template_list_col.controls = [
            ft.Row([
                ft.ElevatedButton(n, on_click=lambda e, name=n: apply_t(name), expand=True),
                ft.ElevatedButton("×", bgcolor="red800", color="white", on_click=lambda e, name=n: del_t(name), width=45)
            ]) for n in sorted(custom_templates.keys())
        ]
        page.update()

    # --- Excel出力 ---
    def run_excel(e):
        if not selected_samples: return
        try:
            from nmr_excelsekibunti.core.excel_writer import write_excel_from_integrals_multi
            path = os.path.join(BASE_DIR, f"Result_{datetime.datetime.now().strftime('%H%M%S')}.xlsx")
            count = 0
            for s in selected_samples:
                dirs = [os.path.join(INPUT_DIR, d) for d in sample_groups[s]]
                order = sample_order_map.get(s, [])
                if not order: continue
                write_excel_from_integrals_multi(dirs, path, number_order=order, append=(count > 0))
                count += 1
            if count > 0: os.startfile(path); log.value = "Excel成功"
        except Exception as err:
            log.value = f"Error: {err}"
        page.update()

    # --- 初期配置 ---
    for s in samples_keys:
        cb = ft.Checkbox(label=s, data=s, on_change=on_check)
        checkbox_refs[s] = cb # 参照を保存
        check_list_col.controls.append(cb)

    update_tmp_ui()

    page.add(
        ft.Row([
            # 左
            ft.Container(
                content=ft.Column([ft.Text("対象選択", weight="bold"), ft.Divider(), check_list_col]),
                width=250, bgcolor="#262626", padding=15, border_radius=10
            ),
            # 中
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text("ナンバー設定", size=20, weight="bold"),
                        ft.ElevatedButton("Excel出力", bgcolor="green", color="white", on_click=run_excel)
                    ], alignment="spaceBetween"),
                    ft.Divider(),
                    main_display_col,
                    log
                ]),
                expand=True, bgcolor="#1E1E1E", padding=15, border_radius=10
            ),
            # 右
            ft.Container(
                content=ft.Column([
                    ft.Text("テンプレート"),
                    ft.Row([tmp_input, ft.ElevatedButton("保存", on_click=save_t)]),
                    ft.Divider(),
                    template_list_col
                ]),
                width=300, bgcolor="#262626", padding=15, border_radius=10
            )
        ], expand=True)
    )

if __name__ == "__main__":
    ft.app(target=main)