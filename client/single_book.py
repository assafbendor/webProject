import os
import flet as ft
import requests

from client import client_config


class SingleBook:

    def __init__(self, appLayout):
        super().__init__()
        self.appLayout = appLayout

    def get_book(self, isbn):

        path = "/search_books"

        params = isbn

        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f"Bearer {client_config.access_token}"
        }

        try:
            r = requests.get(client_config.SERVER_URL + path, headers=headers, params=params)
            # Parse the response JSON data
            r.raise_for_status()
            books = r.json()
            self.appLayout.set_book_list_view(books)
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")

        except Exception as err:
            print("Failed to make the GET request ", client_config.SERVER_URL + path, ". Error : ", err)


        # # TODO
        # return {
        #     "isbn": "9781094311166",
        #     "title": "Wuthering Heights",
        #     "author": "Emily Bronte",
        #     "language": "English",
        #     "rating": 0,
        #     "cover_image_filename": "Wuthering Heights_Emily Bront\u00c3\u00ab.jpg",
        #     "description": "Wuthering Heights is a moody 19th-century triumph, lauded for its dark imagery, austere setting, and depiction of fraught romance. Wuthering Heights is Emily Bronte\u2019s account of the tormented love story between orphan Heathcliff and the daughter of his benefactor, Catherine Earnshaw. Troubled, stark, and violent, Wuthering Heights was hugely controversial at its publication in 1847, but has since become a classic of English literature. This Essential Classics edition includes a new introduction by Professor Vivian Heller, Ph.D. in literature and modern studies from Yale University. Emily Bronte was an English novelist and poet, best known for her only novel, Wuthering Heights. Silent and reserved, Bronte wrote using the pen name Ellis Bell, and was one of the Bronte siblings. Vivian Heller received her Ph.D. in English Literature and Modern Studies from Yale University. She is author of Joyce, Decadence, and Emancipation(University of Illinois Press) and of The City Beneath Us (W.W. Norton & Company), a history of the building of the New York City subway system. She is an associate at Columbia\u2019s School of Professional Studies and is the writing tutor for the Center for Curatorial Studies at Bard College. She is also a long-standing member of the non-fiction committee of the PEN Prison-Writing Committee, which awards prizes to inmates from across the country. Essential Classics publishes the most crucial literary works throughout history, with a unique introduction to each, making them the perfect treasure for any reader\u2019s shelf.",
        #     "ratings_count": 0,
        #     "average_rating": 3.5,
        #     "pages": 143,
        # }

    def build(self, isbn):
        book = self.get_book(1)

        image_card = ft.Card(
            elevation=2,
            margin=2,
            shape=ft.ContinuousRectangleBorder.radius,
            content=ft.Container(
                content=ft.Image(
                    src=os.path.join(os.getcwd(), "img", book['cover_image_filename']),
                    height=self.appLayout.page.height / 4.5,
                    width=self.appLayout.page.height / 6
                ),
                padding=10,
                margin=10,

             ),
        )
        title = ft.Text(book['title'], font_family="Calibiri", size=36, color=ft.colors.BLUE_400)
        author = ft.Text(book['author'], font_family="Calibiri", size=24, color=ft.colors.BLUE_600)

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

        full_stars = int(book['average_rating'])
        half_star = book['average_rating'] - full_stars > 0.4
        stars = []
        for i in range(full_stars):
            stars.append(ft.Icon(name=ft.icons.STAR, color=ft.colors.YELLOW))

        if half_star:
            stars.append(ft.Icon(name=ft.icons.STAR_HALF, color=ft.colors.YELLOW))

        rating_row = ft.Row(controls=stars, spacing=2)

        title_row = ft.Row(controls=[title_column, image_card],
                           alignment=ft.alignment.center,
                           vertical_alignment=ft.CrossAxisAlignment.CENTER,
                           )

        column = ft.Column(controls=[title_row, language, pages, summary_container, rating_row],
                           alignment=ft.alignment.center,
                           horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                           spacing=20)

        return column
