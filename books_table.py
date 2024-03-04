import flet as ft


def main(page: ft.Page):
    # Setting the background color of the page
    page.bgcolor = "#083b7a"
    page.padding = 50

    page.add(
    ft.DataTable(
        #width=700,
        bgcolor="white",
        border=ft.border.all(2, "black"),
        border_radius=10,
        vertical_lines=ft.border.BorderSide(1, "blue"),
        horizontal_lines=ft.border.BorderSide(1, "blue"),
        sort_column_index=0,
        sort_ascending=True,
        heading_row_color=ft.colors.BLACK12,
        heading_row_height=100,
        data_row_color={"hovered": "grey"},
        divider_thickness=0,
        column_spacing=200,
        columns=[
            ft.DataColumn(
                ft.Text("Name", color="black", text_align=ft.alignment.center),
                on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
            ),
            ft.DataColumn(
                ft.Text("Author", color="black"),
                tooltip="This is a second column",
                numeric=True,
                on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
            ),
        ],
        rows=[
            ft.DataRow(
                [ft.DataCell(ft.Text("A")), ft.DataCell(ft.Text("1"))],
                selected=True,
                on_select_changed=lambda e: print(f"row select changed: {e.data}"),
            ),
            ft.DataRow([ft.DataCell(ft.Text("B")), ft.DataCell(ft.Text("2"))]),
        ],
    ),
)


ft.app(target=main)