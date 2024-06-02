import os

import flet as ft
import requests

import client_config
import single_book


class BookList:

    def __init__(self, page: ft.Page):
        super().__init__()
        self.table = None
        self.page = page
        self.single_book = single_book.SingleBook(page)

    def reserve_book(self, e):
        path = "/reserve"

        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f"Bearer {self.page.client_storage.get('token')}"
        }

        params = {
            'username': self.page.client_storage.get('username'),
            'isbn': e.data
        }

        try:
            r = requests.post(client_config.SERVER_URL + path, headers=headers, params=params)
            r.raise_for_status()
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print("Failed to make the get request: ", client_config.SERVER_URL + path, " Error: ", err)

    def show_book_details(self, e):
        self.single_book.open_book_dlg(e)

    def get_books(self):
        path = "/books"

        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f"Bearer {self.page.client_storage.get('token')}"
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
        def get_on_click(book):
            return lambda e: self.single_book.open_book_dlg(e=ft.ControlEvent(
                control=None,
                name="Trending Book Clicked",
                page=self.page,
                data=book,
                target=''))

        def reserve_book_clicked(isbn):
            return lambda e: self.reserve_book(e=ft.ControlEvent(
                control=None,
                name="Reserve Book Clicked",
                page=self.page,
                data=isbn,
                target=''))

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
                        ft.PopupMenuItem(text="Reserve", on_click=reserve_book_clicked(book['isbn'])),
                        ft.PopupMenuItem(text="Show Details", on_click=get_on_click(book)),
                    ],
                        tooltip=None),
                    )
                ], )

            dataRows.append(row)
        return dataRows

    def build(self, books):
        self.page.scroll = ft.ScrollMode.HIDDEN
        self.page.update()

        def back():
            self.page.views.pop()
            self.page.update()

        column = ft.Column(
            controls=[ft.DataTable(
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
            ),
                ft.TextButton("Back",
                              on_click=lambda e: back(),
                              icon=ft.icons.ARROW_BACK)
            ]
        )

        return column
