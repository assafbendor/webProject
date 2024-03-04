import flet as ft

def main(page: ft.Page):

    def loan_books_clicked():
        pass

    def return_books_clicked():
        pass

    def extend_book_clicked():
        pass

    def logout_clicked():
        pass

    username="Shira_Librarian"

    # Setting the background color of the page
    page.bgcolor = "#ECEEF0"
    page.padding = 50

    hello = str("Hello, " + username + "!" + '\n')
    hello_text = ft.Text(hello,
                   font_family="Calibiri",
                   theme_style=ft.TextThemeStyle.DISPLAY_LARGE,
                   text_align=ft.TextAlign.CENTER,
                   color=ft.colors.BLACK54)
    
    logo = ft.Image(
        src="..\img\logo.png",
        width=400,  # Set the width of the image
        height=400  # Set the height of the image
    )

    text = ft.Text("Book for You",
                   font_family="Calibiri",
                   size=50,
                   text_align=ft.TextAlign.RIGHT,
                   color=ft.colors.BLACK54)

    column = ft.Column([hello_text, logo, text],
                       alignment=ft.alignment.center,
                       horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    logo_container = ft.Container(
        content=column,
        padding=ft.padding.only(left=120),
        alignment=ft.alignment.center_left)

    # Create a Container to act as a vertical line
    vertical_line = ft.Container(
        width=1,  # Width of the line
        height=page.window_height,  # Height of the line, adjust as needed
        bgcolor="#ea665e",  # Color of the line,
        padding=ft.padding.only(top=90, left=140),
        alignment=ft.alignment.center
    )

    vertical_line_container = ft.Container(
        content=vertical_line,
        padding=ft.padding.only(top=60, left=150)
    )
    
    what_to_do = "What would you like to do today?"
    what_to_do_text = ft.Text(what_to_do,
                   font_family="Calibiri",
                   theme_style=ft.TextThemeStyle.DISPLAY_SMALL,
                   text_align=ft.TextAlign.CENTER,
                   color=ft.colors.BLACK54)
    
    def on_action_hover(e):
        e.control.bgcolor = ft.colors.BLACK26 if e.data == "true" else ft.colors.BLACK54
        e.control.shadow.blur_radius = 15 if e.data == "true" else 5
        e.control.update()    
      
    my_books_button = ft.Container(
        content=ft.Text("Loan Books", font_family="Calibiry", size=20),
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
        on_click=loan_books_clicked)


    search_books_button = ft.Container(
        content=ft.Text("Return Books", font_family="Calibiry", size=20),
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
        on_click=return_books_clicked)
    
    recommend_button = ft.Container(
        content=ft.Text("Extend Book", font_family="Calibiry", size=20),
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
        on_click=extend_book_clicked)
    
    actions_row = ft.Row(controls=[my_books_button, search_books_button, recommend_button],
                         alignment=ft.alignment.center,
                         spacing=50)

    actions_column = ft.Column([what_to_do_text, actions_row], spacing=100)                     
    
    actions_container = ft.Container(actions_column, padding=150)

    page_row = ft.Row([logo_container, vertical_line_container, actions_container])

    logout_button = ft.FloatingActionButton(
        icon=ft.icons.LOGOUT, on_click=logout_clicked, bgcolor=ft.colors.BLACK54, tooltip="logout")

    page.add(page_row)
    page.add(logout_button)
    page.update()

ft.app(target=main)