import flet as ft


def build_center_panel(
    title,
    stats_control,
    main_display_col,
    on_open_settings,
    on_run_excel,
    on_open_excel_files,
    on_undo,
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
                        ft.Column(
                            [
                                title,
                                stats_control,
                            ],
                            spacing=2,
                        ),
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    "Undo",
                                    on_click=on_undo,
                                ),
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
                                ft.ElevatedButton(
                                    "Excel Files",
                                    on_click=on_open_excel_files,
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
    colors=None,
):
    layout = ft.Container(
        expand=True,
        padding=0,
        content=ft.Row(
            [
                left_panel,
                center_panel,
                right_panel,
            ],
            expand=True,
        ),
    )

    if colors is not None:
        apply_layout_background(layout, colors)

    return layout


def apply_layout_background(layout, colors):
    if "bg_gradient" in colors:
        layout.bgcolor = None
        layout.gradient = ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=colors["bg_gradient"],
        )
        return

    layout.gradient = None
    layout.bgcolor = colors["bg"]


def apply_panel_background(panel, colors, color_key):
    gradient_key = f"{color_key}_gradient"

    if gradient_key in colors:
        panel.bgcolor = None
        panel.gradient = ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=colors[gradient_key],
        )
        return

    panel.gradient = None
    panel.bgcolor = colors[color_key]
