import flet as ft


def build_template_panel(
    title,
    tmp_input,
    template_list_col,
    on_save_template,
    colors,
):
    return ft.Container(
        width=300,
        bgcolor=colors["panel2"],
        border_radius=10,
        padding=15,
        content=ft.Column(
            [
                title,
                ft.Row(
                    [
                        tmp_input,
                        ft.ElevatedButton(
                            "Save",
                            on_click=on_save_template,
                        ),
                    ]
                ),
                ft.Divider(),
                template_list_col,
            ]
        ),
    )


def build_template_title(colors):
    return ft.Text(
        "Templates",
        size=20,
        weight="bold",
        color=colors["text"],
    )


def build_template_input():
    return ft.TextField(
        label="Name",
        width=150,
        dense=True,
    )
