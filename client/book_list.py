from datetime import datetime
import json
import os
import flet as ft

class BookList:

    def __init__(self, appLayout):
        super().__init__()
        self.appLayout = appLayout
        
    def get_books(self):
        # path = "/books"
        # r = requests.get(server + path)
        # return r.json()
        with open("server/books.json", 'r') as file:
            books = json.load(file)
        return books        


    def prepare_rows(self,books):
        dataRows = []
        for book in books:
            row = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Image(src=os.path.join("client", "img", book['cover_image_filename']), height=45, width=30)),
                    ft.DataCell(ft.Text(book['title'])),
                    ft.DataCell(ft.Text(book['author'])),
                    ft.DataCell(ft.Text(datetime.now().date())),
                    ft.DataCell(ft.Text(datetime.now().date())),
            ],
            color={"hovered": ft.colors.BLACK})
            dataRows.append(row)
        return dataRows
        
    def build(self, books):
        self.appLayout.page.scroll = ft.ScrollMode.HIDDEN

        table = ft.DataTable(
                width=self.appLayout.page.width,
                horizontal_lines=ft.border.BorderSide(1, "white"),
                horizontal_margin=10,
                # bgcolor=ft.colors.LIGHT_BLUE_900,
                data_row_color={"hovered": ft.colors.WHITE},
                heading_row_color=ft.colors.BLACK12,
                column_spacing=50,
                columns=[
                    ft.DataColumn(
                        ft.Text("Book Cover"),
                    ),
                    ft.DataColumn(
                        ft.Text("Book Name"),
                        on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                    ),
                    ft.DataColumn(
                        ft.Text("Author"),
                        on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                    ),
                    ft.DataColumn(
                        ft.Text("Borrowed at"),
                        on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                    ),                    
                    ft.DataColumn(
                        ft.Text("Due"),
                        on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                    ),                    

                ],
                rows=self.prepare_rows(books),
            )
        
        return table