import flet as ft
from components import Logo
import requests
import client_config

class Login:

    def resize(self, nav_rail_extended, width, height):
        self.view.width = width
        self.view.height = height
        self.view.update()    

    def __init__(self, appLayout):
        super().__init__()
        self.appLayout = appLayout
        
    def get_token(self):
       return self.token

    def login_clicked(self, e):
        path = "/token"

        username = self.username_text.value
        password = self.password_text.value
        
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = {
            'username': username,
            'password': password,
        }
        
        print(username, password)
        
        try:
            r = requests.post(client_config.SERVER_URL + path, headers=headers, data=data)
            # Parse the response JSON data
            r.raise_for_status()
            response_data = r.json()
            # Extract the "token" key from the response body
            self.token = response_data.get("access_token")
            if self.token:
                print("Token:", self.token)
                self.appLayout.on_login()
            else:
                print("Token not found in the response body.")
                self.login_error.visible = True
                self.appLayout.page.update()
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            self.login_error.visible = True
            self.appLayout.page.update()
        except Exception as err: 
            print("Failed to make the POST request. Status code:", r.status_code)
            self.login_error.visible=True
            self.appLayout.page.update()
           

    def sign_up_clicked(self, e):
        self.appLayout.page.route = "/sign_up"
        self.appLayout.page.update()

    def build(self):

        self.username_text = ft.TextField(label="Username",
                                     focused_color=ft.colors.BLACK87,
                                     color=ft.colors.BLACK87,
                                     bgcolor=ft.colors.WHITE,
                                     border_color=ft.colors.BLACK54, 
                                     focused_border_color=ft.colors.BLACK, 
                                     height=40,
                                     border_radius=15)

        self.password_text = ft.TextField(label="Password",
                                     password=True,
                                     color=ft.colors.BLACK87,
                                     can_reveal_password=True,
                                     bgcolor=ft.colors.WHITE,
                                     focused_color=ft.colors.BLACK87,
                                     border_radius=15,
                                     border_color=ft.colors.BLACK54, 
                                     focused_border_color=ft.colors.BLACK,                                      
                                     height=40)

        forgot_password = ft.Text("Forgot password?",
                                  color="#34aeed",
                                  size=12,
                                  style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE,
                                                     decoration_color="#34aeed"))

        password_block = ft.Column([self.password_text, forgot_password],
                                   spacing=5,
                                   horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        details = ft.Column([self.username_text, password_block], spacing=20)

        login_button = ft.ElevatedButton(text="LOG IN",
                                         on_click=self.login_clicked,
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

        no_account = ft.Text("Don't have an account?",
                             color=ft.colors.WHITE,
                             size=18)
        

        sign_up = ft.TextButton(
              content= ft.Text("Sign Up", 
                                color="#34aeed",
                                style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE,
                                decoration_color="#34aeed")),
               on_click=self.sign_up_clicked)
    
        no_account_block = ft.Column(spacing=5,
                                     controls=[no_account, sign_up],
                                     alignment=ft.alignment.center, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

      
        self.login_error =  ft.TextButton(
            visible=False,
            content=ft.Container(
                content= ft.Text("The username or password is incorrect", color=ft.colors.WHITE, size=15),
                bgcolor=ft.colors.RED,                    
                padding=ft.padding.all(10),
            )
        )
        
        login_block = ft.Column(spacing=50,
                                controls=[details, login_button, no_account_block, self.login_error],
                                alignment=ft.alignment.center, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        login_container = ft.Container(
            content=login_block,
            alignment=ft.alignment.center,
            padding=ft.padding.only(left=self.appLayout.page.width/6),
            data=self,
            height=self.appLayout.page.height-250
        )

        logo = Logo(self.appLayout)
        self.view = ft.Container(content = ft.Row(
            controls=[logo.build(), login_container],
            alignment=ft.alignment.center, 
            vertical_alignment=ft.CrossAxisAlignment.CENTER, 
            expand=True,
            ))
        
        return self.view
