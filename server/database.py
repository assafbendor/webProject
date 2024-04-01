from typing import List, Type

from sqlalchemy import create_engine, or_
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

def get_author(author_id: int | None = None, author_name: str | None = None) -> models.Author | None:
    with Session() as session:
        if author_name is not None:
            author = session.query(models.Author).filter_by(name=author_name).first()
        elif author_id is not None:
            author = session.query(models.Author).filter_by(id=author_id).first()
        else:
            author = None
        return author


def add_author_to_database(author: models.Author):
    if get_author(author_name=author.name) is None:
        with Session() as session:
            session.add(author)
            session.commit()
        return True
    return False

def search_book_by_title(title: str) -> list[Book]:
    with Session() as session:
        book = session.query(Book).filter_by(title=title).all()
    return book

def search_book(isbn: str | None = None, author_name: str | None = None, author_id: int | None = None, title: str | None = None) -> list[Book] | None:
    with Session() as session:
        if isbn is not None:
            book_list = [session.query(Book).filter_by(isbn=isbn).first()]
        elif author_name is not None or author_id is not None:
            author = get_author(author_id=author_id, author_name=author_name)
            book_list = session.query(Book).filter_by(author=author)
        elif title is not None:
            book_list = session.query(Book).filter_by(title=title)
        else:
            book_list = None

        return book_list





def delete_reader(email: str) -> bool:
    user = find_users(email=email)
    if user is not None:
        with Session() as session:
            session.delete(user)
            session.commit()
            return True
    return False

def return_all_books() -> list[Book]:
    with Session() as session:
        book_list = session.query(Book).all()
    return book_list


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
    # print(add_reader_to_database(models.Reader(username="shira", email="shira.bendor@gmail.com", name="Shira Ben-Dor", password="shira1234")))
    # print(change_password("shira.bendor@gmail.com", "shira1234"))
    # print(find_users(email="shira.bendor@gmail.com"))
    # print(delete_reader(email="asaf.bendor2@gmail.com"))
    # print(add_author_to_database(models.Author(name="Benny", id=12345)))
    # print(get_author("Benny"))
    # print(search_book_by_author(get_author("Benny")))
    # new_book = Book(isbn="12345678", title="example")
    # print(search_book_by_isbn("12345678"))
    # print(add_book_to_database(new_book))
    # print(search_book_by_isbn("12345678"))
    # print(return_all_books())
    # print(search_book_by_title("1984"))
    # #print(search_book_by_author("Jane Austen"))
    # #print(search_book_by_author(author_name="George Orwell"))

