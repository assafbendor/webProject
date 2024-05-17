import flet as ft
import requests

import client_config
from client.my_books import MyBooks


class LoanBooks:

    def __init__(self, page):
        super().__init__()
        self.view = None
        self.readers_dropdown = None
        self.page = page
        self.my_books = MyBooks(self.page)

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
                                        cursor_color=ft.colors.BLACK54)

        self.loan_book_button = ft.ElevatedButton(text="Borrow Book",
                                                  on_click=self.borrow_clicked)

        self.loan_row = ft.Row(controls=[self.borrow_isbn, self.loan_book_button], visible=False)

        self.borrow_result = ft.TextButton(
            visible=False,
            content=ft.Container(
                content=ft.Text("Book Borrowed Successfully!", color=ft.colors.WHITE, size=15),
                bgcolor=ft.colors.GREEN,
                padding=ft.padding.all(10),
            )

        )

        self.reader_books = ft.Container()

    def borrow_clicked(self, e):
        self.borrow_result.visible = False

        path = "/borrow_book"

        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f"Bearer {self.page.client_storage.get('token')}"
        }

        params = {
            'book_isbn': self.borrow_isbn.value
        }

        try:
            r = requests.post(client_config.SERVER_URL + path, params=params, headers=headers)
            r.raise_for_status()
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
        selected_reader = self.readers_dropdown.value
        self.reader_books.content = self.my_books.get_user_books_table(selected_reader)
        self.loan_row.visible = True
        self.page.update()
        print(selected_reader)

    def build(self):
        readers = self.get_readers()
        dropdown_text = ft.Text("Select Reader:")
        self.readers_dropdown = ft.Dropdown(
            on_change=self.reader_selected,
            options=[ft.dropdown.Option(reader['username']) for reader in readers],
        )

        dropdown_row = ft.Row(controls=[dropdown_text, self.readers_dropdown])

        self.view = ft.Column(controls=[dropdown_row, self.reader_books, self.loan_row, self.borrow_result])

        return self.view
