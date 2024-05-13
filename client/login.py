import flet as ft
import requests

import client_config
from components import Logo


class Login:

    def __init__(self, page):
        super().__init__()
        self.token = None
        self.username_text = ft.TextField(label="Username",
                                          focused_color=ft.colors.BLACK87,
                                          color=ft.colors.BLACK87,
                                          bgcolor=ft.colors.WHITE,
                                          border_color=ft.colors.BLACK54,
                                          focused_border_color=ft.colors.BLACK,
                                          height=40,
                                          border_radius=15,
                                          content_padding=ft.padding.only(top=2, bottom=2, left=6),
                                          cursor_height=14,
                                          cursor_color=ft.colors.BLACK54)
        self.password_text = ft.TextField(label="Password",
                                          password=True,
                                          color=ft.colors.BLACK87,
                                          can_reveal_password=True,
                                          bgcolor=ft.colors.WHITE,
                                          focused_color=ft.colors.BLACK87,
                                          border_radius=15,
                                          border_color=ft.colors.BLACK54,
                                          focused_border_color=ft.colors.BLACK,
                                          height=40,
                                          content_padding=ft.padding.only(top=2, bottom=2, left=6),
                                          cursor_height=14,
                                          cursor_color=ft.colors.BLACK54)
        self.view = None
        self.login_error = ft.TextButton(
            visible=False,
            content=ft.Container(
                content=ft.Text("The username or password is incorrect", color=ft.colors.WHITE, size=15),
                bgcolor=ft.colors.RED,
                padding=ft.padding.all(10),
            )
        )

        self.page = page

    def get_token(self):
        return self.token

    def login_clicked(self, e):
        path = "/token"

        username = self.username_text.value
        password = self.password_text.value

        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = {
            'username': username,
            'password': password,
        }

        try:
            r = requests.post(client_config.SERVER_URL + path, headers=headers, data=data)
            # Parse the response JSON data
            r.raise_for_status()
            response_data = r.json()
            # Extract the "token" key from the response body
            token = response_data.get("access_token")
            if token:
                self.page.client_storage.set("token", token)
                self.page.client_storage.set("username", username)
                self.page.go("/search_book")
            else:
                print("Token not found in the response body.")
                self.login_error.visible = True
                self.page.update()
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            self.login_error.visible = True
            self.page.update()
        except Exception as err:
            print("Failed to make the POST request. Status code:", r.status_code, " Error: ", err)
            self.login_error.visible = True
            self.page.update()

    def sign_up_clicked(self, e):
        self.page.go("/signup")

    def build(self):
        forgot_password = ft.Text("Forgot password?",
                                  color="#34aeed",
                                  size=12,
                                  visible=False,  # TODO: implement
                                  style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE,
                                                     decoration_color="#34aeed"))

        password_block = ft.Column([self.password_text, forgot_password],
                                   horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        details = ft.Column([self.username_text, password_block])

        login_button = ft.ElevatedButton(text="LOG IN",
                                         on_click=self.login_clicked,
                                         icon=ft.icons.LOGIN_ROUNDED)

        no_account = ft.Text("Don't have an account?",
                             color=ft.colors.WHITE,
                             size=18)

        sign_up = ft.TextButton("Sign Up",
                                icon=ft.icons.APP_REGISTRATION_ROUNDED,
                                on_click=self.sign_up_clicked)

        no_account_block = ft.Column(controls=[no_account, sign_up],
                                     alignment=ft.alignment.center,
                                     horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                     expand=False)

        login_block = ft.Column(controls=[details, login_button, no_account_block, self.login_error],
                                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        login_container = ft.Container(
            content=login_block,
            alignment=ft.alignment.center,
            padding=100,
            expand=True
        )

        logo = Logo(self.page)
        self.view = ft.Row(
            controls=[logo.build(), login_container],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )

        return self.view
