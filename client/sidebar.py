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
    def create_reader_nav_bar(self):
        return [
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
                    label_content=Text("Personal Books Recommendation"),
                    label="Find me a book",
                    icon=icons.RECOMMEND,
                    selected_icon=icons.RECOMMEND
                ),
        ]
    def create_admin_nav_bar(self):
        return [
                NavigationRailDestination(
                    label_content=Text("Loan Books"),
                    label="Loan Books",
                    icon=icons.LIBRARY_BOOKS,
                    selected_icon=icons.LIBRARY_BOOKS
                ),
                NavigationRailDestination(
                    label_content=Text("Return Books"),
                    label="Return Books",
                    icon=icons.LIBRARY_BOOKS_OUTLINED,
                    selected_icon=icons.LIBRARY_BOOKS_OUTLINED
                ),
                NavigationRailDestination(
                    label_content=Text("Add a New Nook"),
                    label="Add a New Book",
                    icon=icons.BOOKMARK_ADD_OUTLINED,
                    selected_icon=icons.BOOKMARK_ADD_OUTLINED
                ),
                NavigationRailDestination(
                    label_content=Text("Delete a Book"),
                    label="Delete a Book",
                    icon=icons.DELETE,
                    selected_icon=icons.DELETE
                ),
                NavigationRailDestination(
                    label_content=Text("Add a Librarian"),
                    label="Add a Librarian",
                    icon=icons.PERSON_ADD_ALT_1,
                    selected_icon=icons.PERSON_ADD_ALT_1
                ),
                NavigationRailDestination(
                    label_content=Text("Remove a Librarian"),
                    label="Delete a Book",
                    icon=icons.PERSON_OFF,
                    selected_icon=icons.PERSON_OFF
                ),
                
            ]
            
    def __init__(self, app_layout, is_admin: bool):
        super().__init__()
        self.app_layout = app_layout
        self.nav_rail_visible = True
        self.top_nav_items = self.create_reader_nav_bar()
        self.bottom_nav_items = self.create_admin_nav_bar() #if is_admin else None
        self.top_nav_rail = NavigationRail(
            selected_index=None,
            label_type="all",
            on_change=self.top_nav_change,
            destinations=self.top_nav_items,
            bgcolor=colors.BLUE_GREY,
            extended=True,
            height=150
        )
        self.bottom_nav_rail = NavigationRail(
            selected_index=None,
            label_type="all",
            on_change=self.bottom_nav_change,
            extended=True,
            expand=True,
            destinations=self.bottom_nav_items,
            bgcolor=colors.BLUE_GREY,
        )
        self.toggle_nav_rail_button = IconButton(icons.ARROW_BACK)

    def build(self):
        self.view = Container(
            content=Column([
                self.top_nav_rail,
                # Divider
                Container(
                    bgcolor=colors.BLACK26,
                    border_radius=border_radius.all(30),
                    height=1,
                    alignment=alignment.center_right,
                    width=220
                ),
                self.bottom_nav_rail                
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
        self.bottom_nav_rail.selected_index = None
        self.top_nav_rail.selected_index = index
        self.view.update()
        if index == 0:
            self.page.route = "/my-books"
        elif index == 1:
            self.page.route = "/book-search"
        elif index == 2:
            self.page.route = "/recommend"
        self.page.update()
        
        
    def bottom_nav_change(self, e):
        index = e if (type(e) == int) else e.control.selected_index
        self.top_nav_rail.selected_index = None
        self.bottom_nav_rail.selected_index = index
        self.view.update()
        if index == 0:
            self.page.route = "/loan-books"
        elif index == 1:
            self.page.route = "/return-books"
        elif index == 2:
            self.page.route = "/add-book"
        if index == 3:
            self.page.route = "/delete-book"
        elif index == 4:
            self.page.route = "/add-librarian"
        elif index == 5:
            self.page.route = "/remove-librarian"
        self.page.update()        
