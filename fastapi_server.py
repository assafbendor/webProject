from typing import Union

from fastapi import FastAPI

import database

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/books")
def get_books():
    list = database.select_all_books()
    print("server books")
    return list


def get_book_list(user):
   pass


