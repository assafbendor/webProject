import flet as ft
from flet import (
    AppBar,
    Icon,
    Page,
    Text,
    View,
    colors,
    theme,
)

from client.book_search import BookSearch
from client.login import Login
from client.sign_up import SignUp


def main(page: Page):
    page.title = "BookForYou"

    page.fonts = {
        "lato-light": "fonts/Lato/Lato-Light.ttf"
    }

    page.theme = theme.Theme(font_family="lato-light")

    page.bgcolor = "#083b7a"

    def route_change(e):
        appbar = AppBar(
            leading=Icon(ft.icons.MENU_BOOK),
            leading_width=75,
            title=Text(f"Book For You", size=32),
            center_title=False,
            toolbar_height=75,
            bgcolor=colors.LIGHT_BLUE_ACCENT_700,
            actions=[
                ft.TextButton("Your Books", ft.icons.BOOKMARKS_ROUNDED, on_click=lambda e: page.go("/my_books")),
                ft.TextButton("History", ft.icons.HISTORY, on_click=lambda e: page.go("/history")),
                ft.TextButton("Recommended", ft.icons.RECOMMEND, on_click=lambda e: page.go("/recommended")),
                ft.TextButton("Search", ft.icons.SEARCH, on_click=lambda e: page.go("/search_book")),
                ft.PopupMenuButton(content=ft.Container(
                    ft.Row(controls=[
                        ft.Icon(ft.icons.ACCOUNT_CIRCLE),
                        ft.Text(page.client_storage.get("username"))
                    ]),
                    padding=5
                ),
                    items=[
                        ft.PopupMenuItem(text="Profile"),
                        ft.PopupMenuItem(text="Logout"),
                    ]),
            ],
        )

        page.views.clear()

        page.views.append(
            View(
                controls=[ft.Container(content=ft.Text("Coming soon...", size=100), alignment=ft.alignment.center, expand=True)],
                bgcolor="#083b7a",
            )
        )

        if page.route == "/login":
            page.views.append(
                View(
                    controls=[Login(page).build()],
                    bgcolor="#083b7a",
                )
            )

        if page.route == "/signup":
            page.views.append(
                View(
                    controls=[SignUp(page).build()],
                    bgcolor="#083b7a",
                )
            )

        if page.route == "/search_book":
            page.views.append(
                View(
                    controls=[BookSearch(page).build()],
                    appbar=appbar
                )
            )

        page.update()

    page.on_route_change = route_change

    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_view_pop = view_pop

    page.go("/login")


ft.app(target=main, assets_dir="assets")
