import flet as ft


def build_settings_dialog(
    input_dir_field,
    output_dir_field,
    theme_dropdown,
    auto_open_switch,
    on_close,
    on_save,
):
    return ft.AlertDialog(
        modal=True,
        title=ft.Text("Settings"),
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
                "Cancel",
                on_click=on_close,
            ),
            ft.ElevatedButton(
                "Save",
                on_click=on_save,
            ),
        ],
    )


def build_settings_fields(settings):
    input_dir_field = ft.TextField(
        label="NMR input folder",
        value=settings["input_dir"],
    )
    output_dir_field = ft.TextField(
        label="Excel output folder",
        value=settings["output_dir"],
    )
    theme_dropdown = ft.Dropdown(
        label="Theme",
        value=settings["theme_mode"],
        options=[
            ft.dropdown.Option("dark"),
            ft.dropdown.Option("light"),
        ],
    )
    auto_open_switch = ft.Switch(
        label="Open Excel after export",
        value=settings["auto_open_excel"],
    )

    return (
        input_dir_field,
        output_dir_field,
        theme_dropdown,
        auto_open_switch,
    )
