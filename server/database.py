from typing import List, Type

from sqlalchemy import create_engine, DateTime
from sqlalchemy.orm import sessionmaker

from server.config import DATABASE_URL
from server.models import Book, Copy, Borrow

import api
import models
import random
import datetime

engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)

def get_all_books() -> list[Type[Book]]:
    with Session() as session:
        book_list = session.query(Book).all()
        return book_list

def get_all_users():
    with Session() as session:
        users = session.query(models.Reader).all()
    return users

def get_copies_by_username(username: str):
    with Session() as session:
        borrows = session.query(Borrow).filter_by(reader_username=username, return_date=None).all()
        return [borrow.copy for borrow in borrows]

def find_users(username: str | None = None, email: str | None = None, name: str | None = None) -> models.Reader | None:
    with Session() as session:
        if email is not None:
            user = session.query(models.Reader).filter_by(email=email).first()
        elif username is not None:
            user = session.query(models.Reader).filter_by(username=username).first()
        elif name is not None:
            user = session.query(models.Reader).filter_by(name=name)
        else:
            user = None
    return user


def add_reader_to_database(reader: models.Reader) -> bool:
    if find_users(email=reader.email, username=reader.username, name=reader.name) is None:
        with Session() as session:
            session.add(reader)
            session.commit()
            return True
    return False

def change_password(email: str, new_password) -> bool:
    if find_users(email=email) is not None:
        with Session() as session:
            user = session.query(models.Reader).filter_by(email=email).first()
            user.password = api.get_password_hash(password=new_password)
            session.commit()
            return True
    return False

def email_to_username(email: str):
    user = find_users(email)
    if user is None:
        return False
    return user.username


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


def search_book(isbn: str | None = None,
                author_name: str | None = None,
                author_id: int | None = None,
                title: str | None = None,
                language: str | None = None,
                rating: float | None = None)\
        -> list[Book] | None:
    with Session() as session:
        if isbn is not None:
            book_list = [session.query(Book).filter_by(isbn=isbn).first()]
        elif author_name is not None or author_id is not None:
            author = get_author(author_id=author_id, author_name=author_name)
            book_list = session.query(Book).filter_by(author=author).all()
        elif title is not None:
            book_list = [session.query(Book).filter_by(title=title).first()]
        elif language is not None:
            book_list = session.query(Book).filter_by(language=language).all()
        elif rating is not None:
            book_list = session.query(Book).filter_by(average_rating=rating).all() #need to be changed
        else:
            book_list = None

        if len(book_list) == 1:
            # Get the first (and only) element
            element = book_list[0]
            # Check if the element is any of the empty types
            if element in (None, '', [], (), {}):
                return None
        return book_list


def delete_reader(email: str) -> bool:
    user = find_users(email=email)
    if user is not None:
        with Session() as session:
            session.delete(user)
            session.commit()
            return True
    return False

def delete_book(isbn: str | None = None,
                author_name: str | None = None,
                author_id: int | None = None,
                title: str | None = None,
                language: str | None = None):
    book_list = search_book(isbn=isbn, author_name=author_name, author_id=author_id, title=title, language=language)
    if book_list[0] is not None:
        with Session() as session:
            for book in book_list:
                session.delete(book)
            session.commit()
        return True
    return False

def add_book_to_database(book: Book):
    if search_book(isbn=book.isbn)[0] is None:
        with Session() as session:
            session.add(book)
            session.commit()
        return True
    return False

def add_librarian(username: str | None = None, email: str | None = None, name: str | None = None):
    user = find_users(username=username, email=email, name=name)
    if user is not None:
        if not user.admin:
            with Session() as session:
                user.admin = True
                session.commit()
            return 1
        else:
            return 0
    return -1

# def borrow_book(reader: models.Reader, copy: Copy):
#     try:
#         borrow = Borrow(reader_username=reader.username, copy=copy, borrow_date=datetime.datetime.now())
#         with Session() as session:
#             borrow.copy.is_borrowed = True
#             session.add(borrow)
#             session.commit()



def get_all_copies():
    with Session() as session:
        return session.query(Copy).all()

def del_copies():
    c = get_all_copies()
    with Session() as session:
        for i in c:
            session.delete(i)
            session.commit()

def set_copies():
    lst = get_all_books()
    with Session() as session:
        for book in lst:
            num = random.randint(1, 5)
            for i in range(num):
                copy = Copy(book=book)
                session.add(copy)
                session.commit()

def get_free_copy(book: Book) -> Copy | None:
    with Session() as session:
        copy = session.query(Copy).filter_by(book=book).filter_by(is_borrowed=False).first()
    return copy

def get_copy_by_isbn(isbn: str):
    book = search_book(isbn=isbn)[0]
    copy = get_free_copy(book)
    return copy

def test():
    lst = get_all_borrows()
    borrow = lst[0]
    print(borrow.copy.is_borrowed)

def get_all_borrows():
    with Session() as session:
        lst = session.query(Borrow).all()
    return lst

def del_borrows():
    lst = get_all_borrows()
    with Session() as session:
        for b in lst:
            session.delete(b)
            session.commit()

def return_book(reader: models.Reader, book: Book):
    lst = get_copies_by_username(reader.username)
    for copy in lst:
        if copy.book.isbn == book.isbn:
            if copy.is_borrowed:
                with Session() as session:
                    borrow = session.query(Borrow).filter_by(copy=copy).first()
                    borrow.return_date = datetime.datetime.now()
                    session.commit()
                    copy.is_borrowed = False
                    session.commit()
                    return True
    return False


if __name__ == '__main__':
   pass
