import flet as ft


def build_center_panel(
    title,
    main_display_col,
    on_open_settings,
    on_run_excel,
    colors,
):
    return ft.Container(
        expand=True,
        bgcolor=colors["panel"],
        border_radius=10,
        padding=15,
        content=ft.Column(
            [
                ft.Row(
                    [
                        title,
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    "Settings",
                                    on_click=on_open_settings,
                                ),
                                ft.ElevatedButton(
                                    "Export Excel",
                                    bgcolor="green",
                                    color="white",
                                    on_click=on_run_excel,
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


def build_center_title(colors):
    return ft.Text(
        "NMR Manager",
        size=24,
        weight="bold",
        color=colors["text"],
    )


def build_main_layout(
    left_panel,
    center_panel,
    right_panel,
):
    return ft.Row(
        [
            left_panel,
            center_panel,
            right_panel,
        ],
        expand=True,
    )
