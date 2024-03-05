import flet as ft
import requests
import json

server='http://127.0.0.1:8000'


def get_books():
    path = "/books"
    r=requests.get(server+path)
    return r.json
        

def prepare_rows(books):

    json.loads(books)

    # rows = []
    # for i in books:
 
 #       print(i)
        # rows.append(ft.DataRow([ft.DataCell(ft.Text(i[0])),
        #                          0,
        #                          0,
        #                          0]))
    # return rows    

def main(page: ft.Page):
    # Setting the background color of the page
    page.bgcolor = "#083b7a"
    page.padding = 50

    books = get_books

    page.add(
            ft.DataTable(
                horizontal_lines=ft.border.BorderSide(1, "white"),
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
                        ft.Text("Available Copies"),
                        numeric=True,
                        on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                    ),
                    ft.DataColumn(
                        ft.Text("Availability"),
                        on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                    ),
                ],
                rows=prepare_rows(books),
            ),
        )    


ft.app(target=main)