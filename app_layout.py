import flet as ft

from login import Login

class AppLayout(ft.Row):
    def __init__(
        self,
        app,
        page: ft.Page,
        *args,
        **kwargs):
        
        super().__init__(*args, **kwargs)
        self.app = app
        self.page = page
        self.page.on_resize = self.page_resize
        self.login = Login(self, page)
        self.login_view = self.login.build()
        self._active_view: ft.Control = self.login_view
        self.controls = [self.active_view]

    @property
    def active_view(self):
        return self._active_view
 
    @active_view.setter
    def active_view(self, view):
        self._active_view = view
        self.update()

    def page_resize(self, e=None):
        self.active_view.resize(self.page.width, 
                                self.page.height)
        self.page.update()        
