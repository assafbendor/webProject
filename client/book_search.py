import os

import flet as ft
import requests

import client_config
import single_book
from client.book_list import BookList


class BookSearch:

    def __init__(self, page: ft.Page):
        super().__init__()
        # self.language = ft.TextField(label="Language",
        #                              border_color=ft.colors.BLACK54,
        #                              focused_border_color=ft.colors.BLACK,
        #                              width=appLayout.page.width / 2,
        #                              focused_color=ft.colors.BLACK87)
        # self.ISBN = ft.TextField(label="ISBN",
        #                          border_color=ft.colors.BLACK54,
        #                          focused_border_color=ft.colors.BLACK,
        #                          width=appLayout.page.width / 2,
        #                          focused_color=ft.colors.BLACK87)
        # self.title = ft.TextField(label="Title",
        #                           border_color=ft.colors.BLACK54,
        #                           focused_border_color=ft.colors.BLACK,
        #                           width=appLayout.page.width / 2,
        #                           focused_color=ft.colors.BLACK87)
        # self.author = ft.TextField(label="Author",
        #                            border_color=ft.colors.BLACK54,
        #                            focused_border_color=ft.colors.BLACK,
        #                            width=appLayout.page.width / 2,
        #                            focused_color=ft.colors.BLACK87)

        self.query_str = ft.TextField(label="Query",
                                      border_color=ft.colors.BLACK54,
                                      focused_border_color=ft.colors.BLACK,
                                      width=page.width / 2,
                                      focused_color=ft.colors.BLACK87)
        self.trending_row = None
        self.trending_books = []
        self.single_book = single_book.SingleBook(page)
        self.page = page
        self.not_found_dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Oh oh! "),
            content=ft.Text("Looks like we didn't find what you are looking for... "),
            actions=[
                ft.TextButton("OK", on_click=self.close_not_found_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
            elevation=10,
        )

    def close_not_found_dlg(self, e):
        self.not_found_dlg.open = False
        self.page.update()

    def open_not_found_dialog(self):
        self.page.dialog = self.not_found_dlg
        self.not_found_dlg.open = True
        self.page.update()

    def search_clicked(self, e):

        path = "/search_books_by_anything"
        # inputs = {
        #     'isbn': self.ISBN.value,
        #     'title': self.title.value,
        #     'author_name': self.author.value,
        #     'language': self.language.value
        # }

        inputs = {
            "query_str": self.query_str.value
        }
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f"Bearer {self.page.client_storage.get('token')}"
        }
        params = {key: value for key, value in inputs.items() if value != ''}

        try:
            r = requests.get(client_config.SERVER_URL + path, headers=headers, params=params)
            r.raise_for_status()
            books = r.json()
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            if r is not None:
                if r.status_code == requests.codes.not_found:
                    self.open_not_found_dialog()
        else:
            self.page.views.append(ft.View(
                # f"/search_book?query={self.query_str.value}",
                controls=[BookList(self.page).build(books)],
                appbar=self.page.appbar
            ))

            self.page.update()

    def get_trending_books(self):
        path = "/highest_rating_books"
        params = {
            'number_of_books': 5,
        }
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f"Bearer {self.page.client_storage.get('token')}"
        }

        try:
            r = requests.get(client_config.SERVER_URL + path, headers=headers, params=params)
            r.raise_for_status()
            books = r.json()
            return books
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            if r is not None:
                if r.status_code == requests.codes.not_found:
                    self.open_not_found_dialog()
        except Exception as err:
            print("Failed to make the GET request ", client_config.SERVER_URL + path, ". Error : ", err)

    def slider_changed(self, e):
        self.selected_rating = {e.control.value}

    def build(self):

        page_title = ft.Text("Search For Any Book", theme_style=ft.TextThemeStyle.DISPLAY_LARGE)
        page_title_container = ft.Container(content=page_title, padding=ft.padding.only(bottom=20))

        search = ft.ElevatedButton(text="SEARCH!",
                                   icon=ft.icons.SEARCH_OUTLINED,
                                   on_click=self.search_clicked,
                                   bgcolor=ft.colors.WHITE54,
                                   color=ft.colors.BLACK87,
                                   height=47,
                                   elevation=10,
                                   style=ft.ButtonStyle(
                                       shape=ft.RoundedRectangleBorder(radius=5),
                                       color={
                                           ft.MaterialState.HOVERED: ft.colors.LIGHT_BLUE_200,
                                           ft.MaterialState.DEFAULT: ft.colors.WHITE54,
                                           ft.MaterialState.FOCUSED: ft.colors.LIGHT_BLUE_200}
                                   ))

        rating_text = ft.Text("Minimal Book Score")
        rating = ft.Slider(min=1, max=5, divisions=0.5, label="{value}", on_change=self.slider_changed)
        rating_row = ft.Row(controls=[rating_text, rating])

        # inputs = ft.Column([self.author, self.title, self.ISBN, self.language, rating_row], spacing=5)
        inputs = ft.Column([self.query_str], spacing=5)
        inputs_container = ft.Container(content=inputs,
                                        bgcolor=ft.colors.WHITE,
                                        padding=ft.padding.all(20),
                                        border=ft.border.all(1, ft.colors.BLACK),
                                        border_radius=ft.border_radius.all(20),
                                        shadow=ft.BoxShadow(
                                            spread_radius=1,
                                            blur_radius=15,
                                            color=ft.colors.BLUE_GREY_300,
                                            offset=ft.Offset(0, 0),
                                            blur_style=ft.ShadowBlurStyle.OUTER, ))

        inputs_and_search = ft.Column([page_title_container, inputs_container, search],
                                      spacing=20,
                                      alignment=ft.alignment.center,
                                      horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        inputs_and_search_container = ft.Container(content=inputs_and_search,
                                                   padding=ft.padding.only(top=50),
                                                   alignment=ft.alignment.center)

        trending_title = ft.Text("Trending Books", theme_style=ft.TextThemeStyle.DISPLAY_MEDIUM)
        trending_title_container = ft.Container(content=trending_title,
                                                padding=ft.padding.only(bottom=10))

        self.trending_books = self.get_trending_books()
        trending_books_controls = []

        paths = []
        for i in range(5):
            paths.append(os.path.join(os.getcwd(), "img", self.trending_books[i]['cover_image_filename']))

        for i in range(len(self.trending_books)):
            image_col = ft.Column(controls=[
                ft.Card(
                    elevation=2,
                    margin=2,
                    shape=ft.ContinuousRectangleBorder.radius,
                    content=ft.Container(
                        content=ft.Image(
                            src=f"{paths[i]}",
                        ),
                        padding=5,
                        margin=5,
                    ),
                ),
                self.single_book.get_stars(self.trending_books[i])],
                alignment=ft.alignment.center,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER)

            def get_on_click(book):
                return lambda e: self.single_book.open_book_dlg(e=ft.ControlEvent(
                    control=None,
                    name="Trending Book Clicked",
                    page=self.page,
                    data=book,
                    target=''))

            trending_books_controls.append(ft.Container(
                content=image_col,
                on_click=get_on_click(self.trending_books[i])
                # on_click=self.single_book.open_book_dlg
            ))

        trending_row = ft.Row(
            controls=[
                trending_books_controls[0],
                trending_books_controls[1],
                trending_books_controls[2],
                trending_books_controls[3],
                trending_books_controls[4]],
            spacing=50)

        trending_column = ft.Column(controls=[trending_title_container, trending_row])
        trending_container = ft.Container(content=trending_column,
                                          alignment=ft.alignment.center)
        final_column = ft.Column(controls=[inputs_and_search_container, trending_container],
                                 spacing=50,
                                 alignment=ft.alignment.center,
                                 horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        return final_column
