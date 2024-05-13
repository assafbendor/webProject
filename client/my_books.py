import os

import flet as ft
import requests

import client_config


class MyBooks:

    def __init__(self, page):
        super().__init__()
        self.page = page

    def get_books(self):
        path = "/book_list"

        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f"Bearer {self.page.client_storage.get('token')}"
        }

        params = {
            "username": self.page.client_storage.get("username")
        }

        try:
            r = requests.get(client_config.SERVER_URL + path, params=params, headers=headers)
            r.raise_for_status()
            books = r.json()
            return books
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print("Failed to make the get request: ", client_config.SERVER_URL + path, " Error: ", err)

    def prepare_rows(self):

        dataRows = []

        books = self.get_books()
        for book in books:
            row = ft.DataRow(
                cells=[
                    ft.DataCell(
                        ft.Image(src=f"{os.path.join(os.getcwd(), 'img', book['cover_image_filename'])}",
                                 height=45,
                                 width=30)),
                    ft.DataCell(ft.Text(book['title'])),
                    ft.DataCell(ft.Text(book['author']['name'])),
                    ft.DataCell(ft.Text("borrow date")),
                    ft.DataCell(ft.Text("due date")),
                ],
                )

            dataRows.append(row)
        return dataRows

    def build(self):
        self.page.scroll = ft.ScrollMode.HIDDEN
        self.page.update()

        table = ft.DataTable(
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
                    ft.Text("Borrow Date"),
                    on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),
                ft.DataColumn(
                    ft.Text("Due Date"),
                    on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),
            ],
            rows=self.prepare_rows(),
        )

        return table
