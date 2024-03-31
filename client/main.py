import flet as ft
from app_layout import AppLayout
from flet import (
    AlertDialog,
    AppBar,
    Column,
    Container,
    ElevatedButton,
    Icon,
    Page,
    PopupMenuButton,
    PopupMenuItem,
    RoundedRectangleBorder,
    Row,
    TemplateRoute,
    Text,
    TextField,
    UserControl,
    View,
    colors,
    icons,
    margin,
    padding,
    theme,
)

class BookForYouApp(UserControl):
    def __init__(self, page: Page):
        super().__init__()

        self.page = page
        self.page.on_route_change = self.route_change
        self.appbar = AppBar(
            leading=Icon(ft.icons.MENU_BOOK),
            leading_width=75,
            title=Text(f"Book For You", font_family="Callibiry", size=32, text_align="start"),
            center_title=False,
            toolbar_height=75,
            bgcolor=colors.LIGHT_BLUE_ACCENT_700,
        )
        self.page.appbar = self.appbar
        self.page.update()

    def build(self):
        self.layout = AppLayout(
            self,
            self.page,
            tight=True,
            expand=True,
            #vertical_alignment="start",
            alignment="center",
        )
        return self.layout

    def initialize(self):
        # self.page.views.clear()
        self.page.views.append(
            View(
                "/",
                [self.appbar, self.layout],
                padding=padding.all(0),
                bgcolor="#083b7a",
            )
        )

        self.page.update()

        self.page.go("/")

    def route_change(self, e):
        troute = TemplateRoute(self.page.route)
        if troute.match("/"):
            self.page.go("/login")
        elif troute.match("/sign_up"):
            self.layout.set_signup_view()
        elif troute.match("/login"):
            self.layout.set_login_view()            
        elif troute.match("/book-search"):
            self.layout.set_book_search_view()                        
        elif troute.match("/my-books"):
            self.layout.set_book_list_view("my-books")                                
        self.page.update()

def main(page: Page):

    page.title = "BookForYou"
    page.padding = 0
    page.theme = theme.Theme(font_family="Calibiri")
    page.theme.page_transitions.windows = "cupertino"
    page.fonts = {"Calibiri": "Calibiri-Regular.ttf"}
    page.bgcolor = "#083b7a"
    app = BookForYouApp(page)
    page.add(app)
    page.update()
    app.initialize()


ft.app(target=main, assets_dir="../assets")