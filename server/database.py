from typing import List, Type

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from server.config import DATABASE_URL
from server.models import Book, Copy, Borrow

import api
import models

engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)


def get_all_books() -> list[Type[Book]]:
    with Session() as session:
        books = session.query(Book).all()
        return books


def get_copies_by_username(username: str):
    with Session() as session:
        borrows = session.query(Borrow).filter_by(reader_username=username, return_date=None).all()
        return [borrow.copy for borrow in borrows]

def find_users(email: str):
    with Session() as session:
        user = session.query(models.Reader).filter_by(email=email).first()
    return user


def add_reader_to_database(reader: models.Reader) -> bool:
    if find_users(email=reader.email) is None:
        with Session() as session:
            session.add(reader)
            session.commit()
            return True
    return False

def change_password(email: str, new_password) -> bool:
    if find_users(email=email) is not None:
        with Session() as session:
            user = session.query(models.Reader).filter_by(email=email).first()
            user.email = api.get_password_hash(password=new_password)
            session.commit()
            return True
    return False

def email_to_username(email: str):
    user = find_users(email)
    if user is None:
        return False
    return user.username

def find_user_by_username(username: str):
    with Session() as session:
        user = session.query(models.Reader).filter_by(username=username).first()
    return user

def search_book_by_author(author: models.Author):
    print(author.books)
    return author.books
def get_author(author_name: str):
    with Session() as session:
        return session.query(models.Author).filter_by(name=author_name).first()

def add_author_to_database(author: models.Author):
    if get_author(author.name) is None:
        with Session() as session:
            session.add(author)
            session.commit()
        return True
    return False

def search_book_by_isbn(isbn: str):
    with Session() as session:
        return session.query(Book).filter_by(isbn=isbn).first()

def search_book_by_title(title: str):
    with Session() as session:
        book = session.query(Book).filter_by(title=title)

def add_book_to_database(book: Book):
    if search_book_by_isbn(book.isbn) is None:
        with Session() as session:
            session.add(book)
            session.commit()
        return True
    return False

def delete_reader(email: str) -> bool:
    user = find_users(email=email)
    if user is not None:
        with Session() as session:
            session.delete(user)
            session.commit()
            return True
    return False




# def borrowed_for_more_than_a_month(username: str):
#     # There is no data_borrowed column in the database, only a borrow_date (start date) and return_date (end date)
#
#     with Session() as session:
#         borrows = session.query(Borrow).filter_by(reader_username=username, return_date=None).all()
#         return [borrow for borrow in borrows if (borrow.return_date - borrow.borrow_date).days > 30]



if __name__ == '__main__':
    books = get_all_books()
    # print(books[0].copies)
    # print(books)
    # print(get_copies_by_username('peter'))
    #print(add_reader_to_database(models.Reader(username="shira", email="shira.bendor@gmail.com", name="Shira Ben-Dor", password="shira1234")))
    # print(change_password("shira.bendor@gmail.com", "shira1234"))
    # print(find_users(email="shira.bendor@gmail.com"))
    # print(delete_reader(email="asaf.bendor2@gmail.com"))
    # print(add_author_to_database(models.Author(name="Benny", id=12345)))
    # print(get_author("Benny"))
    # print(search_book_by_author(get_author("Benny")))
    new_book = Book(isbn="12345678", title="example")
    print(search_book_by_isbn("12345678"))
    print(add_book_to_database(new_book))
    print(search_book_by_isbn("12345678"))


