import flet as ft
import os

class Logo(ft.UserControl):

    def __init__(self, appLayout):
        super().__init__()
        self.appLayout = appLayout

    def build(self):

        self.logo = ft.Image(
            src="img/logo.png",
            width=self.appLayout.page.width/3,  # Set the width of the image
            height=self.appLayout.page.width/3  # Set the height of the image
        )

        self.text = ft.Text("Book for You",
                            font_family="Calibiri",
                            size=50,
                            text_align=ft.TextAlign.RIGHT)

        self.column = ft.Column([self.logo, self.text],
                                alignment=ft.alignment.center,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        self.logo_container = ft.Container(
            content=self.column,
            padding=ft.padding.only(left=120),
            alignment=ft.alignment.center_left)

        # Create a Container to act as a vertical line
        self.vertical_line = ft.Container(
            width=1,  # Width of the line
            height=self.appLayout.page.height,
            bgcolor="#ea665e",  # Color of the line,
            alignment=ft.alignment.center
        )

        self.vertical_line_container = ft.Container(
            content=self.vertical_line,
            padding=ft.padding.only(top=60, left=100)
        )

        self.view=ft.Container(
            content=ft.Row(
                controls=[self.logo_container, self.vertical_line_container]),
            data=self,
            margin = ft.margin.all(0),
            padding = ft.padding.only(top=10, right=0),
            height = self.appLayout.page.height)
        return self.view
    
    def resize(self, width, height):
        self.view.height = height
        self.view.width = width
        self.view.update()    
