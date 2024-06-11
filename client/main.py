import flet as ft
import requests
from flet import (
    AppBar,
    Icon,
    Page,
    Text,
    View,
    colors,
    theme,
)

from client import client_config
from client.book_search import BookSearch
from client.history import History
from client.loan_books import LoanBooks
from client.login import Login
from client.my_books import MyBooks
from client.recommendations import Recommendations
# from client.recommendations import Recommendations
from client.sign_up import SignUp


def main(page: Page):
    page.title = "BookForYou"

    page.fonts = {
        "lato-light": "fonts/Lato/Lato-Light.ttf"
    }

    page.theme = theme.Theme(font_family="lato-light")

    page.bgcolor = "#083b7a"

    def close_dialog(e):
        change_password_dialog.content.controls[0].clean()
        change_password_dialog.content.controls[1].clean()
        change_password_dialog.open = False
        page.update()

    def change_password_clicked(e):
        path = "/change_password"

        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {page.client_storage.get('token')}"
        }

        data = {
            "new_password": change_password_dialog.content.controls[0].value,
            "new_password_verify": change_password_dialog.content.controls[1].value
        }

        try:
            r = requests.post(client_config.SERVER_URL + path, headers=headers, json=data)
            # Parse the response JSON data
            response_data = r.json()
            r.raise_for_status()
            # Extract the "token" key from the response body
            change_password_dialog.content.controls[0].clean()
            change_password_dialog.content.controls[1].clean()
            change_password_dialog.open = False
            page.update()

        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            if response_data is not None:
                change_password_dialog.content.controls[2].content.content.value = response_data.get("detail")
                change_password_dialog.content.controls[2].visible = True
                page.update()
        except Exception as err:
            print("Failed to make the POST request. Status code:", r.status_code, " Error: ", err)
            change_password_dialog.content.controls[2].content.content.value = response_data.get("detail")
            change_password_dialog.content.controls[2].visible = True
            page.update()

        page.update()

    change_password_dialog = ft.AlertDialog(
        title=ft.Text("Change Password "),
        modal=True,
        content=ft.Column(controls=[
            ft.TextField(label="New Password",
                         password=True,
                         can_reveal_password=True,
                         bgcolor=ft.colors.WHITE,
                         color=ft.colors.BLACK87,
                         focused_color=ft.colors.BLACK87,
                         border_color=ft.colors.BLACK54,
                         focused_border_color=ft.colors.BLACK,
                         border_radius=15,
                         height=40,
                         content_padding=ft.padding.only(top=2, bottom=2, left=6),
                         cursor_height=14,
                         cursor_color=ft.colors.BLACK54
                         ),
            ft.TextField(label="Verify New Password",
                         password=True,
                         can_reveal_password=True,
                         bgcolor=ft.colors.WHITE,
                         color=ft.colors.BLACK87,
                         focused_color=ft.colors.BLACK87,
                         border_color=ft.colors.BLACK54,
                         focused_border_color=ft.colors.BLACK,
                         border_radius=15,
                         height=40,
                         content_padding=ft.padding.only(top=2, bottom=2, left=6),
                         cursor_height=14,
                         cursor_color=ft.colors.BLACK54
                         ),
            ft.TextButton(
                visible=False,
                content=ft.Container(
                    content=ft.Text("The username or password is incorrect", color=ft.colors.WHITE, size=15),
                    bgcolor=ft.colors.RED,
                    padding=ft.padding.all(10),
                ))
        ]),
        actions=[
            ft.TextButton("OK", on_click=change_password_clicked),
            ft.TextButton("Cancel", on_click=close_dialog)
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
        elevation=10)

    def show_change_password_dialog(e):
        page.dialog = change_password_dialog
        change_password_dialog.open = True
        page.update()

    def do_logout(e):
        page.client_storage.remove("token")
        page.client_storage.remove("username")
        page.go("/login")

    def route_change(e):
        reader_appbar = AppBar(
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
                        ft.PopupMenuItem(text="Change Password", on_click=show_change_password_dialog),
                        ft.PopupMenuItem(text="Logout", on_click=do_logout),
                    ],
                    tooltip=None),
            ],
        )

        admin_appbar = AppBar(
            leading=Icon(ft.icons.MENU_BOOK),
            leading_width=75,
            title=Text(f"Book For You - ADMIN ", size=32),
            center_title=False,
            toolbar_height=75,
            bgcolor=colors.CYAN_ACCENT_700,
            actions=[
                ft.TextButton("Manage Loans", ft.icons.ASSIGNMENT_ADD, on_click=lambda e: page.go("/loan_books")),
                ft.TextButton("Manage Books", ft.icons.LIBRARY_ADD, on_click=lambda e: page.go("/add_book")),
                ft.PopupMenuButton(content=ft.Container(
                    ft.Row(controls=[
                        ft.Icon(ft.icons.ACCOUNT_CIRCLE),
                        ft.Text(page.client_storage.get("username"))
                    ]),
                    padding=5
                ),
                    items=[
                        ft.PopupMenuItem(text="Change Password", on_click=show_change_password_dialog),
                        ft.PopupMenuItem(text="Logout", on_click=do_logout),
                    ], tooltip=None),

            ],
        )

        page.views.clear()

        # reader routes

        page.views.append(
            View(
                controls=[ft.Container(content=ft.Text("Coming soon...", size=100), alignment=ft.alignment.center,
                                       expand=True)],
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
                    appbar=reader_appbar
                )
            )

        if page.route == "/my_books":
            page.views.append(
                View(
                    controls=[MyBooks(page).build()],
                    appbar=reader_appbar
                )
            )

        if page.route == "/history":
            page.views.append(
                View(
                    controls=[History(page).build()],
                    appbar=reader_appbar
                )
            )

        if page.route == "/recommended":
            page.views.append(
                View(
                    controls=[Recommendations(page).build()],
                    appbar=reader_appbar
                )
            )

        # admin routes

        if page.route == "/manage_loans":
            page.views.append(
                View(
                    controls=[LoanBooks(page).build()],
                    appbar=admin_appbar
                )
            )

        if page.route == "/manage_books":
            page.views.append(
                View(
                    controls=[BookSearch(page).build()],
                    appbar=admin_appbar
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
