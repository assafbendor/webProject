import flet as ft
import requests
from flet_core import icons

import client_config
from client.my_books import MyBooks


class ManageBooks:

    def __init__(self, page):
        super().__init__()

        self.go_icon = None
        self.page = page

        self.book_isbn_input = ft.TextField(
            label="ISBN",
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

        self.title_input = ft.TextField(
            label="Title",
            focused_color=ft.colors.BLACK87,
            color=ft.colors.BLACK87,
            bgcolor=ft.colors.WHITE,
            border_color=ft.colors.BLACK54,
            focused_border_color=ft.colors.BLACK,
            height=40,
            width=300,
            border_radius=15,
            content_padding=ft.padding.only(top=2, bottom=2, left=6),
            cursor_height=14,
            cursor_color=ft.colors.BLACK54)

        self.language_input = ft.TextField(
            label="Language",
            focused_color=ft.colors.BLACK87,
            color=ft.colors.BLACK87,
            bgcolor=ft.colors.WHITE,
            border_color=ft.colors.BLACK54,
            focused_border_color=ft.colors.BLACK,
            height=40,
            width=300,
            border_radius=15,
            content_padding=ft.padding.only(top=2, bottom=2, left=6),
            cursor_height=14,
            cursor_color=ft.colors.BLACK54)

        self.rating_input = ft.TextField(
            label="Rating",
            focused_color=ft.colors.BLACK87,
            color=ft.colors.BLACK87,
            bgcolor=ft.colors.WHITE,
            border_color=ft.colors.BLACK54,
            focused_border_color=ft.colors.BLACK,
            height=40,
            width=100,
            border_radius=15,
            content_padding=ft.padding.only(top=2, bottom=2, left=6),
            cursor_height=14,
            cursor_color=ft.colors.BLACK54)

        self.description = ft.TextField(
            label="Description",
            focused_color=ft.colors.BLACK87,
            color=ft.colors.BLACK87,
            bgcolor=ft.colors.WHITE,
            border_color=ft.colors.BLACK54,
            focused_border_color=ft.colors.BLACK,
            height=40,
            width=300,
            border_radius=15,
            content_padding=ft.padding.only(top=2, bottom=2, left=6),
            cursor_height=14,
            cursor_color=ft.colors.BLACK54)

        # cover_image_filename = Column(String, nullable=True) TODO

        self.pages_input = ft.TextField(
            label="Number of Pages",
            focused_color=ft.colors.BLACK87,
            color=ft.colors.BLACK87,
            bgcolor=ft.colors.WHITE,
            border_color=ft.colors.BLACK54,
            focused_border_color=ft.colors.BLACK,
            height=40,
            width=300,
            border_radius=15,
            content_padding=ft.padding.only(top=2, bottom=2, left=6),
            cursor_height=14,
            cursor_color=ft.colors.BLACK54)

        self.author_input = ft.TextField(
            label="Author",
            focused_color=ft.colors.BLACK87,
            color=ft.colors.BLACK87,
            bgcolor=ft.colors.WHITE,
            border_color=ft.colors.BLACK54,
            focused_border_color=ft.colors.BLACK,
            height=40,
            width=300,
            border_radius=15,
            content_padding=ft.padding.only(top=2, bottom=2, left=6),
            cursor_height=14,
            cursor_color=ft.colors.BLACK54)

        self.copies_input = ft.TextField(
            label="Number of Copies",
            focused_color=ft.colors.BLACK87,
            color=ft.colors.BLACK87,
            bgcolor=ft.colors.WHITE,
            border_color=ft.colors.BLACK54,
            focused_border_color=ft.colors.BLACK,
            height=40,
            width=300,
            border_radius=15,
            content_padding=ft.padding.only(top=2, bottom=2, left=6),
            cursor_height=14,
            cursor_color=ft.colors.BLACK54)

        apply = ft.TextButton(content=ft.Text("Apply"),
                              style=ft.ButtonStyle(color=ft.colors.BLACK87,
                                                   bgcolor=ft.colors.GREEN,
                                                   shape=ft.RoundedRectangleBorder(radius=10)),
                              on_click=self.add_or_edit())

        self.book_info = ft.Column(
            controls=[self.title_input,
                      self.language_input,
                      self.rating_input,
                      self.description,
                      self.pages_input,
                      self.author_input,
                      self.copies_input,
                      apply],

            alignment=ft.alignment.center,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        self.book_info_container = ft.Container(content=self.book_info,
                                                bgcolor=ft.colors.BLACK54,
                                                padding=ft.padding.all(50),
                                                visible=False)

    def get_book(self, e):

        path = "/search_books"

        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f"Bearer {self.page.client_storage.get('token')}"
        }

        params = {
            'isbn': self.book_isbn_input.value,
        }

        try:
            r = requests.get(client_config.SERVER_URL + path, params=params, headers=headers)
            r.raise_for_status()
            book_list = r.json()
            if len(book_list) > 1:
                print("Unexpected result")
            else:
                if len(book_list) == 0:
                    self.add_new_book(isbn=self.book_isbn_input.value)
                else:
                    self.edit_book(book_list[0])
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print("Failed to make the get request: ", client_config.SERVER_URL + path, " Error: ", err)
        self.page.update()

    def add_or_edit(self):
        pass

    def add_new_book(self, isbn):
        self.book_info_container.visible = True
        self.page.update()

    def edit_book(self, isbn):
        self.book_info_container.visible = True
        self.page.update()


    def build(self):

        book_text = ft.Text("Book ISBN :")

        self.go_icon = ft.IconButton(icon=icons.DOUBLE_ARROW,
                                     icon_color=ft.colors.GREEN,
                                     on_click=self.get_book)

        isbn_row = ft.Row(
            controls=[book_text, self.book_isbn_input, self.go_icon],
            spacing=10,
            alignment=ft.alignment.center)

        view = ft.Container(content=
                            ft.Column(controls=[isbn_row, self.book_info_container], spacing=50),
                            padding=ft.padding.only(left=50, top=50),
                            alignment=ft.alignment.center,
                            )

        return view
