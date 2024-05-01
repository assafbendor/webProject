import os
import flet as ft
import requests

from client import client_config
from client.access_token import get_access_token


class SingleBook:

    def __init__(self, appLayout):
        super().__init__()
        self.appLayout = appLayout

    def get_book(self, isbn):

        path = "/search_books"
        params = {
            "isbn": isbn
        }
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f"Bearer {get_access_token()}"
        }
        try:
            r = requests.get(client_config.SERVER_URL + path, headers=headers, params=params)
            # Parse the response JSON data
            r.raise_for_status()
            book = r.json()
            return book
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")

        except Exception as err:
            print("Failed to make the GET request ", client_config.SERVER_URL + path, ". Error : ", err)

    def build(self, isbn):
        book = self.get_book(isbn)[0]

        image_card = ft.Card(
            elevation=2,
            margin=2,
            shape=ft.ContinuousRectangleBorder.radius,
            content=ft.Container(
                content=ft.Image(
                    src=os.path.join(os.getcwd(), "img", book['cover_image_filename']),
                ),
                padding=10,
                margin=10,
            ),
        )
        title = ft.Text(book['title'], font_family="Calibiri", size=36, color=ft.colors.BLUE_400)
        author = ft.Text(book['author']['name'], font_family="Calibiri", size=24, color=ft.colors.BLUE_600)

        title_column = ft.Column(controls=[title, author],
                                 alignment=ft.alignment.center,
                                 horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                 spacing=30)

        language = ft.Text("Language:" + book['language'], size=20)
        pages = ft.Text(str(book['pages']) + " pages", size=30)

        summary = ft.Text(book['description'],
                          color=ft.colors.WHITE54,
                          size=18,
                          italic=True,
                          font_family="Chalkboard")

        summary_container = ft.Container(content=summary, margin=15, padding=30)

        stars_row = self.get_stars(book)

        title_row = ft.Row(controls=[title_column, image_card],
                           alignment=ft.alignment.center,
                           vertical_alignment=ft.CrossAxisAlignment.CENTER,
                           spacing=50
                           )

        column = ft.Column(controls=[title_row, language, pages, summary_container, stars_row],
                           alignment=ft.alignment.center,
                           horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                           spacing=20)

        return column

    def get_stars(self, book):
        full_stars = int(book['average_rating'])
        half_star = book['average_rating'] - full_stars > 0.4
        stars = []
        for i in range(full_stars):
            stars.append(ft.Icon(name=ft.icons.STAR, color=ft.colors.YELLOW))
        if half_star:
            stars.append(ft.Icon(name=ft.icons.STAR_HALF, color=ft.colors.YELLOW))

        rating_row = ft.Row(controls=stars, spacing=2)
        return rating_row
