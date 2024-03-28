import flet as ft
import requests

import components

server = 'http://127.0.0.1:8000'


class UserMain:

    def book_search_clicked(self):
        path = "/books"
        r = requests.get(server + path)
        return r.text

    def recommend_clicked():
        pass

    def my_books_clicked():
        pass

    def logout_clicked():
        pass    

    def main(page: ft.Page):

        username = "Shira"

        # Setting the background color of the page
        page.bgcolor = "#083b7a"
        page.padding = 50

        hello = str("Hello, " + username + "!" + '\n')
        hello_text = ft.Text(hello,
                            font_family="Calibiri",
                            theme_style=ft.TextThemeStyle.DISPLAY_LARGE)

        logo = components.Logo()

        column = ft.Column(controls=[hello_text, logo.build()])

        what_to_do = "What would you like to do today?"
        what_to_do_text = ft.Text(what_to_do,
                                font_family="Calibiri",
                                theme_style=ft.TextThemeStyle.DISPLAY_SMALL,
                                text_align=ft.TextAlign.CENTER)

        def on_action_hover(e):
            e.control.bgcolor = ft.colors.BLACK26 if e.data == "true" else ft.colors.BLACK54
            e.control.shadow.blur_radius = 15 if e.data == "true" else 5
            e.control.update()

        my_books_button = ft.Container(
            content=ft.Text("My Books", font_family="Calibiry", size=20),
            margin=30,
            padding=30,
            alignment=ft.alignment.center,
            bgcolor=ft.colors.BLACK54,
            border_radius=20,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=5,
                color=ft.colors.BLUE_GREY_300,
                offset=ft.Offset(0, 0),
                blur_style=ft.ShadowBlurStyle.OUTER),
            on_hover=on_action_hover,
            on_click=my_books_clicked)

        search_books_button = ft.Container(
            content=ft.Text("Book Search", font_family="Calibiry", size=20),
            margin=30,
            padding=30,
            alignment=ft.alignment.center,
            bgcolor=ft.colors.BLACK54,
            border_radius=20,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=5,
                color=ft.colors.BLUE_GREY_300,
                offset=ft.Offset(0, 0),
                blur_style=ft.ShadowBlurStyle.OUTER),
            on_hover=on_action_hover,
            on_click=book_search_clicked)

        recommend_button = ft.Container(
            content=ft.Text("Find me a book!", font_family="Calibiry", size=20),
            margin=30,
            padding=30,
            alignment=ft.alignment.center,
            bgcolor=ft.colors.BLACK54,
            border_radius=20,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=5,
                color=ft.colors.BLUE_GREY_300,
                offset=ft.Offset(0, 0),
                blur_style=ft.ShadowBlurStyle.OUTER),
            on_hover=on_action_hover,
            on_click=recommend_clicked)

        actions_row = ft.Row(controls=[my_books_button, search_books_button, recommend_button],
                            alignment=ft.alignment.center,
                            spacing=50)

        actions_column = ft.Column([what_to_do_text, actions_row], spacing=100)

        actions_container = ft.Container(actions_column, padding=150)

        page_row = ft.Row([column, actions_container])

        logout_button = ft.FloatingActionButton(
            icon=ft.icons.LOGOUT, on_click=logout_clicked, bgcolor=ft.colors.WHITE54, tooltip="logout")

 
