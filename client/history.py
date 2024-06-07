import os
from datetime import datetime

import flet as ft
import requests

import client_config
import single_book

class History:

    def __init__(self, page: ft.Page):
        super().__init__()
        self.table = None
        self.page = page
        self.single_book = single_book.SingleBook(page)

    def get_history(self, username):

        path = "/history"

        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f"Bearer {self.page.client_storage.get('token')}"
        }

        params = {
            "username": username
        }

        try:
            r = requests.get(client_config.SERVER_URL + path, headers=headers, params=params)
            r.raise_for_status()
            borrow = r.json()
            return borrow
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print("Failed to make the get request: ", client_config.SERVER_URL + path, " Error: ", err)

    def prepare_rows(self):

        borrows = self.get_history(self.page.client_storage.get("username"))

        dataRows = []
        for borrow in borrows:
            row = ft.DataRow(
                cells=[
                    ft.DataCell(
                        ft.Image(
                            src=f"{client_config.SERVER_URL}/photos/borrow['copy']['book']['cover_image_filename']",
                            height=45,
                            width=30)),
                    ft.DataCell(ft.Text(borrow['copy']['book']['title'])),
                    ft.DataCell(ft.Text(borrow['copy']['book']['author']['name'])),
                    ft.DataCell(ft.Text(datetime.fromisoformat(borrow['borrow_date']).strftime("%d/%m/%Y"))),
                    ft.DataCell(ft.Text(datetime.fromisoformat(borrow['borrow_date']).strftime("%d/%m/%Y"))),
                ],
            )

            dataRows.append(row)
        return dataRows

    def build(self):
        self.page.scroll = ft.ScrollMode.HIDDEN
        self.page.update()

        def back():
            self.page.views.pop()
            self.page.update()

        history_text = ft.Text("Here is the history of books you borrowed:", color=ft.colors.LIGHT_BLUE_200)

        column = ft.Column(
            controls=[history_text,
                      ft.DataTable(
                          width=self.page.width,
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
                                  ft.Text("Return Date"),
                                  on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                              ),
                          ],
                          rows=self.prepare_rows(),
                      ),
                ]
        )

        return column
