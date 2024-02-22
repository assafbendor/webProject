import flet as ft
import database


def main(page: ft.Page):

    def sign_up_clicked(par):
        user = (username_text.value, password_text.value, email_text.value)
        database.create_user(user)

    # Setting the background color of the page
    page.bgcolor = "#083b7a"
    page.padding = 50

    logo = ft.Image(
        src="/Users/assafbendor/PycharmProjects/webProject/img/logo.png",
        width=400,  # Set the width of the image
        height=400,  # Set the height of the image
    )

    text = ft.Text("Book for You",
                   font_family="Calibiri",
                   size=50,
                   text_align=ft.TextAlign.RIGHT)

    column = ft.Column([logo, text],
                       alignment=ft.alignment.center,
                       horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    logo_container = ft.Container(
        content=column,
        padding=ft.padding.only(left=120),
        alignment=ft.alignment.center_left)

    # Create a Container to act as a vertical line
    vertical_line = ft.Container(
        width=1,  # Width of the line
        height=680,  # Height of the line, adjust as needed
        bgcolor="#ea665e",  # Color of the line,
        padding=ft.padding.only(top=90, left=140)
    )

    vertical_line_container = ft.Container(
        content=vertical_line,
        padding=ft.padding.only(top=60, left=150)
    )

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
                                       on_click=sign_up_clicked,
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

    login = ft.Text("Log in",
                    color="#34aeed",
                    style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE,
                                       decoration_color="#34aeed"))

    has_account_block = ft.Column(spacing=5,
                                  controls=[has_account, login],
                                  alignment=ft.alignment.center, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    sign_up_block = ft.Column(spacing=50,
                              controls=[details, sign_up_button, has_account_block],
                              alignment=ft.alignment.center, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    sign_up_container = ft.Container(
        content=sign_up_block,
        alignment=ft.alignment.center,
        padding=ft.padding.only(left=150)
    )

    row = ft.Row(
        controls=[
            logo_container, vertical_line_container, sign_up_container
            # Place the vertical line between the text controls
        ],
        alignment=ft.alignment.center,  # Center align the items vertically
    )

    # Add the row to the page

    page.add(row)

    page.update()


# Running the app
# ft.app(target=main,
#      view=ft.AppView.WEB_BROWSER,
#       assets_dir="/Users/assafbendor/PycharmProjects/webProject/img/")


ft.app(target=main)
