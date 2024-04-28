import os
import flet as ft
import single_book

from client.single_book import SingleBook
from components import Logo
import requests
import client_config


class BookSearch:

    def __init__(self, appLayout):
        super().__init__()
        self.trending_books = []
        self.single_book = single_book.SingleBook(appLayout)
        self.appLayout = appLayout
        self.not_found_dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Oh oh! "),
            content=ft.Text("Looks like we didn't find what you are looking for... "),
            actions=[
                ft.TextButton("OK", on_click=self.close_not_found_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
            elevation=10,
        )

        self.book_details_dlg = ft.AlertDialog(
            modal=True,
            content=ft.Column(controls=[ft.Text("b! ")]),
            actions=[
                ft.TextButton("OK", on_click=self.close_book_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

    def close_book_dlg(self, e):
        self.book_details_dlg.open = False
        self.appLayout.page.update()

    def open_book_dlg(self, isbn):
        self.book_details_dlg.content.controls = [self.single_book.build(isbn)]
        self.appLayout.page.dialog = self.book_details_dlg
        self.book_details_dlg.open = True
        self.appLayout.page.update()

    def close_not_found_dlg(self, e):
        self.not_found_dlg.open = False
        self.appLayout.page.update()

    def open_not_found_dialog(self, e):
        self.appLayout.page.dialog = self.not_found_dlg
        self.not_found_dlg.open = True
        self.appLayout.page.update()

    def search_clicked(self, e):
        global r
        path = "/search_books"

        inputs = {
            'isbn': self.ISBN.value,
            'title': self.title.value,
            'author_name': self.author.value,
            'language': self.language.value
        }
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f"Bearer {client_config.access_token}"
        }

        params = {key: value for key, value in inputs.items() if value != ''}

        try:
            r = requests.get(client_config.SERVER_URL + path, headers=headers, params=params)
            # Parse the response JSON data
            r.raise_for_status()
            books = r.json()
            self.appLayout.set_book_list_view(books)
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            if r is not None:
                if r.status_code == requests.codes.not_found:
                    self.open_not_found_dialog(e)

        except Exception as err:
            print("Failed to make the GET request ", client_config.SERVER_URL + path, ". Error : ", err)

    def slider_changed(self, e):
        self.selected_rating = {e.control.value}

    def build(self):

        self.page_title = ft.Text("Search For Any Book", theme_style=ft.TextThemeStyle.DISPLAY_LARGE)
        self.page_title_container = ft.Container(content=self.page_title, padding=ft.padding.only(bottom=20))

        self.author = ft.TextField(label="Author",
                                   border_color=ft.colors.BLACK54,
                                   focused_border_color=ft.colors.BLACK,
                                   width=self.appLayout.page.width / 2,
                                   focused_color=ft.colors.BLACK87)
        self.title = ft.TextField(label="Title",
                                  border_color=ft.colors.BLACK54,
                                  focused_border_color=ft.colors.BLACK,
                                  width=self.appLayout.page.width / 2,
                                  focused_color=ft.colors.BLACK87)
        self.ISBN = ft.TextField(label="ISBN",
                                 border_color=ft.colors.BLACK54,
                                 focused_border_color=ft.colors.BLACK,
                                 width=self.appLayout.page.width / 2,
                                 focused_color=ft.colors.BLACK87)
        self.language = ft.TextField(label="Language",
                                     border_color=ft.colors.BLACK54,
                                     focused_border_color=ft.colors.BLACK,
                                     width=self.appLayout.page.width / 2,
                                     focused_color=ft.colors.BLACK87)

        self.search = ft.ElevatedButton(text="SEARCH!",
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

        self.rating_text = ft.Text("Minimal Book Score")
        self.rating = ft.Slider(min=1, max=5, divisions=0.5, label="{value}", on_change=self.slider_changed)
        self.rating_row = ft.Row(controls=[self.rating_text, self.rating])

        self.inputs = ft.Column([self.author, self.title, self.ISBN, self.language, self.rating_row], spacing=5)

        self.inputs_container = ft.Container(content=self.inputs,
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

        self.inputs_and_search = ft.Column([self.page_title_container, self.inputs_container, self.search],
                                           spacing=20,
                                           alignment=ft.alignment.center,
                                           horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        self.inputs_and_search_container = ft.Container(content=self.inputs_and_search,
                                                        padding=ft.padding.only(top=50, left=250),
                                                        alignment=ft.alignment.center)

        self.trending_title = ft.Text("Trending Books", theme_style=ft.TextThemeStyle.DISPLAY_MEDIUM)
        self.trending_title_container = ft.Container(content=self.trending_title,
                                                     padding=ft.padding.only(top=20, bottom=50))

        # TODO: select top 5 books

        sample_books = []
        sample_books.append({"isbn": 9788681804186, "cover_image_filename": "War and Peace_Leo Tolstoy.jpg"})
        sample_books.append({"isbn": 9784599600049, "cover_image_filename": "The Great Gatsby_F. Scott Fitzgerald.jpg"})
        sample_books.append({"isbn": 9784154748027, "cover_image_filename": "Moby Dick_Herman Melville.jpg"})
        sample_books.append({"isbn": 9788949859198, "cover_image_filename": "Hamlet_William Shakespeare.jpg"})
        sample_books.append({"isbn": 9789913767779, "cover_image_filename": "1984_George Orwell.jpg"})

        paths=[]
        for i in range(5):
            paths.append([os.path.join(os.getcwd(), "img", sample_books[i]['cover_image_filename'])])

        for i in range(len(sample_books)):
            self.trending_books.append(ft.Container(
                content=ft.Image(
                    src=f"{paths[i]}",
                    width=self.appLayout.page.width / 6,  # Set the width of the image
                    height=self.appLayout.page.width / 4.5  # Set the height of the image
                ),
                on_click=self.open_book_dlg(isbn=sample_books[i]['isbn'])
            ))

        self.trending_row = ft.Row(controls=[self.trending_books[0], self.trending_books[1], self.trending_books[2], self.trending_books[3], self.trending_books[4]], spacing=40)
        self.trending_column = ft.Column(controls=[self.trending_title_container, self.trending_row])
        self.trending_container = ft.Container(content=self.trending_column, padding=ft.padding.only(top=30, left=250),
                                               alignment=ft.alignment.center)
        self.final_column = ft.Column(controls=[self.inputs_and_search_container, self.trending_container],
                                      alignment=ft.alignment.center)

        return self.final_column
