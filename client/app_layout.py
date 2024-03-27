
import login
import sign_up
import components
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
    padding,
)
from sidebar import Sidebar


class AppLayout(Row):
    def __init__(self, app, page: Page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.page = page    
        self.page.on_resize = self.page_resize
        self.toggle_nav_rail_button = IconButton(
            icon=icons.ARROW_CIRCLE_LEFT,
            icon_color=colors.BLUE_GREY_400,
            selected=False,
            selected_icon=icons.ARROW_CIRCLE_RIGHT,
            on_click=self.toggle_nav_rail,
        )
        self.sidebar = Sidebar(self, page)

        self.login = login.Login(self)
        #self.login_view = Row(controls = [self.login.build()], expand=True)
        self.login_view = self.login.build()

        self.sign_up = sign_up.SignUp(self)
        self.sign_up_view = self.sign_up.build()

        self._active_view: Control = self.login_view
        print(type(self.active_view))
        self.controls = [self.sidebar, self.toggle_nav_rail_button, self.active_view]

    @property
    def active_view(self):
        return self._active_view

    @active_view.setter
    def active_view(self, view):
        self._active_view = view
        self.controls[-1] = self._active_view
        self.sidebar.sync_board_destinations()
        self.update()

    def set_login_view(self):
        self._active_view=self.login_view
        self.sidebar.update()
        self.page.update()
        self.page_resize()

    def set_signup_view(self):
        self._active_view=self.sign_up_view
        self.sidebar.update()
        self.page.update()
        self.page_resize()


    def set_all_boards_view(self):
        self.active_view = self.all_boards_view
        self.hydrate_all_boards_view()
        self.sidebar.top_nav_rail.selected_index = 0
        self.sidebar.bottom_nav_rail.selected_index = None
        self.sidebar.update()
        self.page.update()

    def set_members_view(self):
        self.active_view = self.members_view
        self.sidebar.top_nav_rail.selected_index = 1
        self.sidebar.bottom_nav_rail.selected_index = None
        self.sidebar.update()
        self.page.update()

    def page_resize(self, e=None):
        # if type(self.active_view) is Board:
        #     self.active_view.resize(
        #         self.sidebar.visible, self.page.width, self.page.height
        #     )
        self.page.update()

    def hydrate_all_boards_view(self):
        self.all_boards_view.controls[-1] = Row(
            [
                Container(
                    content=Row(
                        [
                            Container(
                                content=Text(value=b.name),
                                data=b,
                                expand=True,
                                on_click=self.board_click,
                            ),
                            Container(
                                content=PopupMenuButton(
                                    items=[
                                        PopupMenuItem(
                                            content=Text(
                                                value="Delete",
                                                style="labelMedium",
                                                text_align="center",
                                            ),
                                            on_click=self.app.delete_board,
                                            data=b,
                                        ),
                                        PopupMenuItem(),
                                        PopupMenuItem(
                                            content=Text(
                                                value="Archive",
                                                style="labelMedium",
                                                text_align="center",
                                            ),
                                        ),
                                    ]
                                ),
                                padding=padding.only(right=-10),
                                border_radius=border_radius.all(3),
                            ),
                        ],
                        alignment="spaceBetween",
                    ),
                    border=border.all(1, colors.BLACK38),
                    border_radius=border_radius.all(5),
                    bgcolor=colors.WHITE60,
                    padding=padding.all(10),
                    width=250,
                    data=b,
                )
                for b in self.store.get_boards()
            ],
            wrap=True,
        )
        self.sidebar.sync_board_destinations()

    def board_click(self, e):
        self.sidebar.bottom_nav_change(self.store.get_boards().index(e.control.data))

    def toggle_nav_rail(self, e):
        self.sidebar.visible = not self.sidebar.visible
        self.toggle_nav_rail_button.selected = not self.toggle_nav_rail_button.selected
        self.page_resize()
        self.page.update()