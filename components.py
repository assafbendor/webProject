import flet as ft

class Logo():
    def build(self):
        self.logo = ft.Image(
            src="..\img\logo.png",
            width=400,  # Set the width of the image
            height=400  # Set the height of the image
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
            bgcolor="#ea665e",  # Color of the line,
            padding=ft.padding.only(top=90, left=140),
            alignment=ft.alignment.center
        )

        self.vertical_line_container = ft.Container(
            content=self.vertical_line,
            padding=ft.padding.only(top=60, left=150)
        )
        
        return ft.Row(controls=[self.logo_container, self.vertical_line_container])
