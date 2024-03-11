import json
from fastapi import FastAPI

import database

app = FastAPI()

def toJson(objects, keys):
    keys = ('Username', 'Password', 'Email')

    data = [dict(zip(keys, book)) for book in objects]

    json_data = json.dumps(data)
    print(json_data)
    return json_data


@app.get("/books")
def get_books():
    lst = database.select_all_books()
    return toJson(lst, ('Index', 'Book Name', 'Author', 'Availability'))

@app.get("/users")
def get_users():
    lst = database.select_all_users()
    return toJson(lst, ('Username', 'Password', 'Email'))

def get_book_list(user):
   pass


