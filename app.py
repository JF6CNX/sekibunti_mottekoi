import os

import flet as ft

from nmr_manager.excel_service import export_selected_samples
from nmr_manager.integrals import extract_numbers_and_ppm
from nmr_manager.messages import (
    NO_OUTPUT_DATA,
    SAMPLE_NOT_SELECTED,
    error_message,
    excel_export_success,
)
from nmr_manager.scanner import scan_samples
from nmr_manager.settings import load_settings, save_settings
from nmr_manager.state import AppState
from nmr_manager.templates import load_templates, save_templates
from nmr_manager.theme import get_colors, get_theme_mode
from nmr_manager.ui import (
    build_center_panel,
    build_center_title,
    build_main_layout,
    build_sample_panel,
    build_sample_title,
    build_settings_dialog,
    build_settings_fields,
    build_template_input,
    build_template_panel,
    build_template_title,
)


def main(page: ft.Page):
    settings = load_settings()
    custom_templates = load_templates()
    state = AppState()
    state.set_sample_groups(scan_samples(settings["input_dir"]))

    page.title = "NMR Manager"
    page.window_width = 1600
    page.window_height = 950
    page.padding = 10
    page.theme_mode = get_theme_mode(settings["theme_mode"])

    colors = get_colors(settings["theme_mode"])
    page.bgcolor = colors["bg"]

    main_display_col = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.ALWAYS,
    )
    check_list_col = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.ALWAYS,
    )
    template_list_col = ft.Column()
    tmp_input = build_template_input()

    (
        input_dir_field,
        output_dir_field,
        theme_dropdown,
        auto_open_switch,
    ) = build_settings_fields(settings)

    def show_message(message, color="green"):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=color,
        )
        page.snack_bar.open = True
        page.update()

    def apply_theme():
        nonlocal colors

        page.theme_mode = get_theme_mode(settings["theme_mode"])
        colors = get_colors(settings["theme_mode"])
        page.bgcolor = colors["bg"]

    def close_settings(e=None):
        settings_dialog.open = False
        page.update()

    def save_setting_action(e):
        try:
            settings["input_dir"] = input_dir_field.value.strip()
            settings["output_dir"] = output_dir_field.value.strip()
            settings["theme_mode"] = theme_dropdown.value
            settings["auto_open_excel"] = auto_open_switch.value

            os.makedirs(settings["output_dir"], exist_ok=True)
            save_settings(settings)

            apply_theme()
            reload_sample_list()
            rebuild_main_view()
            close_settings()
            show_message("settings saved", "green")

        except Exception as err:
            show_message(error_message(err), "red")

    def open_settings(e):
        settings_dialog.open = True
        page.update()

    def on_check(e):
        sample_name = e.control.data

        if e.control.value:
            state.select_sample(sample_name)
        else:
            state.unselect_sample(sample_name)

        rebuild_main_view()

    def reload_sample_list():
        state.set_sample_groups(scan_samples(settings["input_dir"]))
        check_list_col.controls.clear()
        state.checkbox_refs.clear()

        for sample_name in state.samples_keys:
            checkbox = ft.Checkbox(
                label=sample_name,
                data=sample_name,
                on_change=on_check,
            )
            state.checkbox_refs[sample_name] = checkbox
            check_list_col.controls.append(checkbox)

        page.update()

    def remove_sample_direct(sample_name):
        state.unselect_sample(sample_name)

        if sample_name in state.checkbox_refs:
            state.checkbox_refs[sample_name].value = False

        rebuild_main_view()

    def clear_all_samples(e):
        state.clear_samples()
        rebuild_main_view()

    def toggle_number(sample_name, number):
        state.toggle_number(sample_name, number)
        rebuild_main_view()

    def rebuild_main_view():
        apply_theme()

        new_controls = []

        for sample_name in state.selected_samples:
            dirs = [
                os.path.join(settings["input_dir"], dirname)
                for dirname in state.sample_groups[sample_name]
            ]
            numbers, ppm_map = extract_numbers_and_ppm(dirs)
            order = state.get_order(sample_name)
            cards = []

            for number in numbers:
                is_selected = number in order
                ppm_value = ""

                if number in ppm_map:
                    ppm_value = f"{ppm_map[number][0]:.1f}-{ppm_map[number][1]:.1f}"

                card = ft.Container(
                    width=80,
                    height=100,
                    bgcolor=colors["selected"] if is_selected else colors["card"],
                    border=ft.border.all(2, "white") if is_selected else None,
                    border_radius=8,
                    on_click=lambda e, sn=sample_name, num=number: toggle_number(
                        sn,
                        num,
                    ),
                    content=ft.Column(
                        [
                            ft.Text(
                                f"#{order.index(number) + 1}" if is_selected else "",
                                size=10,
                                color="yellow",
                                weight="bold",
                            ),
                            ft.Text(
                                str(number),
                                size=22,
                                color=colors["text"],
                                weight="bold",
                            ),
                            ft.Text(
                                ppm_value,
                                size=9,
                                color=colors["text"],
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
                                        sample_name,
                                        size=16,
                                        weight="bold",
                                        color="#4DABF7",
                                        expand=True,
                                    ),
                                    ft.ElevatedButton(
                                        "Remove",
                                        height=30,
                                        on_click=lambda e, sn=sample_name: (
                                            remove_sample_direct(sn)
                                        ),
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

        left_panel.bgcolor = colors["panel2"]
        center_panel.bgcolor = colors["panel"]
        right_panel.bgcolor = colors["panel2"]

        left_title.color = colors["text"]
        center_title.color = colors["text"]
        right_title.color = colors["text"]

        page.update()

    def save_template(e):
        name = tmp_input.value.strip()

        if not name:
            return

        if not state.selected_samples:
            show_message(SAMPLE_NOT_SELECTED, "red")
            return

        reference_sample = state.selected_samples[0]
        custom_templates[name] = list(state.get_order(reference_sample))
        save_templates(custom_templates)

        tmp_input.value = ""
        update_template_ui()
        show_message(f"template saved: {name}", "blue")

    def apply_template(name):
        order = custom_templates[name]

        for sample_name in state.selected_samples:
            state.set_order(sample_name, order)

        rebuild_main_view()
        show_message(f"template applied: {name}", "blue")

    def delete_template(name):
        if name not in custom_templates:
            return

        del custom_templates[name]
        save_templates(custom_templates)
        update_template_ui()
        show_message(f"template deleted: {name}", "red")

    def update_template_ui():
        template_list_col.controls = [
            ft.Row(
                [
                    ft.ElevatedButton(
                        name,
                        expand=True,
                        on_click=lambda e, template_name=name: apply_template(
                            template_name
                        ),
                    ),
                    ft.ElevatedButton(
                        "X",
                        width=45,
                        bgcolor="red",
                        color="white",
                        on_click=lambda e, template_name=name: delete_template(
                            template_name
                        ),
                    ),
                ]
            )
            for name in sorted(custom_templates.keys())
        ]
        page.update()

    def run_excel(e):
        if not state.selected_samples:
            show_message(SAMPLE_NOT_SELECTED, "red")
            return

        try:
            path, filename, count = export_selected_samples(
                settings,
                state.selected_samples,
                state.sample_groups,
                state.sample_order_map,
            )

            if count > 0:
                if settings["auto_open_excel"]:
                    os.startfile(path)

                show_message(excel_export_success(filename), "green")
            else:
                show_message(NO_OUTPUT_DATA, "red")

        except Exception as err:
            show_message(error_message(err), "red")

    settings_dialog = build_settings_dialog(
        input_dir_field,
        output_dir_field,
        theme_dropdown,
        auto_open_switch,
        close_settings,
        save_setting_action,
    )
    page.overlay.append(settings_dialog)

    left_title = build_sample_title(colors)
    center_title = build_center_title(colors)
    right_title = build_template_title(colors)

    left_panel = build_sample_panel(
        left_title,
        check_list_col,
        clear_all_samples,
        colors,
    )
    center_panel = build_center_panel(
        center_title,
        main_display_col,
        open_settings,
        run_excel,
        colors,
    )
    right_panel = build_template_panel(
        right_title,
        tmp_input,
        template_list_col,
        save_template,
        colors,
    )

    reload_sample_list()
    update_template_ui()

    page.add(
        build_main_layout(
            left_panel,
            center_panel,
            right_panel,
        )
    )
    rebuild_main_view()


if __name__ == "__main__":
    ft.app(target=main)
