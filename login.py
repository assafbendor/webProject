import flet as ft


def main(page: ft.Page):
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

    row = ft.Row(
        controls=[
            logo_container, vertical_line_container, login_container  # Place the vertical line between the text controls
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
