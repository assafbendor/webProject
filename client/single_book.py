import os

import flet as ft

from client import client_config


class SingleBook:

    def __init__(self, page):
        super().__init__()
        self.page = page

        self.book_details_dlg = ft.AlertDialog(
            modal=True,
            content=ft.Column(controls=[ft.Text("b! ")]),
            actions=[
                ft.TextButton("OK", on_click=self.close_book_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
        )

    def close_book_dlg(self, e):
        self.book_details_dlg.open = False
        self.page.update()

    def open_book_dlg(self, e):
        self.book_details_dlg.content.controls = self.build(e.data).controls
        self.page.dialog = self.book_details_dlg
        self.book_details_dlg.open = True
        self.page.update()

    def build(self, book):
        image_card = ft.Card(
            elevation=2,
            margin=2,
            shape=ft.ContinuousRectangleBorder.radius,
            content=ft.Container(
                content=ft.Image(
                    src=f"{client_config.SERVER_URL}/photos/{book['cover_image_filename']}"),
                padding=10,
                margin=10,
            ),
        )
        title = ft.Text(book['title'], size=36, color=ft.colors.BLUE_400)
        author = ft.Text(book['author']['name'], size=24, color=ft.colors.BLUE_600)

        title_column = ft.Column(controls=[title, author],
                                 alignment=ft.alignment.center,
                                 horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                 spacing=30)

        language = ft.Text("Language:" + book['language'], size=20)
        pages = ft.Text(str(book['pages']) + " pages", size=20)

        summary = ft.Text(book['description'],
                          color=ft.colors.WHITE54,
                          size=20,
                          italic=True)

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
