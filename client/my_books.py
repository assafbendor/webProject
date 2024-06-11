import os
from datetime import datetime

import flet as ft
import requests

import client_config


class MyBooks:

    def __init__(self, page):
        super().__init__()
        self.page = page

    def get_reservations(self, username):
        path = "/reservations"

        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f"Bearer {self.page.client_storage.get('token')}"
        }

        params = {
            "username": username
        }

        try:
            r = requests.get(client_config.SERVER_URL + path, params=params, headers=headers)
            r.raise_for_status()
            reservations = r.json()
            return reservations
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print("Failed to make the get request: ", client_config.SERVER_URL + path, " Error: ", err)

    def get_borrows(self, username):
        path = "/book_list"

        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f"Bearer {self.page.client_storage.get('token')}"
        }

        params = {
            "username": username
        }

        try:
            r = requests.get(client_config.SERVER_URL + path, params=params, headers=headers)
            r.raise_for_status()
            borrows = r.json()
            return borrows
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print("Failed to make the get request: ", client_config.SERVER_URL + path, " Error: ", err)

    def prepare_rows(self, username):

        def get_status(borrow_status):
            if datetime.fromisoformat(borrow_status['due_date']) < datetime.now():
                return ft.Text("Late", bgcolor=ft.colors.RED)
            else:
                return ft.Text("On Time", bgcolor=ft.colors.GREEN)

        dataRows = []

        borrows = self.get_borrows(username)
        for borrow in borrows:
            row = ft.DataRow(
                cells=[
                    ft.DataCell(
                        ft.Image(src=f"{client_config.SERVER_URL}/photos/{borrow['copy']['book']['cover_image_filename']}",
                                 height=45,
                                 width=30)),
                    ft.DataCell(ft.Text(borrow['copy']['book']['title'])),
                    ft.DataCell(ft.Text(borrow['copy']['book']['author']['name'])),
                    ft.DataCell(ft.Text(datetime.fromisoformat(borrow['borrow_date']).strftime("%d/%m/%Y"))),
                    ft.DataCell(ft.Text(datetime.fromisoformat(borrow['due_date']).strftime("%d/%m/%Y"))),
                    ft.DataCell(get_status(borrow))
                ],

                )

            dataRows.append(row)
        return dataRows

    def prepare_rows_reservations(self, username):

        dataRows = []

        reservations = self.get_reservations(username)
        for reservation in reservations:
            row = ft.DataRow(
                cells=[
                    ft.DataCell(
                        ft.Image(src=f"{client_config.SERVER_URL}/photos/{reservation['book']['cover_image_filename']}",
                                 height=45,
                                 width=30)),
                    ft.DataCell(ft.Text(reservation['book']['title'])),
                    ft.DataCell(ft.Text(reservation['book']['author']['name'])),
                    ft.DataCell(ft.Text(datetime.fromisoformat(reservation['date']).strftime("%d/%m/%Y"))),
                ],
                )

            dataRows.append(row)
        return dataRows

    def build(self):
        self.page.scroll = ft.ScrollMode.HIDDEN
        self.page.update()

        borrows_text = ft.Text("You currently have the following borrowed books:", color=ft.colors.LIGHT_BLUE_200)
        borrows = self.get_user_books_table(self.page.client_storage.get("username"))
        reservation_text = ft.Text("You currently have the following reserved books:", color=ft.colors.LIGHT_BLUE_200)
        reservations = self.get_user_reservation_table(self.page.client_storage.get("username"))

        return ft.Column(controls=[borrows_text, borrows, reservation_text, reservations], spacing=25)

    def get_user_books_table(self, username):
        table = ft.DataTable(
            width=self.page.width,
            horizontal_lines=ft.border.BorderSide(1, "white"),
            horizontal_margin=15,
            data_row_color={ft.MaterialState.HOVERED: ft.colors.WHITE},
            heading_row_color=ft.colors.BLACK45,
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
                ft.DataColumn(
                    ft.Text("Status"),
                    on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),
            ],
            rows=self.prepare_rows(username),
        )
        return table

    def get_user_reservation_table(self, username):
        table = ft.DataTable(
            width=self.page.width,
            horizontal_lines=ft.border.BorderSide(1, "white"),
            horizontal_margin=15,
            data_row_color={ft.MaterialState.HOVERED: ft.colors.WHITE},
            heading_row_color=ft.colors.BLACK45,
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
                    ft.Text("Reservation Date"),
                    on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),
            ],
            rows=self.prepare_rows_reservations(username),
        )
        return table
