import flet as ft


def build_sample_panel(
    title,
    check_list_col,
    on_clear_all,
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
                ft.Divider(),
                ft.ElevatedButton(
                    "Clear all",
                    on_click=on_clear_all,
                ),
                check_list_col,
            ]
        ),
    )


def build_sample_title(colors):
    return ft.Text(
        "Samples",
        size=20,
        weight="bold",
        color=colors["text"],
    )
