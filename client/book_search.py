import os
import flet as ft
from components import Logo
import requests
import client_config


class BookSearch:

    def __init__(self, appLayout):
        super().__init__()
        self.appLayout = appLayout

    def search_clicked(self, e):
        path = "/findbook"

        isbn = self.ISBN.value
        
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        params = {
            'isbn': isbn,
        }
        
        print(isbn)        
        try:
            r = requests.get(client_config.SERVER_URL + path, headers=headers, params=params)
            # Parse the response JSON data
            r.raise_for_status()
            response_data = r.json()
            # Extract the book info from the response body
            # TODO
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            self.login_error.visible = True
            self.appLayout.page.update()
        except Exception as err: 
            print("Failed to make the POST request. Status code:", r.status_code)
            self.login_error.visible=True
            self.appLayout.page.update()
   
    def slider_changed(self, e):
       self.selected_rating = {e.control.value}

    def build(self):
        
        self.page_title           = ft.Text("Search For Any Book", theme_style=ft.TextThemeStyle.DISPLAY_LARGE)
        self.page_title_container = ft.Container(content=self.page_title, padding=ft.padding.only(bottom=20)) 
        
        self.author   = ft.TextField(label="Author", 
                                     border_color=ft.colors.BLACK54, 
                                     focused_border_color=ft.colors.BLACK, 
                                     width=self.appLayout.page.width/2,
                                      focused_color=ft.colors.BLACK87 )
        self.title    = ft.TextField(label="Title",  
                                     border_color=ft.colors.BLACK54, 
                                     focused_border_color=ft.colors.BLACK, 
                                     width=self.appLayout.page.width/2,
                                     focused_color=ft.colors.BLACK87 )
        self.ISBN     = ft.TextField(label="ISBN",
                                     border_color=ft.colors.BLACK54, 
                                     focused_border_color=ft.colors.BLACK, 
                                     width=self.appLayout.page.width/2,
                                      focused_color=ft.colors.BLACK87 )
        self.language = ft.TextField(label="Language",
                                     border_color=ft.colors.BLACK54, 
                                     focused_border_color=ft.colors.BLACK, 
                                     width=self.appLayout.page.width/2,
                                     focused_color=ft.colors.BLACK87 )

        self.search = ft.ElevatedButton(text="SEARCH!",
                                          icon=ft.icons.SEARCH_OUTLINED,
                                          on_click=self.search_clicked,
                                          bgcolor=ft.colors.WHITE54,
                                          color=ft.colors.BLACK87,
                                          height=47,
                                          elevation=10,
                                          style=ft.ButtonStyle(
                                             shape=ft.RoundedRectangleBorder(radius=5),
                                             color={
                                                 ft.MaterialState.HOVERED: ft.colors.LIGHT_BLUE_200,
                                                 ft.MaterialState.DEFAULT: ft.colors.WHITE54,
                                                 ft.MaterialState.FOCUSED: ft.colors.LIGHT_BLUE_200}
                                         ))

        
        self.rating_text = ft.Text("Minimal Book Score")
        self.rating      = ft.Slider(min=1, max=5, divisions=0.5, label="{value}", on_change=self.slider_changed)
        self.rating_row  = ft.Row(controls=[self.rating_text, self.rating])
        
        self.inputs = ft.Column([self.author, self.title, self.ISBN, self.language, self.rating_row], spacing=5)
        
        self.inputs_container  = ft.Container(content=self.inputs, 
                                              bgcolor=ft.colors.WHITE,
                                              padding=ft.padding.all(20),
                                              border=ft.border.all(1, ft.colors.BLACK),
                                              border_radius=ft.border_radius.all(20),
                                              shadow=ft.BoxShadow(
                                                                    spread_radius=1,
                                                                    blur_radius=15,
                                                                    color=ft.colors.BLUE_GREY_300,
                                                                    offset=ft.Offset(0, 0),
                                                                    blur_style=ft.ShadowBlurStyle.OUTER,))
        
        self.inputs_and_search            = ft.Column([self.page_title_container, self.inputs_container, self.search], 
                                                      spacing=20, 
                                                      alignment=ft.alignment.center, 
                                                      horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        self.inputs_and_search_container  = ft.Container(content=self.inputs_and_search,
                                             padding=ft.padding.only(top=50, left=250), alignment=ft.alignment.center)
        
        
        self.trending_title = ft.Text("Trending Books", theme_style=ft.TextThemeStyle.DISPLAY_MEDIUM)
        self.trending_title_container = ft.Container(content=self.trending_title, padding=ft.padding.only(top=20, bottom=50)) 
        
        # TODO: select top 5 books
        
        self.book1 = ft.Image(
            src = os.path.join("client", "img", "The Sound and the Fury_William Faulkner.jpg"),
            width=self.appLayout.page.width/9,  # Set the width of the image
            height=self.appLayout.page.width/6  # Set the height of the image
            
        )
        
        self.book2 = ft.Image(
            src = os.path.join("client", "img", "A Christmas Carol_Charles Dickens.jpg"),
            width=self.appLayout.page.width/9,  # Set the width of the image
            height=self.appLayout.page.width/6  # Set the height of the image
        )
            
        self.book3 = ft.Image(
            src = os.path.join("client", "img", "The Road_Cormac McCarthy.jpg"),
            width=self.appLayout.page.width/9,  # Set the width of the image
            height=self.appLayout.page.width/6  # Set the height of the image
        )
        self.book4 = ft.Image(
            src = os.path.join("client", "img", "The Scarlet Letter_Nathaniel Hawthorne.jpg"),
            width=self.appLayout.page.width/9,  # Set the width of the image
            height=self.appLayout.page.width/6  # Set the height of the image
        )
                    
        self.book5 = ft.Image(
            src = os.path.join("client", "img", "A Clockwork Orange_Anthony Burgess.jpg"),                
            width=self.appLayout.page.width/9,  # Set the width of the image
            height=self.appLayout.page.width/6  # Set the height of the image
        )
        
        self.trending_row = ft.Row(controls=[self.book1, self.book2, self.book3, self.book4, self.book5], spacing=30)
        self.trending_column = ft.Column(controls=[self.trending_title_container, self.trending_row])
        self.trending_container = ft.Container(content = self.trending_column, padding=ft.padding.only(top=30, left=250), alignment=ft.alignment.center )    
        self.final_column = ft.Column(controls = [self.inputs_and_search_container, self.trending_container], alignment=ft.alignment.center)
        
        return self.final_column