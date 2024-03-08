import json
from fastapi import FastAPI

import database

app = FastAPI()

def toJson(books):
    keys = ('Index', 'Book Name', 'Author', 'Availability')
    data = [dict(zip(keys, book)) for book in books]

    json_data = json.dumps(data)
    print(json_data)
    return json_data


@app.get("/books")
def get_books():
    list = database.select_all_books()
    return toJson(list)


def get_book_list(user):
   pass


