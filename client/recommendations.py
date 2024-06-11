import os

import flet as ft
import requests

import client_config


class Recommendations:

    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

    def get_recommended_books(self):
        path = "/user_recommendation"
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
        except Exception as err:
            print("Failed to make the GET request ", client_config.SERVER_URL + path, ". Error : ", err)

    def build(self):

        page_title = ft.Text("Based on your past borrows, we can recommend the following books:",
                             color=ft.colors.LIGHT_BLUE_200)
        page_title_container = ft.Container(content=page_title, padding=ft.padding.only(bottom=20))

        recommended_books = self.get_recommended_books()
        recommended_books_controls = []

        for book in recommended_books:
            image_col = ft.Row(controls=[
                ft.Card(
                    elevation=2,
                    margin=2,
                    shape=ft.ContinuousRectangleBorder.radius,
                    content=ft.Container(
                        content=ft.Image(
                            src=f"{client_config.SERVER_URL}/photos/{book['cover_image_filename']}",
                        ),
                        padding=5,
                        margin=5,
                    ),
                ),
                ft.Card(content=ft.Text(book['description'], no_wrap=False, width=self.page.width/2), margin=5)
            ],
                alignment=ft.alignment.center,
                vertical_alignment=ft.CrossAxisAlignment.CENTER)

            recommended_books_controls.append(ft.Container(
                content=image_col,
            ))

        recommended_books_col = ft.Column(
            controls=[
                recommended_books_controls[0],
                recommended_books_controls[1],
                recommended_books_controls[2],
                recommended_books_controls[3],
                recommended_books_controls[4]],
            spacing=50,
            alignment=ft.MainAxisAlignment.SPACE_EVENLY)

        trending_column = ft.Column(controls=[page_title_container, recommended_books_col])
        return trending_column
