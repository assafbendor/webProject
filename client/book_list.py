from datetime import datetime
import json
import os
import flet as ft
import requests
import client_config
from client.access_token import get_access_token


class BookList:

    def __init__(self, appLayout):
        super().__init__()
        self.table = None
        self.appLayout = appLayout

    # def row_selected(self, e):
    #     e.control.selected = not e.control.selected
    #     self.appLayout.page.update()

    def borrow_book(self, e):
        pass

    def reserve_book(self, e):
        pass

    def show_book_details(self, e):
        pass

    def get_books(self):
        path = "/books"

        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f"Bearer {get_access_token()}"
        }

        try:
            r = requests.get(client_config.SERVER_URL + path, headers=headers)
            r.raise_for_status()
            books = r.json()
            return books
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print("Failed to make the get request: ", client_config.SERVER_URL + path, " Error: ", err)

    def prepare_rows(self, books):
        dataRows = []
        for book in books:
            row = ft.DataRow(
                cells=[
                    ft.DataCell(
                        ft.Image(src=f"{os.path.join(os.getcwd(), 'img', book['cover_image_filename'])}",
                                 height=45,
                                 width=30)),
                    ft.DataCell(ft.Text(book['title'])),
                    ft.DataCell(ft.Text(book['author']['name'])),
                    ft.DataCell(ft.PopupMenuButton(items=[
                        ft.PopupMenuItem(text="Borrow", on_click=self.borrow_book),
                        ft.PopupMenuItem(text="Reserve", on_click=self.reserve_book),
                        ft.PopupMenuItem(text="Show Details", on_click=self.show_book_details),
                     ],), )
                ],)

            dataRows.append(row)
        return dataRows

    def build(self, books):
        self.appLayout.page.scroll = ft.ScrollMode.HIDDEN
        self.appLayout.page.update()

        self.table = ft.DataTable(
            # width=self.appLayout.page.width,
            show_checkbox_column=True,
            horizontal_lines=ft.border.BorderSide(1, "white"),
            horizontal_margin=15,
            data_row_color={ft.MaterialState.HOVERED: ft.colors.WHITE},
            heading_row_color=ft.colors.BLACK12,
            column_spacing=20,
            columns=[
                ft.DataColumn(
                    ft.Text("Book Cover"),
                ),
                ft.DataColumn(
                    ft.Text("Book Name"),
                    on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),
                ft.DataColumn(
                    ft.Text("Author"),
                    on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),
                ft.DataColumn(
                    ft.Text("Actions"),
                    on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),
            ],
            rows=self.prepare_rows(books),
        )

        return self.table
