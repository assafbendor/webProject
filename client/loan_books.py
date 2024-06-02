import flet as ft
import requests

import client_config
from client.my_books import MyBooks


class LoanBooks:

    def __init__(self, page):
        super().__init__()
        self.reservations_table_header_text = None
        self.reader_reservations = None
        self.table_header_text = None
        self.table_column = None
        self.view = None
        self.readers_dropdown = None
        self.page = page
        self.my_books = MyBooks(self.page)
        self.selected_reader = None

        self.isbn_text = ft.Text("Select an ISBN and click borrow/return",
                                 theme_style=ft.TextThemeStyle.BODY_MEDIUM)

        self.borrow_isbn = ft.TextField(label="ISBN",
                                        focused_color=ft.colors.BLACK87,
                                        color=ft.colors.BLACK87,
                                        bgcolor=ft.colors.WHITE,
                                        border_color=ft.colors.BLACK54,
                                        focused_border_color=ft.colors.BLACK,
                                        height=40,
                                        border_radius=15,
                                        content_padding=ft.padding.only(top=2, bottom=2, left=6),
                                        cursor_height=14,
                                        cursor_color=ft.colors.BLACK54,
                                        width=250)

        self.loan_book_button = ft.ElevatedButton(text="Loan Book",
                                                  on_click=self.borrow_clicked)

        self.return_book_button = ft.ElevatedButton(text="Return Book",
                                                    on_click=self.return_clicked)

        self.actions_row = ft.Row(controls=[self.loan_book_button, self.return_book_button], spacing=25)
        self.actions_and_isbn = ft.Column(controls=[self.isbn_text, self.borrow_isbn, self.actions_row, ],
                                          visible=False)

        self.borrow_result = ft.TextButton(
            visible=False,
            content=ft.Container(
                content=ft.Text("Action Completed Successfully!", color=ft.colors.WHITE, size=15),
                bgcolor=ft.colors.GREEN,
                padding=ft.padding.all(10),
            )

        )

        self.reader_books = ft.Container()
        self.reader_reservations = ft.Container()

    def borrow_clicked(self, e):
        self.borrow_result.visible = False

        path = "/borrow_book"

        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f"Bearer {self.page.client_storage.get('token')}"
        }

        params = {
            'book_isbn': self.borrow_isbn.value,
            'username': self.readers_dropdown.value
        }

        try:
            r = requests.post(client_config.SERVER_URL + path, params=params, headers=headers)
            r.raise_for_status()
            self.reader_books.content = self.my_books.get_user_books_table(self.selected_reader)
            self.reader_reservations.content = self.my_books.get_user_reservation_table(self.selected_reader)
            self.borrow_result.visible = True
            self.page.update()
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            if r is not None:
                response_json = r.json()
                self.borrow_result.content.content = ft.Text(response_json['detail'], color=ft.colors.WHITE, size=15)
                self.borrow_result.content.bgcolor = ft.colors.RED
                self.borrow_result.visible = True
                self.page.update()
        except Exception as err:
            if r is not None:
                self.borrow_result.content.content = ft.Text(r.json()['detail'], color=ft.colors.WHITE, size=15),
                self.borrow_result.content.bgcolor = ft.colors.RED
                self.borrow_result.visible = True
                self.page.update()
            print("Failed to make the get request: ", client_config.SERVER_URL + path, " Error: ", err)
            self.page.update()

    def return_clicked(self, e):
        self.borrow_result.visible = False

        path = "/return_book"

        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f"Bearer {self.page.client_storage.get('token')}"
        }

        params = {
            'book_isbn': self.borrow_isbn.value,
            'username': self.readers_dropdown.value
        }

        try:
            r = requests.post(client_config.SERVER_URL + path, params=params, headers=headers)
            r.raise_for_status()
            self.reader_books.content = self.my_books.get_user_books_table(self.selected_reader)
            self.borrow_result.visible = True
            self.page.update()
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            if r is not None:
                response_json = r.json()
                self.borrow_result.content.content = ft.Text(response_json['detail'], color=ft.colors.WHITE, size=15)
                self.borrow_result.content.bgcolor = ft.colors.RED
                self.borrow_result.visible = True
                self.page.update()
        except Exception as err:
            if r is not None:
                self.borrow_result.content.content = ft.Text(r.json()['detail'], color=ft.colors.WHITE, size=15),
                self.borrow_result.content.bgcolor = ft.colors.RED
                self.borrow_result.visible = True
                self.page.update()
            print("Failed to make the get request: ", client_config.SERVER_URL + path, " Error: ", err)
            self.page.update()

    def get_readers(self):
        path = "/get_readers"

        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f"Bearer {self.page.client_storage.get('token')}"
        }

        try:
            r = requests.get(client_config.SERVER_URL + path, headers=headers)
            r.raise_for_status()
            readers = r.json()
            return readers
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print("Failed to make the get request: ", client_config.SERVER_URL + path, " Error: ", err)

    def reader_selected(self, e):
        self.selected_reader = self.readers_dropdown.value
        self.reader_books.content = self.my_books.get_user_books_table(self.selected_reader)
        self.reader_reservations.content = self.my_books.get_user_reservation_table(self.selected_reader)
        self.table_header_text.value = "Books currently borrowed by " + self.selected_reader
        self.reservations_table_header_text.value = "Books currently reserved by " + self.selected_reader
        self.table_column.visible = True
        self.actions_and_isbn.visible = True
        self.page.update()
        print(self.selected_reader)

    def build(self):
        readers = self.get_readers()
        dropdown_text = ft.Text("Select Reader:")
        self.readers_dropdown = ft.Dropdown(
            on_change=self.reader_selected,
            options=[ft.dropdown.Option(reader['username']) for reader in readers],
        )

        dropdown_row = ft.Row(controls=[dropdown_text, self.readers_dropdown])

        self.table_header_text = ft.Text("", theme_style=ft.TextThemeStyle.HEADLINE_SMALL)
        self.reservations_table_header_text = ft.Text("", theme_style=ft.TextThemeStyle.HEADLINE_SMALL)

        self.table_column = ft.Column(controls=[self.table_header_text,
                                                self.reader_books,
                                                self.reservations_table_header_text,
                                                self.reader_reservations],
                                      spacing=20,
                                      visible=False)

        self.view = ft.Container(content=
        ft.Column(
            controls=[dropdown_row, self.table_column, self.actions_and_isbn, self.borrow_result],
            spacing=40),
            padding=ft.padding.only(left=50, top=50))

        return self.view
