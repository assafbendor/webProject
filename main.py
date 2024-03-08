import flet
from flet import (
    Page,
    colors
)

from BookForYouApp import BookForYouApp
 
if __name__ == "__main__":
 
    def main(page: Page):
 
        page.title = "Book for You"
        page.padding = 0
        page.bgcolor = "#083b7a"
        app = BookForYouApp(page)
        page.add(app)
        page.update()
 
    flet.app(target=main, view=flet.WEB_BROWSER)