import flet 
from flet import (
    Page
)
 

class BookForYouApp:
    def __init__(self, page: Page):
        self.page = page
        self.page.update()