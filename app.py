import flet as ft
from nmr_excelsekibunti.core.excel_writer import write_excel_from_integrals

def main(page: ft.Page):
    page.title = "NMR積分データ自動集計ツール"
    
    input_dir_text = ft.Text("未選択")
    output_file_text = ft.Text("未選択")

    # 型ヒントを外して、実行時のエラーを回避
    def on_dir_result(e):
        if e.path:
            input_dir_text.value = e.path
            page.update()

    def on_file_result(e):
        if e.path:
            path = e.path if e.path.lower().endswith(".xlsx") else e.path + ".xlsx"
            output_file_text.value = path
            page.update()

    dir_picker = ft.FilePicker(on_result=on_dir_result)
    file_picker = ft.FilePicker(on_result=on_file_result)
    page.overlay.extend([dir_picker, file_picker])

    def run_process(e):
        if input_dir_text.value == "未選択" or output_file_text.value == "未選択":
            return
        try:
            write_excel_from_integrals(input_dir_text.value, output_file_text.value)
            page.add(ft.Text("完了！", color="green"))
        except Exception as ex:
            page.add(ft.Text(f"エラー: {ex}", color="red"))

    page.add(
        ft.ElevatedButton("フォルダ選択", on_click=lambda _: dir_picker.get_directory_path()),
        input_dir_text,
        ft.ElevatedButton("保存先選択", on_click=lambda _: file_picker.save_file()),
        output_file_text,
        ft.ElevatedButton("実行", on_click=run_process)
    )

ft.app(target=main)