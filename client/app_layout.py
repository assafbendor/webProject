import string
from sidebar import Sidebar

import login
import sign_up
import book_search
import book_list

from flet import (
    ButtonStyle,
    Column,
    Container,
    Control,
    IconButton,
    Page,
    PopupMenuButton,
    PopupMenuItem,
    RoundedRectangleBorder,
    Row,
    Text,
    TextButton,
    TextField,
    border,
    border_radius,
    colors,
    icons,
    alignment,
    padding,
    FloatingActionButton,
)


class AppLayout(Row):
    def __init__(self, app, page: Page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.book_list_view = None
        self.app = app
        self.page = page
        self.page.on_resize = self.page_resize
        self.toggle_nav_rail_button = IconButton(
            icon=icons.ARROW_CIRCLE_LEFT,
            icon_color=colors.BLUE_GREY_400,
            selected=False,
            visible=False,
            selected_icon=icons.ARROW_CIRCLE_RIGHT,
            on_click=self.toggle_nav_rail,
        )

        self.logout_button = FloatingActionButton(
            icon=icons.LOGOUT,
            on_click=self.on_logout,
            bgcolor=colors.WHITE54,
            tooltip="logout",
            visible=False)

        self.sidebar = Sidebar(self, True)
        self.sidebar.visible = False

        self.login = login.Login(self)
        self.login_view = self.login.build()

        self.sign_up = sign_up.SignUp(self)
        self.sign_up_view = self.sign_up.build()

        self.book_search = book_search.BookSearch(self)
        self.book_search_view = self.book_search.build()

        self.book_list = book_list.BookList(self)

        # self.single_book = single_book.SingleBook(self)
        # self.single_book_view = None

        self._active_view: Control = self.login_view
        self.controls = [self.sidebar, self.toggle_nav_rail_button, self.active_view]

    @property
    def active_view(self):
        return self._active_view

    @active_view.setter
    def active_view(self, view):
        self._active_view = view
        self.controls[-1] = self._active_view
        # self.sidebar.sync_board_destinations()
        self.update()

    def set_login_view(self):
        self.active_view = self.login_view
        # self.sidebar.update()
        self.page.update()
        self.page_resize()

    def set_signup_view(self):
        self.active_view = self.sign_up_view
        # self.sidebar.update()
        self.page.update()
        self.page_resize()

    def set_book_search_view(self):
        self.active_view = self.book_search_view
        self.sidebar.top_nav_rail.selected_index = 1
        self.sidebar.update()
        self.page.update()
        self.page_resize()

#    def set_book_list_view(self, list_type: string):
        # if list_type == "my-books":
        #     books = self.book_list.get_books()
    def set_book_list_view(self, books):
        self.book_list_view = self.book_list.build(books)
        self.active_view = self.book_list_view
        self.sidebar.top_nav_rail.selected_index = 0
        self.sidebar.update()
        self.page.update()
        self.page_resize()

    # def set_single_book_view(self, isbn):
    #     self.active_view = self.single_book.build(isbn)
    #     self.page.update()
    #     self.page_resize()

    def page_resize(self, e=None):
        # self.active_view.resize(
        #         self.page.width, self.page.height
        #     )
        # self.page.update()
        pass

    def toggle_nav_rail(self, e):
        self.sidebar.visible = not self.sidebar.visible
        self.toggle_nav_rail_button.selected = not self.toggle_nav_rail_button.selected
        self.page_resize()
        self.page.update()

    def on_login(self):
        self.sidebar.visible = True
        self.toggle_nav_rail_button.visible = True
        self.logout_button.visible = True
        self.set_book_search_view()
        self.page_resize()
        self.page.update()

    def on_logout(self, e):
        self.sidebar.visible = False
        self.toggle_nav_rail_button.visible = False
        self.logout_button.visible = False
        self.page_resize()
        self.page.update()

