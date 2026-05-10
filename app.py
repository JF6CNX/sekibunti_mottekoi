import flet as ft
import os
import datetime
import json
import re
import sys

# ==========================================
# パス設定
# ==========================================
import sys

if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")

os.makedirs(DATA_DIR, exist_ok=True)

SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")
TEMPLATE_FILE = os.path.join(DATA_DIR, "nmr_v12_final.json")

# ==========================================
# デフォルト設定
# ==========================================
DEFAULT_SETTINGS = {
    "input_dir": r"C:/Users/haruk/chem/nmr",
    "output_dir": os.path.join(BASE_DIR, "output"),
    "theme_mode": "dark",
    "auto_open_excel": True,
}


# ==========================================
# 設定読み込み
# ==========================================
def load_settings():

    if os.path.exists(SETTINGS_FILE):

        try:

            with open(
                SETTINGS_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)

            for k, v in DEFAULT_SETTINGS.items():

                if k not in data:
                    data[k] = v

            return data

        except:
            return DEFAULT_SETTINGS.copy()

    return DEFAULT_SETTINGS.copy()


# ==========================================
# 設定保存
# ==========================================
def save_settings(data):

    with open(
        SETTINGS_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False,
        )


# ==========================================
# テンプレ読み込み
# ==========================================
def load_templates():

    if os.path.exists(TEMPLATE_FILE):

        try:

            with open(
                TEMPLATE_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                return json.load(f)

        except:
            return {}

    return {}


# ==========================================
# テンプレ保存
# ==========================================
def save_templates(data):

    with open(
        TEMPLATE_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False,
        )


# ==========================================
# integral読み込み
# ==========================================
def extract_numbers_and_ppm(dirs):

    numbers = set()
    ppm_map = {}

    for base in dirs:

        if not os.path.exists(base):
            continue

        for root, _, files in os.walk(base):

            for file in files:

                if "integrals" not in file.lower():
                    continue

                try:

                    path = os.path.join(root, file)

                    with open(
                        path,
                        encoding="utf-8",
                        errors="ignore"
                    ) as f:

                        for line in f:

                            parts = line.split()

                            if len(parts) < 4:
                                continue

                            try:

                                num = int(parts[0])

                                numbers.add(num)

                                if num not in ppm_map:

                                    ppm_map[num] = (
                                        float(parts[1]),
                                        float(parts[2]),
                                    )

                            except:
                                pass

                except:
                    pass

    return sorted(numbers), ppm_map


# ==========================================
# サンプル探索
# ==========================================
def scan_samples(input_dir):

    sample_groups = {}

    if not os.path.exists(input_dir):
        return {}

    for d in os.listdir(input_dir):

        full = os.path.join(input_dir, d)

        # フォルダのみ対象
        if not os.path.isdir(full):
            continue

        name_clean = os.path.splitext(d)[0]

        # ==================================
        # 対応例
        # TTH-AAA-001
        # MKK-BBB-002
        # FJK_CCC_003
        # abc-test-001
        # ==================================
        pattern = (
            r"^([A-Za-z0-9]+"
            r"[-_＿]"
            r"[A-Za-z0-9]+"
            r"[-_＿]"
            r"\d{3})"
        )

        match = re.match(
            pattern,
            name_clean,
        )

        if match:

            base = match.group(1)

        else:

            split_match = re.search(
                r"^(.*)[-_＿][^-_＿]+$",
                name_clean,
            )

            base = (
                split_match.group(1)
                if split_match
                else name_clean
            )

        sample_groups.setdefault(base, []).append(d)

    return sample_groups


# ==========================================
# メイン
# ==========================================
def main(page: ft.Page):

    settings = load_settings()

    os.makedirs(
        settings["output_dir"],
        exist_ok=True,
    )

    page.title = "NMR Manager"
    page.window_width = 1600
    page.window_height = 950
    page.padding = 10

    # ======================================
    # テーマ
    # ======================================
    def apply_theme():

        if settings["theme_mode"] == "dark":
            page.theme_mode = ft.ThemeMode.DARK
        else:
            page.theme_mode = ft.ThemeMode.LIGHT

    apply_theme()

    # ======================================
    # カラー
    # ======================================
    def colors():

        dark = (
            page.theme_mode
            == ft.ThemeMode.DARK
        )

        return {

            "bg":
                "#121212"
                if dark else "#F5F5F5",

            "panel":
                "#1E1E1E"
                if dark else "#FFFFFF",

            "panel2":
                "#262626"
                if dark else "#FFFFFF",

            "text":
                "white"
                if dark else "black",

            "card":
                "#333333"
                if dark else "#EAEAEA",

            "selected":
                "#1976D2",
        }

    C = colors()

    # ======================================
    # データ
    # ======================================
    custom_templates = load_templates()

    selected_samples = []
    sample_order_map = {}
    checkbox_refs = {}

    sample_groups = scan_samples(
        settings["input_dir"]
    )

    samples_keys = sorted(
        sample_groups.keys()
    )

    # ======================================
    # メッセージ
    # ======================================
    def show_message(msg, color="green"):

        page.snack_bar = ft.SnackBar(
            content=ft.Text(msg),
            bgcolor=color,
        )

        page.snack_bar.open = True

        page.update()

    # ======================================
    # UI
    # ======================================
    main_display_col = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.ALWAYS,
    )

    check_list_col = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.ALWAYS,
    )

    template_list_col = ft.Column()

    tmp_input = ft.TextField(
        label="保存名",
        width=150,
        dense=True,
    )

    # ======================================
    # 設定UI
    # ======================================
    input_dir_field = ft.TextField(
        label="NMR入力フォルダ",
        value=settings["input_dir"],
    )

    output_dir_field = ft.TextField(
        label="Excel出力フォルダ",
        value=settings["output_dir"],
    )

    theme_dropdown = ft.Dropdown(
        label="テーマ",
        value=settings["theme_mode"],
        options=[
            ft.dropdown.Option("dark"),
            ft.dropdown.Option("light"),
        ],
    )

    auto_open_switch = ft.Switch(
        label="Excel出力後に自動で開く",
        value=settings["auto_open_excel"],
    )

    # ======================================
    # 設定閉じる
    # ======================================
    def close_settings():

        settings_dialog.open = False

        page.update()

    # ======================================
    # 設定保存
    # ======================================
    def save_setting_action(e):

        try:

            old_theme = settings["theme_mode"]

            settings["input_dir"] = (
                input_dir_field.value.strip()
            )

            settings["output_dir"] = (
                output_dir_field.value.strip()
            )

            settings["theme_mode"] = (
                theme_dropdown.value
            )

            settings["auto_open_excel"] = (
                auto_open_switch.value
            )

            os.makedirs(
                settings["output_dir"],
                exist_ok=True,
            )

            save_settings(settings)

            apply_theme()

            reload_sample_list()

            rebuild_main_view()

            close_settings()

            changed = []

            if old_theme != settings["theme_mode"]:

                changed.append(
                    f"テーマ変更: "
                    f"{settings['theme_mode']}"
                )

            changed.append("設定保存完了")

            show_message(
                " / ".join(changed),
                "green",
            )

        except Exception as err:

            show_message(
                f"設定保存エラー: {err}",
                "red",
            )

    # ======================================
    # 設定ダイアログ
    # ======================================
    settings_dialog = ft.AlertDialog(

        modal=True,

        title=ft.Text("設定"),

        content=ft.Container(

            width=500,

            content=ft.Column(
                [
                    input_dir_field,
                    output_dir_field,
                    theme_dropdown,
                    auto_open_switch,
                ],
                tight=True,
            ),
        ),

        actions=[

            ft.TextButton(
                "キャンセル",
                on_click=lambda e:
                close_settings(),
            ),

            ft.ElevatedButton(
                "保存",
                on_click=save_setting_action,
            ),
        ],
    )

    page.overlay.append(settings_dialog)

    # ======================================
    # 設定開く
    # ======================================
    def open_settings(e):

        settings_dialog.open = True

        page.update()

    # ======================================
    # サンプル再読込
    # ======================================
    def reload_sample_list():

        nonlocal sample_groups
        nonlocal samples_keys

        sample_groups = scan_samples(
            settings["input_dir"]
        )

        samples_keys = sorted(
            sample_groups.keys()
        )

        check_list_col.controls.clear()

        checkbox_refs.clear()

        for s in samples_keys:

            cb = ft.Checkbox(
                label=s,
                data=s,
                on_change=on_check,
            )

            checkbox_refs[s] = cb

            check_list_col.controls.append(cb)

        page.update()

    # ======================================
    # サンプル解除
    # ======================================
    def remove_sample_direct(s_name):

        if s_name in selected_samples:
            selected_samples.remove(s_name)

        if s_name in checkbox_refs:
            checkbox_refs[s_name].value = False

        rebuild_main_view()

    # ======================================
    # 全解除
    # ======================================
    def clear_all_samples(e):

        selected_samples.clear()

        sample_order_map.clear()

        for cb in checkbox_refs.values():
            cb.value = False

        rebuild_main_view()

    # ======================================
    # メイン描画
    # ======================================
    def rebuild_main_view():

        nonlocal C

        C = colors()

        new_controls = []

        for s_name in selected_samples:

            dirs = [

                os.path.join(
                    settings["input_dir"],
                    d,
                )

                for d in sample_groups[s_name]
            ]

            nums, ppm_map = (
                extract_numbers_and_ppm(dirs)
            )

            order = sample_order_map.get(
                s_name,
                [],
            )

            cards = []

            for n in nums:

                is_sel = n in order

                ppm_val = ""

                if n in ppm_map:

                    ppm_val = (
                        f"{ppm_map[n][0]:.1f}"
                        f"-"
                        f"{ppm_map[n][1]:.1f}"
                    )

                card = ft.Container(

                    width=80,
                    height=100,

                    bgcolor=(
                        C["selected"]
                        if is_sel
                        else C["card"]
                    ),

                    border=(
                        ft.border.all(2, "white")
                        if is_sel
                        else None
                    ),

                    border_radius=8,

                    on_click=lambda e,
                    sn=s_name,
                    num=n:
                    toggle_number(sn, num),

                    content=ft.Column(

                        [

                            ft.Text(
                                (
                                    f"#{order.index(n)+1}"
                                    if is_sel
                                    else ""
                                ),
                                size=10,
                                color="yellow",
                                weight="bold",
                            ),

                            ft.Text(
                                str(n),
                                size=22,
                                color=C["text"],
                                weight="bold",
                            ),

                            ft.Text(
                                ppm_val,
                                size=9,
                                color=C["text"],
                            ),
                        ],

                        alignment="center",
                        horizontal_alignment="center",
                        spacing=0,
                    ),
                )

                cards.append(card)

            new_controls.append(

                ft.Container(

                    padding=10,

                    content=ft.Column(

                        [

                            ft.Row(

                                [

                                    ft.Text(
                                        s_name,
                                        size=16,
                                        weight="bold",
                                        color="#4DABF7",
                                        expand=True,
                                    ),

                                    ft.ElevatedButton(
                                        "× 解除",
                                        height=30,
                                        on_click=lambda e,
                                        sn=s_name:
                                        remove_sample_direct(sn),
                                    ),
                                ]
                            ),

                            ft.Row(
                                cards,
                                scroll=ft.ScrollMode.ALWAYS,
                                height=120,
                            ),

                            ft.Divider(),
                        ]
                    ),
                )
            )

        main_display_col.controls = new_controls

        page.bgcolor = C["bg"]

        left_panel.bgcolor = C["panel2"]
        center_panel.bgcolor = C["panel"]
        right_panel.bgcolor = C["panel2"]

        left_title.color = C["text"]
        center_title.color = C["text"]
        right_title.color = C["text"]

        left_panel.update()
        center_panel.update()
        right_panel.update()

        page.update()

    # ======================================
    # ナンバー切替
    # ======================================
    def toggle_number(s_name, num):

        if s_name not in sample_order_map:
            sample_order_map[s_name] = []

        lst = sample_order_map[s_name]

        if num in lst:
            lst.remove(num)
        else:
            lst.append(num)

        rebuild_main_view()

    # ======================================
    # チェック
    # ======================================
    def on_check(e):

        s_name = e.control.data

        if e.control.value:

            if s_name not in selected_samples:
                selected_samples.append(s_name)

        else:

            if s_name in selected_samples:
                selected_samples.remove(s_name)

        rebuild_main_view()

    # ======================================
    # テンプレ保存
    # ======================================
    def save_t(e):

        name = tmp_input.value.strip()

        if not name:
            return

        if not selected_samples:

            show_message(
                "サンプル未選択",
                "red",
            )

            return

        ref = selected_samples[0]

        custom_templates[name] = list(
            sample_order_map.get(ref, [])
        )

        save_templates(custom_templates)

        tmp_input.value = ""

        update_tmp_ui()

        show_message(
            f"テンプレ保存: {name}",
            "blue",
        )

    # ======================================
    # テンプレ適用
    # ======================================
    def apply_t(name):

        order = custom_templates[name]

        for s_name in selected_samples:

            sample_order_map[s_name] = list(order)

        rebuild_main_view()

        show_message(
            f"テンプレ適用: {name}",
            "blue",
        )

    # ======================================
    # テンプレ削除
    # ======================================
    def del_t(name):

        if name in custom_templates:

            del custom_templates[name]

            save_templates(custom_templates)

            update_tmp_ui()

            show_message(
                f"テンプレ削除: {name}",
                "red",
            )

    # ======================================
    # テンプレ更新
    # ======================================
    def update_tmp_ui():

        template_list_col.controls = [

            ft.Row(

                [

                    ft.ElevatedButton(
                        n,
                        expand=True,
                        on_click=lambda e,
                        name=n:
                        apply_t(name),
                    ),

                    ft.ElevatedButton(
                        "×",
                        width=45,
                        bgcolor="red",
                        color="white",
                        on_click=lambda e,
                        name=n:
                        del_t(name),
                    ),
                ]
            )

            for n in sorted(
                custom_templates.keys()
            )
        ]

        page.update()

    # ======================================
    # Excel出力
    # ======================================
    def run_excel(e):

        if not selected_samples:

            show_message(
                "サンプル未選択",
                "red",
            )

            return

        try:

            from nmr_excelsekibunti.core.excel_writer import (
                write_excel_from_integrals_multi,
            )

            timestamp = (
                datetime.datetime.now().strftime(
                    "%Y%m%d_%H%M%S"
                )
            )

            filename = f"{timestamp}.xlsx"

            path = os.path.join(
                settings["output_dir"],
                filename,
            )

            count = 0

            for s in selected_samples:

                dirs = [

                    os.path.join(
                        settings["input_dir"],
                        d,
                    )

                    for d in sample_groups[s]
                ]

                order = sample_order_map.get(
                    s,
                    [],
                )

                if not order:
                    continue

                write_excel_from_integrals_multi(
                    dirs,
                    path,
                    number_order=order,
                    append=(count > 0),
                )

                count += 1

            if count > 0:

                if settings["auto_open_excel"]:
                    os.startfile(path)

                show_message(
                    f"Excel出力成功: {filename}",
                    "green",
                )

            else:

                show_message(
                    "出力データなし",
                    "red",
                )

        except Exception as err:

            show_message(
                f"Error: {err}",
                "red",
            )

    # ======================================
    # 初期チェック
    # ======================================
    for s in samples_keys:

        cb = ft.Checkbox(
            label=s,
            data=s,
            on_change=on_check,
        )

        checkbox_refs[s] = cb

        check_list_col.controls.append(cb)

    update_tmp_ui()

    # ======================================
    # 左
    # ======================================
    left_title = ft.Text(
        "対象選択",
        size=20,
        weight="bold",
        color=C["text"],
    )

    left_panel = ft.Container(

        width=300,

        bgcolor=C["panel2"],

        border_radius=10,

        padding=15,

        content=ft.Column(

            [

                left_title,

                ft.Divider(),

                ft.ElevatedButton(
                    "全解除",
                    on_click=clear_all_samples,
                ),

                check_list_col,
            ]
        ),
    )

    # ======================================
    # 中央
    # ======================================
    center_title = ft.Text(
        "NMR Manager",
        size=24,
        weight="bold",
        color=C["text"],
    )

    center_panel = ft.Container(

        expand=True,

        bgcolor=C["panel"],

        border_radius=10,

        padding=15,

        content=ft.Column(

            [

                ft.Row(

                    [

                        center_title,

                        ft.Row(

                            [

                                ft.ElevatedButton(
                                    "設定",
                                    on_click=open_settings,
                                ),

                                ft.ElevatedButton(
                                    "Excel出力",
                                    bgcolor="green",
                                    color="white",
                                    on_click=run_excel,
                                ),
                            ]
                        ),
                    ],

                    alignment="spaceBetween",
                ),

                ft.Divider(),

                main_display_col,
            ]
        ),
    )

    # ======================================
    # 右
    # ======================================
    right_title = ft.Text(
        "テンプレート",
        size=20,
        weight="bold",
        color=C["text"],
    )

    right_panel = ft.Container(

        width=300,

        bgcolor=C["panel2"],

        border_radius=10,

        padding=15,

        content=ft.Column(

            [

                right_title,

                ft.Row(
                    [
                        tmp_input,

                        ft.ElevatedButton(
                            "保存",
                            on_click=save_t,
                        ),
                    ]
                ),

                ft.Divider(),

                template_list_col,
            ]
        ),
    )

    # ======================================
    # レイアウト
    # ======================================
    page.add(

        ft.Row(

            [
                left_panel,
                center_panel,
                right_panel,
            ],

            expand=True,
        )
    )

    rebuild_main_view()


# ==========================================
# 起動
# ==========================================
if __name__ == "__main__":

    ft.app(target=main)