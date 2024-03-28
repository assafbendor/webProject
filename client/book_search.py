import flet as ft
from components import Logo

class BookSearch:

    def __init__(self, appLayout):
        super().__init__()
        self.appLayout = appLayout

    def search_clicked():
       pass

    def build(self):
        self.author   = ft.TextField(label="Author",
                                     focused_color=ft.colors.WHITE,
                                     bgcolor=ft.colors.WHITE12)
        self.title    = ft.TextField(label="Title")
        self.ISBN     = ft.TextField(label="ISBN")
        self.language = ft.TextField(label="Language")
        self.search   = ft.ElevatedButton(text="Search!",
                                         on_click=self.search_clicked,
                                         bgcolor=ft.colors.WHITE,
                                         color=ft.colors.BLACK87,
                                         height=47,
                                         elevation=2,
                                         style=ft.ButtonStyle(
                                             shape=ft.RoundedRectangleBorder(radius=2),
                                             color={
                                                 ft.MaterialState.HOVERED: ft.colors.LIGHT_BLUE_200,
                                                 ft.MaterialState.DEFAULT: ft.colors.WHITE,
                                                 ft.MaterialState.FOCUSED: ft.colors.LIGHT_BLUE_200}
                                         ))

        self.inputs            = ft.Column([self.author, self.title, self.ISBN, self.language],
                                           spacing=5)
        
        self.inputs_and_search = ft.Column([self.inputs, self.search], spacing=20, alignment=ft.alignment.center)
        self.inputs_container  = ft.Container(content=self.inputs_and_search,
                                             padding=ft.padding.only(top=100))

        return self.inputs_container