from flet import (
    UserControl,
    Column,
    Container,
    IconButton,
    Row,
    Text,
    IconButton,
    NavigationRail,
    NavigationRailDestination,
    TextField,
    alignment,
    border_radius,
    colors,
    icons,
    padding,
    margin,
)

class Sidebar(UserControl):

    def __init__(self, app_layout, page):
        super().__init__()
        self.app_layout = app_layout
        self.nav_rail_visible = True
        self.top_nav_items = [
            NavigationRailDestination(
                label_content=Text("My Books"),
                label="My Books",
                icon=icons.LIBRARY_BOOKS,
                selected_icon=icons.LIBRARY_BOOKS
            ),
            NavigationRailDestination(
                label_content=Text("Book Search"),
                label="Book Search",
                icon=icons.SEARCH,
                selected_icon=icons.SEARCH
            ),
            NavigationRailDestination(
                label_content=Text("Find me a book"),
                label="Find me a book",
                icon=icons.RECOMMEND,
                selected_icon=icons.RECOMMEND
            ),


        ]
        self.top_nav_rail = NavigationRail(
            selected_index=None,
            label_type="all",
            on_change=self.top_nav_change,
            destinations=self.top_nav_items,
            bgcolor=colors.BLUE_GREY,
            extended=True,
            expand=True,
            height=110
        )
        self.toggle_nav_rail_button = IconButton(icons.ARROW_BACK)

    def build(self):
        self.view = Container(
            content=Column([
                self.top_nav_rail,
            ], tight=True),
            padding=padding.all(15),
            margin=margin.all(0),
            width=250,
            expand=True,
            bgcolor=colors.BLUE_GREY,
            visible=self.nav_rail_visible,
        )
        return self.view

    def toggle_nav_rail(self, e):
        self.view.visible = not self.view.visible
        self.view.update()
        self.page.update()

    def top_nav_change(self, e):
        index = e if (type(e) == int) else e.control.selected_index
        self.top_nav_rail.selected_index = index
        self.view.update()
        if index == 0:
            self.page.route = "/my-books"
        elif index == 1:
            self.page.route = "/book-search"
        elif index == 1:
            self.page.route = "/recommend"
        self.page.update()