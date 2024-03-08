import flet as ft
import requests
import json

server='http://127.0.0.1:8000'


def get_books():
    path = "/books"
    r=requests.get(server+path)
#    print(r.json())
    return r.json()
        

def prepare_rows(books):
  books_array = data = json.loads(books)
  dataRows = []
  for book in books_array:
      row = ft.DataRow(cells=[
         ft.DataCell(ft.Text(book['Book Name'])),
                     ft.DataCell(ft.Text(book['Author'])),
                     ft.DataCell(ft.Text(book['Availability'])),
      ],
      color = {"hovered": ft.colors.BLACK})
      dataRows.append(row)
  return dataRows
  

def main(page: ft.Page):
    # Setting the background color of the page
    page.bgcolor = "#083b7a"
    page.padding = 50
    page.scroll = ft.ScrollMode.HIDDEN

    books = get_books()

    title = str("Our Books!")
    title_text = ft.Text(title,
                   font_family="Calibiri",
                   theme_style=ft.TextThemeStyle.DISPLAY_LARGE,
                   text_align=ft.TextAlign.CENTER,
                   color=ft.colors.BLACK54)
    
    page.add(title_text)

    page.add(
            ft.DataTable(
                width = page.width,
                horizontal_lines=ft.border.BorderSide(1, "white"),
                #bgcolor=ft.colors.LIGHT_BLUE_900,
                data_row_color={"hovered": ft.colors.WHITE},
                heading_row_color=ft.colors.BLACK12,
                column_spacing=200,
                columns=[
                    ft.DataColumn(
                        ft.Text("Book Name"),
                        on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                    ),
                    ft.DataColumn(
                        ft.Text("Author"),
                        on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                    ),
                    ft.DataColumn(
                        ft.Text("Availability"),
                        numeric=True,
                        on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                    ),
                ],
                rows=prepare_rows(books),
            ),
        )    


ft.app(target=main)