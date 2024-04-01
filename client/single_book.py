import os
import flet as ft

class SingleBook():

    def __init__(self, appLayout, isbn):
        super().__init__()
        self.appLayout = appLayout
        self.isbn = isbn
        
    def get_book():
      #TODO
      return {
        "isbn": "9781094311166",
        "title": "Wuthering Heights",
        "author": "Emily Bront\u00c3\u00ab",
        "language": "English",
        "rating": 0,
        "cover_image_filename": "Wuthering Heights_Emily Bront\u00c3\u00ab.jpg",
        "description": "Wuthering Heights is a moody 19th-century triumph, lauded for its dark imagery, austere setting, and depiction of fraught romance. Wuthering Heights is Emily Bronte\u2019s account of the tormented love story between orphan Heathcliff and the daughter of his benefactor, Catherine Earnshaw. Troubled, stark, and violent, Wuthering Heights was hugely controversial at its publication in 1847, but has since become a classic of English literature. This Essential Classics edition includes a new introduction by Professor Vivian Heller, Ph.D. in literature and modern studies from Yale University. Emily Bronte was an English novelist and poet, best known for her only novel, Wuthering Heights. Silent and reserved, Bronte wrote using the pen name Ellis Bell, and was one of the Bronte siblings. Vivian Heller received her Ph.D. in English Literature and Modern Studies from Yale University. She is author of Joyce, Decadence, and Emancipation(University of Illinois Press) and of The City Beneath Us (W.W. Norton & Company), a history of the building of the New York City subway system. She is an associate at Columbia\u2019s School of Professional Studies and is the writing tutor for the Center for Curatorial Studies at Bard College. She is also a long-standing member of the non-fiction committee of the PEN Prison-Writing Committee, which awards prizes to inmates from across the country. Essential Classics publishes the most crucial literary works throughout history, with a unique introduction to each, making them the perfect treasure for any reader\u2019s shelf.",
        "ratings_count": 0,
        "average_rating": 3.2
    }

    def build(self):
        
        book = self.get_book()

        image_card = ft.Card(
            elevation=2,
            margin=2,
            shape=ft.ContinuousRectangleBorder,
            content=ft.Image(
                    src=os.path.join("client", "img", book['cover_image_filename']),
                    width=self.appLayout.page.width/4.5,  # Set the width of the image
                    height=self.appLayout.page.width/3  # Set the height of the image
                ))
        
        title = ft.Text(book['title'],theme_style=ft.TextThemeStyle.TITLE_LARGE )
        auther = ft.Text(book['author'],theme_style=ft.TextThemeStyle.TITLE_MEDIUM )
        
        pages = ft.Text(book['pages']+ "pages",theme_style=ft.TextThemeStyle.BODY_MEDIUM )
        
        summary = ft.Text(book['summary'],theme_style=ft.TextThemeStyle.BODY_SMALL )
