import os

import flet as ft

from client import client_config


class Logo(ft.UserControl):

    def __init__(self, page):
        super().__init__()
        self.view = None
        self.page = page

    def build(self):
        logo = ft.Image(
            src=f"{client_config.SERVER_URL}/photos/logo.png",
            expand=True
        )

        text = ft.Text("Book for You",
                       size=50,
                       text_align=ft.TextAlign.CENTER,
                       expand_loose=True)

        column = ft.Column([logo, text],
                           alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                           horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        logo_container = ft.Container(
            content=column,
            alignment=ft.alignment.center,
            expand=True)

        self.view = ft.Container(
            content=ft.Row(
                controls=[logo_container]),
            expand=True,
            padding=100
        )
        # padding = ft.padding.only(top=10, right=0),)
        # height = self.appLayout.page.height)
        return self.view
