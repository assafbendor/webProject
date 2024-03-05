from typing import Union

from fastapi import FastAPI

import database

app = FastAPI()

@app.get("/books")
def get_books():
    list = database.select_all_books()
    return list


def get_book_list(user):
   pass


