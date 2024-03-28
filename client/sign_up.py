import flet as ft

import components

class SignUp(ft.UserControl):

    def __init__(self, appLayout):
        super().__init__()
        self.appLayout = appLayout

    def sign_up_clicked(self, e):
        print("Sign Up!")
 
    def login_clicked(self, e):
        self.appLayout.page.route = "/login"
        self.appLayout.page.update()


    def build(self):

        username_text = ft.TextField(label="Username",
                                    focused_color=ft.colors.BLACK87,
                                    bgcolor=ft.colors.WHITE,
                                    height=40,
                                    border_radius=15)

        password_text = ft.TextField(label="Password",
                                    password=True,
                                    can_reveal_password=True,
                                    bgcolor=ft.colors.WHITE,
                                    focused_color=ft.colors.BLACK87,
                                    border_radius=15,
                                    height=40)

        password_confirm = ft.TextField(label="confirm Password",
                                        password=True,
                                        can_reveal_password=True,
                                        bgcolor=ft.colors.WHITE,
                                        focused_color=ft.colors.BLACK87,
                                        border_radius=15,
                                        height=40)

        email_text = ft.TextField(label="E-mail",
                                focused_color=ft.colors.BLACK87,
                                bgcolor=ft.colors.WHITE,
                                height=40,
                                border_radius=15,
                                keyboard_type=ft.KeyboardType.EMAIL)

        details = ft.Column([username_text, password_text, password_confirm, email_text], spacing=20)

        sign_up_button = ft.ElevatedButton(text="SIGN UP",
                                        on_click=self.sign_up_clicked,
                                        bgcolor=ft.colors.WHITE,
                                        color=ft.colors.BLACK87,
                                        height=47,
                                        elevation=2,
                                        style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(radius=2),
                                            color={
                                                ft.MaterialState.HOVERED: ft.colors.LIGHT_BLUE_200,
                                                ft.MaterialState.DEFAULT: ft.colors.WHITE,
                                                ft.MaterialState.FOCUSED: ft.colors.LIGHT_BLUE_200}
                                        ))

        has_account = ft.Text("Already have an account?",
                            color=ft.colors.WHITE,
                            size=18)

        login = ft.TextButton(
              content= ft.Text("Log in", 
                                color="#34aeed",
                                style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE,
                                decoration_color="#34aeed")),
               on_click=self.login_clicked)
       
        has_account_block = ft.Column(spacing=5,
                                    controls=[has_account, login],
                                    alignment=ft.alignment.center, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        sign_up_block = ft.Column(spacing=50,
                                controls=[details, sign_up_button, has_account_block],
                                alignment=ft.alignment.center, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        sign_up_container = ft.Container(
            content=sign_up_block,
            alignment=ft.alignment.center,
            padding=ft.padding.only(left=150),
            height=self.appLayout.page.width/3
        )

        logo = components.Logo(self.appLayout)

        self.row = ft.Row(
            controls=[logo.build(),
                    sign_up_container],
            alignment=ft.alignment.center, 
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True)

        return self.row

