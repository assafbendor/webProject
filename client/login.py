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

        self.reset_password_dialog = ft.AlertDialog(
            title=ft.Text("Reset Password "),
            modal=True,
            content=ft.Column(controls=[
                ft.Column(controls=[ft.TextField(label="Email",
                                                 focused_color=ft.colors.BLACK87,
                                                 color=ft.colors.BLACK87,
                                                 bgcolor=ft.colors.WHITE,
                                                 border_color=ft.colors.BLACK54,
                                                 focused_border_color=ft.colors.BLACK,
                                                 height=40,
                                                 border_radius=15,
                                                 content_padding=ft.padding.only(top=2, bottom=2, left=6),
                                                 cursor_height=14,
                                                 width=300,
                                                 cursor_color=ft.colors.BLACK54),
                                    ft.TextButton("Send email", on_click=self.show_code_and_new_password)]),
                ft.Column(
                    visible=False,
                    controls=
                    [ft.TextField(label="Code",
                                  focused_color=ft.colors.BLACK87,
                                  color=ft.colors.BLACK87,
                                  bgcolor=ft.colors.WHITE,
                                  border_color=ft.colors.BLACK54,
                                  focused_border_color=ft.colors.BLACK,
                                  height=40,
                                  border_radius=15,
                                  content_padding=ft.padding.only(top=2, bottom=2, left=6),
                                  cursor_height=14,
                                  cursor_color=ft.colors.BLACK54),
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
                                  )]),
                ft.TextButton(
                    visible=False,
                    content=ft.Container(
                        content=ft.Text("The username or password is incorrect", color=ft.colors.WHITE, size=15),
                        bgcolor=ft.colors.RED,
                        padding=ft.padding.all(10),
                    )
                )
            ]),
            actions=[
                ft.TextButton("OK", on_click=self.password_reset, disabled=True),
                ft.TextButton("Cancel", on_click=self.close_password_reset_dialog),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
            elevation=10,
        )

    def close_password_reset_dialog(self, e):
        self.reset_password_dialog.content.controls[2].visible = True
        self.reset_password_dialog.open = False
        self.page.update()

    def password_reset(self, e):
        global response_data
        path = "/verify_code"

        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }

        params = {
            'code': self.reset_password_dialog.content.controls[1].controls[0].value,
            'email': self.reset_password_dialog.content.controls[0].controls[0].value,
        }

        data = {
            "new_password": self.reset_password_dialog.content.controls[1].controls[1].value,
            "new_password_verify": self.reset_password_dialog.content.controls[1].controls[2].value
        }

        try:
            r = requests.post(client_config.SERVER_URL + path, params=params, headers=headers, json=data)
            # Parse the response JSON data
            response_data = r.json()
            r.raise_for_status()
            # Extract the "token" key from the response body
            token = response_data.get("access_token")
            username = response_data.get("username")
            if token:
                self.page.client_storage.set("token", token)
                self.page.client_storage.set("username", username)
                self.reset_password_dialog.open = False

                if response_data.get("is_admin"):
                    self.page.go("/manage_loans")
                else:
                    self.page.go("/search_book")
            else:
                print("Token not found in the response body.")
                self.login_error.visible = True
                self.page.update()
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            if response_data is not None:
                self.reset_password_dialog.content.controls[2].content.content.value = response_data.get("detail")
                self.reset_password_dialog.content.controls[2].visible = True
                self.page.update()
        except Exception as err:
            print("Failed to make the POST request. Status code:", r.status_code, " Error: ", err)
            self.reset_password_dialog.content.controls[2].content.content.value = response_data.get("detail")
            self.reset_password_dialog.content.controls[2].visible = True
            self.page.update()
        self.page.update()

    def show_code_and_new_password(self, e):

        global response_data_2

        path = "/forgot_password"

        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        params = {
            'email': self.reset_password_dialog.content.controls[0].controls[0].value
        }

        try:
            r = requests.post(client_config.SERVER_URL + path, params=params, headers=headers)
            # Parse the response JSON data
            response_data_2 = r.json()
            r.raise_for_status()
            self.reset_password_dialog.content.controls[2].visible = False
            self.reset_password_dialog.content.controls[1].visible = True
            self.reset_password_dialog.actions[0].disabled = False
            self.page.update()

        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            self.reset_password_dialog.content.controls[2].content.content.value = response_data_2.get("detail")
            self.reset_password_dialog.content.controls[2].visible = True
            self.page.update()
        except Exception as err:
            print("Failed to make the POST request. Status code:", r.status_code, " Error: ", err)
            self.reset_password_dialog.content.controls[2].content.content.value = response_data_2.get("detail")
            self.reset_password_dialog.content.controls[2].visible = True
            self.page.update()

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
                if response_data.get("is_admin"):
                    self.page.go("/manage_loans")
                else:
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

    def forgot_password_clicked(self, e):
        self.page.dialog = self.reset_password_dialog
        self.reset_password_dialog.open = True
        self.page.update()

    def build(self):
        forgot_password = ft.TextButton("Forgot password?",
                                        visible=True,
                                        style=ft.ButtonStyle(
                                            color=ft.colors.WHITE,
                                            overlay_color=ft.colors.TRANSPARENT),
                                        on_click=self.forgot_password_clicked
                                        )

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
