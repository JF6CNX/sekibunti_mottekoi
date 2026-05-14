import os

import flet as ft

from nmr_manager.excel_files import (
    format_file_size,
    list_excel_files,
    move_all_excel_files_to_trash,
    move_excel_file_to_trash,
    restore_excel_files,
)
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
    apply_layout_background,
    apply_panel_background,
    build_center_panel,
    build_center_title,
    build_excel_dialog,
    build_excel_file_row,
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
    main_layout = None

    main_display_col = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.ALWAYS,
    )
    check_list_col = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.ALWAYS,
    )
    template_list_col = ft.Column()
    excel_list_col = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.ALWAYS,
    )
    stats_text = ft.Text(
        "Selected: 0 / Peaks: 0 / Export ready: 0",
        size=12,
    )
    tmp_input = build_template_input()
    rename_template_name = None
    last_undo = {
        "label": None,
        "action": None,
    }
    rename_template_input = ft.TextField(
        label="New name",
        width=280,
    )

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

    def set_undo(label, action):
        last_undo["label"] = label
        last_undo["action"] = action

    def run_undo(e):
        action = last_undo["action"]
        label = last_undo["label"]

        if action is None:
            show_message("nothing to undo", "blue")
            return

        try:
            action()
            last_undo["label"] = None
            last_undo["action"] = None
            show_message(f"undone: {label}", "blue")
        except Exception as err:
            show_message(error_message(err), "red")

    def sort_sample_names(sample_names):
        favorites = set(settings.get("favorite_samples", []))
        return sorted(
            sample_names,
            key=lambda name: (name not in favorites, name.lower()),
        )

    def update_stats():
        selected_count = len(state.selected_samples)
        peak_count = sum(
            len(state.get_order(sample_name))
            for sample_name in state.selected_samples
        )
        export_ready_count = sum(
            1
            for sample_name in state.selected_samples
            if state.get_order(sample_name)
        )
        stats_text.value = (
            f"Selected: {selected_count} / "
            f"Peaks: {peak_count} / "
            f"Export ready: {export_ready_count}"
        )

    def apply_theme():
        nonlocal colors

        page.theme_mode = get_theme_mode(settings["theme_mode"])
        colors = get_colors(settings["theme_mode"])
        page.bgcolor = colors["bg"]

        if main_layout is not None:
            apply_layout_background(main_layout, colors)

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

    def close_excel_dialog(e=None):
        excel_dialog.open = False
        page.update()

    def open_excel_dialog(e):
        refresh_excel_files()
        excel_dialog.open = True
        page.update()

    def open_excel_file(path):
        try:
            os.startfile(path)
        except Exception as err:
            show_message(error_message(err), "red")

    def delete_one_excel_file(path):
        try:
            moved_file = move_excel_file_to_trash(path, settings["output_dir"])

            def undo_delete():
                restore_excel_files([moved_file])
                refresh_excel_files()

            set_undo("delete excel file", undo_delete)
            refresh_excel_files()
            show_message("excel file deleted. Undo is available.", "red")
        except Exception as err:
            show_message(error_message(err), "red")

    def open_delete_all_excel_confirm(e):
        delete_all_excel_dialog.open = True
        page.update()

    def close_delete_all_excel_confirm(e=None):
        delete_all_excel_dialog.open = False
        page.update()

    def delete_all_excel_action(e):
        try:
            moved_files = move_all_excel_files_to_trash(settings["output_dir"])
            deleted_count = len(moved_files)

            def undo_delete_all():
                restore_excel_files(moved_files)
                refresh_excel_files()

            set_undo("delete all excel files", undo_delete_all)
            close_delete_all_excel_confirm()
            refresh_excel_files()
            show_message(f"deleted {deleted_count} excel files. Undo is available.", "red")
        except Exception as err:
            show_message(error_message(err), "red")

    def refresh_excel_files(e=None):
        excel_files = list_excel_files(settings["output_dir"])

        if not excel_files:
            excel_list_col.controls = [
                ft.Text("No Excel files found.")
            ]
            page.update()
            return

        excel_list_col.controls = [
            build_excel_file_row(
                item,
                format_file_size(item["size"]),
                open_excel_file,
                delete_one_excel_file,
            )
            for item in excel_files
        ]
        page.update()

    def on_check(e):
        sample_name = e.control.data

        if e.control.value:
            state.select_sample(sample_name)
        else:
            state.unselect_sample(sample_name)

        rebuild_main_view()

    def toggle_favorite_sample(sample_name):
        favorites = settings.setdefault("favorite_samples", [])

        if sample_name in favorites:
            favorites.remove(sample_name)
        else:
            favorites.append(sample_name)

        save_settings(settings)
        reload_sample_list()

    def reload_sample_list():
        state.set_sample_groups(scan_samples(settings["input_dir"]))
        state.samples_keys = sort_sample_names(state.samples_keys)
        check_list_col.controls.clear()
        state.checkbox_refs.clear()

        for sample_name in state.samples_keys:
            is_favorite = sample_name in settings.get("favorite_samples", [])
            checkbox = ft.Checkbox(
                label=sample_name,
                data=sample_name,
                on_change=on_check,
                value=sample_name in state.selected_samples,
            )
            state.checkbox_refs[sample_name] = checkbox
            check_list_col.controls.append(
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "*" if is_favorite else "+",
                            width=42,
                            bgcolor="#FFD400" if is_favorite else None,
                            color="black" if is_favorite else None,
                            on_click=lambda e, sn=sample_name: (
                                toggle_favorite_sample(sn)
                            ),
                        ),
                        checkbox,
                    ],
                    spacing=4,
                )
            )

        page.update()

    def remove_sample_direct(sample_name):
        state.unselect_sample(sample_name)

        if sample_name in state.checkbox_refs:
            state.checkbox_refs[sample_name].value = False

        rebuild_main_view()

    def clear_all_samples(e):
        selected_snapshot = list(state.selected_samples)
        order_snapshot = {
            sample_name: list(order)
            for sample_name, order in state.sample_order_map.items()
        }

        def undo_clear():
            state.selected_samples = list(selected_snapshot)
            state.sample_order_map = {
                sample_name: list(order)
                for sample_name, order in order_snapshot.items()
            }

            for sample_name, checkbox in state.checkbox_refs.items():
                checkbox.value = sample_name in state.selected_samples

            rebuild_main_view()

        set_undo("clear selected samples", undo_clear)
        state.clear_samples()
        rebuild_main_view()
        show_message("selection cleared. Undo is available.", "red")

    def toggle_number(sample_name, number):
        state.toggle_number(sample_name, number)
        rebuild_main_view()

    def rebuild_main_view():
        apply_theme()
        update_stats()

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

        apply_panel_background(left_panel, colors, "panel2")
        apply_panel_background(center_panel, colors, "panel")
        apply_panel_background(right_panel, colors, "panel2")

        left_title.color = colors["text"]
        center_title.color = colors["text"]
        right_title.color = colors["text"]
        stats_text.color = colors["text"]

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

        deleted_order = list(custom_templates[name])

        def undo_delete_template():
            custom_templates[name] = list(deleted_order)
            save_templates(custom_templates)
            update_template_ui()

        set_undo("delete template", undo_delete_template)
        del custom_templates[name]
        save_templates(custom_templates)
        update_template_ui()
        show_message(f"template deleted: {name}. Undo is available.", "red")

    def open_rename_template_dialog(name):
        nonlocal rename_template_name

        rename_template_name = name
        rename_template_input.value = name
        rename_template_dialog.open = True
        page.update()

    def close_rename_template_dialog(e=None):
        rename_template_dialog.open = False
        page.update()

    def rename_template_action(e):
        nonlocal rename_template_name

        old_name = rename_template_name
        new_name = rename_template_input.value.strip()

        if not old_name or not new_name:
            return

        if old_name == new_name:
            close_rename_template_dialog()
            return

        if new_name in custom_templates:
            show_message("template name already exists", "red")
            return

        custom_templates[new_name] = custom_templates.pop(old_name)
        save_templates(custom_templates)
        rename_template_name = None
        close_rename_template_dialog()
        update_template_ui()
        show_message(f"template renamed: {new_name}", "blue")

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
                        "Rename",
                        width=85,
                        on_click=lambda e, template_name=name: (
                            open_rename_template_dialog(template_name)
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

    excel_dialog = build_excel_dialog(
        excel_list_col,
        close_excel_dialog,
        refresh_excel_files,
        open_delete_all_excel_confirm,
    )
    page.overlay.append(excel_dialog)

    delete_all_excel_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Delete all Excel files?"),
        content=ft.Text("This deletes all .xlsx files in the output folder."),
        actions=[
            ft.TextButton(
                "Cancel",
                on_click=close_delete_all_excel_confirm,
            ),
            ft.ElevatedButton(
                "Delete all",
                bgcolor="red",
                color="white",
                on_click=delete_all_excel_action,
            ),
        ],
    )
    page.overlay.append(delete_all_excel_dialog)

    rename_template_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Rename template"),
        content=rename_template_input,
        actions=[
            ft.TextButton(
                "Cancel",
                on_click=close_rename_template_dialog,
            ),
            ft.ElevatedButton(
                "Rename",
                on_click=rename_template_action,
            ),
        ],
    )
    page.overlay.append(rename_template_dialog)

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
        stats_text,
        main_display_col,
        open_settings,
        run_excel,
        open_excel_dialog,
        run_undo,
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

    main_layout = build_main_layout(
        left_panel,
        center_panel,
        right_panel,
        colors,
    )

    page.add(main_layout)
    rebuild_main_view()


if __name__ == "__main__":
    ft.app(target=main)
