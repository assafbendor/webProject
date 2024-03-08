import flet as ft
from components import Logo

def main(page: ft.Page):
    # Setting the background color of the page
    page.bgcolor = "#083b7a"
    page.padding = 50

    logo = Logo()
 
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

    forgot_password = ft.Text("Forgot password?",
                              color="#34aeed",
                              size=12,
                              style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE,
                                                 decoration_color="#34aeed"))

    password_block = ft.Column([password_text, forgot_password],
                               spacing=5,
                               horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    details = ft.Column([username_text, password_block], spacing=20)

    login_button = ft.ElevatedButton(text="LOG IN",
                                     on_click="login_clicked",
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

    no_account = ft.Text("Don't have an account?",
                         color=ft.colors.WHITE,
                         size=18)

    sign_up = ft.Text("Sign Up",
                      color="#34aeed",
                      style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE,
                                         decoration_color="#34aeed"))

    no_account_block = ft.Column(spacing=5,
                                 controls=[no_account,sign_up],
                                 alignment=ft.alignment.center, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    login_block = ft.Column(spacing=50,
                            controls=[details, login_button, no_account_block],
                            alignment=ft.alignment.center, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    login_container = ft.Container(
        content=login_block,
        alignment=ft.alignment.center,
        padding=ft.padding.only(left=150)
    )

   
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.update()

    row=ft.Row(controls=[logo.build(), login_container],
                       width=page.window_width)

    page.add(row)
    page.update()


#Running the app
ft.app(target=main)
#       assets_dir="/Users/assafbendor/PycharmProjects/webProject/img/")


#ft.app(target=main)
