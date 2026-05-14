import flet as ft


def build_excel_dialog(
    excel_list_col,
    on_close,
    on_refresh,
    on_delete_all,
):
    return ft.AlertDialog(
        modal=True,
        title=ft.Text("Excel files"),
        content=ft.Container(
            width=720,
            height=520,
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "Refresh",
                                on_click=on_refresh,
                            ),
                            ft.ElevatedButton(
                                "Delete all",
                                bgcolor="red",
                                color="white",
                                on_click=on_delete_all,
                            ),
                        ],
                        alignment="spaceBetween",
                    ),
                    ft.Divider(),
                    excel_list_col,
                ]
            ),
        ),
        actions=[
            ft.TextButton(
                "Close",
                on_click=on_close,
            ),
        ],
    )


def build_excel_file_row(item, size_label, on_open, on_delete):
    return ft.Container(
        padding=8,
        border=ft.border.all(1, "#555555"),
        border_radius=8,
        content=ft.Row(
            [
                ft.Column(
                    [
                        ft.Text(
                            item["name"],
                            weight="bold",
                        ),
                        ft.Text(
                            f'{item["modified_label"]} / {size_label}',
                            size=12,
                        ),
                    ],
                    expand=True,
                    spacing=2,
                ),
                ft.ElevatedButton(
                    "Open",
                    on_click=lambda e, path=item["path"]: on_open(path),
                ),
                ft.ElevatedButton(
                    "Delete",
                    bgcolor="red",
                    color="white",
                    on_click=lambda e, path=item["path"]: on_delete(path),
                ),
            ]
        ),
    )
