from flet import (
    Control,
    Page,
    Row,
    Text)

class AppLayout(Row):
    def __init__(
        self,
        app,
        page: Page,
        *args,
        **kwargs):
        
        super().__init__(*args, **kwargs)
        self.app = app
        self.page = page
        self._active_view: Control = Row(controls=[Text("Active View")], 
                                         alignment="center", 
                                         horizontal_alignment="center")
        

    @property
    def active_view(self):
        return self._active_view
 
    @active_view.setter
    def active_view(self, view):
        self._active_view = view
        self.update()