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
            vertical_alignment="start",
        )
        return self.layout

    def initialize(self):
        self.page.views.clear()
        self.page.views.append(
            View(
                "/",
                [self.appbar, self.layout],
                padding=padding.all(0),
                bgcolor="#083b7a",
            )
        )
        self.page.update()
        #self.page.go("/")

    def route_change(self, e):
        troute = TemplateRoute(self.page.route)
        if troute.match("/"):
            self.page.go("/login")
        elif troute.match("/sign_up"):
            self.layout.set_signup_view()
        self.page.update()

    def add_board(self, e):
        def close_dlg(e):
            if (hasattr(e.control, "text") and not e.control.text == "Cancel") or (
                type(e.control) is TextField and e.control.value != ""
            ):
                self.create_new_board(dialog_text.value)
            dialog.open = False
            self.page.update()

        def textfield_change(e):
            if dialog_text.value == "":
                create_button.disabled = True
            else:
                create_button.disabled = False
            self.page.update()

        dialog_text = TextField(
            label="New Board Name", on_submit=close_dlg, on_change=textfield_change
        )
        create_button = ElevatedButton(
            text="Create", bgcolor=colors.BLUE_200, on_click=close_dlg, disabled=True
        )
        dialog = AlertDialog(
            title=Text("Name your new board"),
            content=Column(
                [
                    dialog_text,
                    Row(
                        [
                            ElevatedButton(text="Cancel", on_click=close_dlg),
                            create_button,
                        ],
                        alignment="spaceBetween",
                    ),
                ],
                tight=True,
            ),
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
        dialog_text.focus()

    def create_new_board(self, board_name):
        print("new board")
    def delete_board(self, e):
        print("delete board")

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