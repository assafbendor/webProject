import flet as ft
from app_layout import AppLayout

class BookForYouApp(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.page.update()

    def build(self):
        self.layout = AppLayout(
            self,
            self.page,
            tight=True,
            expand=True,
            vertical_alignment="start",
        )
        return self.layout    
    
    def initialize(self):
        self.page.views.clear()
        self.page.views.append(
            ft.View(
                "/",
                [self.appbar, self.layout],
                padding=ft.padding.all(0),
                bgcolor=ft.colors.BLUE_GREY_200,
            )
        )
        self.page.update()
        self.page.go("/")            
 
def main(page: ft.Page):
 
    page.title = "Book for You"
    page.padding = 0
    page.bgcolor = "#083b7a"
    app = BookForYouApp(page)
    page.add(app)
    page.update()
    app.build()

ft.app(target=main)