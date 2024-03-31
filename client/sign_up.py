import flet as ft
import requests
import re
from client_config import SERVER_URL
import components

class SignUp(ft.UserControl):

    def __init__(self, appLayout):
        super().__init__()
        self.appLayout = appLayout
        
    def validate_signup_data(name, username, email, password, repeat_password):
        errors = []

        # Validate name
        if not name:
            errors.append("Name is required.")

        # Validate username
        if not username:
            errors.append("Username is required.")
        elif len(username) < 3:
            errors.append("Username must be at least 3 characters long.")

        # Validate email
        if not email:
            errors.append("Email is required.")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            errors.append("Invalid email format.")

        # Validate password
        if not password:
            errors.append("Password is required.")
        elif len(password) < 6:
            errors.append("Password must be at least 6 characters long.")
        elif password != repeat_password:
            errors.append("Passwords do not match.")

        return errors

    def sign_up_clicked(self, e):
        path = "/sign_up"
        
        name     = self.fullname_text.value
        email    = self.email_text.value
        username = self.username_text.value
        password = self.password_text.value
        confirm  = self.password_confirm.value
        
        errors = self.validate_signup_data(username, email, password, confirm)
        
        if errors:
            print("Signup data is invalid")
            self.sign_up_error.content = ft.Text("Shira", color=ft.colors.WHITE, size=15),
            self.sign_up_error.visible = True
                    
            return
        
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = {
            'username': username,
            'email': email,
            'name': name,
            'password': password
        }
        
        print(username, password, email, name)
        r = requests.post(SERVER_URL + path, headers=headers, data=data)
        
        if r.status_code == 200:
            print("Successul signup")
        else:
          print("Failed to make the POST request. Status code:", r.status_code)
          self.sign_up_error.content = "Sign up Failed"
          self.sign_up_error.visible = True
          self.appLayout.page.update()
          

    def login_clicked(self, e):
        self.appLayout.page.route = "/login"
        self.appLayout.page.update()


    def build(self):
        
        self.fullname_text = ft.TextField(label="Full Name",
                                    focused_color=ft.colors.BLACK87,
                                    color=ft.colors.BLACK87,
                                    bgcolor=ft.colors.WHITE,
                                    height=40,
                                    border_color=ft.colors.BLACK54, 
                                    focused_border_color=ft.colors.BLACK,                                     
                                    border_radius=15)
        
        self.email_text = ft.TextField(label="E-mail",
                                focused_color=ft.colors.BLACK87,
                                color=ft.colors.BLACK87,
                                bgcolor=ft.colors.WHITE,
                                height=40,
                                border_radius=15,
                                border_color=ft.colors.BLACK54, 
                                focused_border_color=ft.colors.BLACK,                                     
                                keyboard_type=ft.KeyboardType.EMAIL)
        

        self.username_text = ft.TextField(label="Username",
                                    focused_color=ft.colors.BLACK87,
                                    bgcolor=ft.colors.WHITE,
                                    color=ft.colors.BLACK87,
                                    height=40,
                                    border_color=ft.colors.BLACK54, 
                                    focused_border_color=ft.colors.BLACK,                                     
                                    border_radius=15)

        self.password_text = ft.TextField(label="Password",
                                    password=True,
                                    can_reveal_password=True,
                                    bgcolor=ft.colors.WHITE,
                                    color=ft.colors.BLACK87,
                                    focused_color=ft.colors.BLACK87,
                                    border_color=ft.colors.BLACK54, 
                                    focused_border_color=ft.colors.BLACK,                                     
                                    border_radius=15,
                                    height=40)

        self.password_confirm = ft.TextField(label="confirm Password",
                                        password=True,
                                        can_reveal_password=True,
                                        bgcolor=ft.colors.WHITE,
                                        focused_color=ft.colors.BLACK87,
                                        color=ft.colors.BLACK87,
                                        border_radius=15,
                                        border_color=ft.colors.BLACK54, 
                                        focused_border_color=ft.colors.BLACK,                                     
                                        height=40)

    
        details = ft.Column([self.fullname_text, self.email_text, self.username_text, self.password_text, self.password_confirm], spacing=20)

        sign_up_button = ft.ElevatedButton(text="SIGN UP",
                                        on_click=self.sign_up_clicked,
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

        has_account = ft.Text("Already have an account?",
                            color=ft.colors.WHITE,
                            size=18)

     
        login = ft.TextButton(
              content= ft.Text("Log in", 
                                color="#34aeed",
                                style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE,
                                decoration_color="#34aeed")),
              on_click=self.login_clicked
        )

     
        has_account_block = ft.Column(spacing=5,
                                    controls=[has_account, login],
                                    alignment=ft.alignment.center, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        
        self.sign_up_error = ft.TextButton(
            visible=False,
            content=ft.Container(
                content= ft.Text("Invalid", color=ft.colors.WHITE, size=15),
                bgcolor=ft.colors.RED,                    
                padding=ft.padding.all(10),
            )
        )

        sign_up_block = ft.Column(spacing=50,
                                controls=[details, sign_up_button, has_account_block, self.sign_up_error ],
                                alignment=ft.alignment.center, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        sign_up_container = ft.Container(
            content=sign_up_block,
            alignment=ft.alignment.center,
            padding=ft.padding.only(left=self.appLayout.page.width/6),
            height=self.appLayout.page.height-250,
            data=self,
        )

        logo = components.Logo(self.appLayout)

        self.row = ft.Row(
            controls=[logo.build(),
                    sign_up_container],
            alignment=ft.alignment.center, 
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True)

        return self.row

