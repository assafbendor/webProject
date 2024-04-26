from typing import List, Type

from sqlalchemy import create_engine, DateTime
from sqlalchemy.orm import sessionmaker

from server.config import DATABASE_URL
from server.models import Book, Copy, Borrow

import api
import models
import random

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

def borrow_book(reader: models.Reader, book: Book):
    copy = get_free_copy(book)
    if copy is None:
        return False
    borrow = Borrow(copy=copy, reader=reader)
    with Session() as session:
        copy.is_borrowed = True
        session.add(borrow)
        session.commit()

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
        print(copy)
    return copy

def get_copy_by_isbn(isbn: str):
    book = search_book(isbn=isbn)[0]
    copy = get_free_copy(book)
    return copy

def test():
    book = search_book(isbn="9784351510613")
    copy = get_free_copy(book[0])
    reader = find_users(username="peter")
    borrow = Borrow(copy=copy, reader_username=reader.username)
    with Session() as session:
        session.add(borrow)
        session.commit()

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

if __name__ == '__main__':


    # books = get_all_books()
    # print(books[0].copies)
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
    # print(delete_book(isbn=12345678))
    # print(return_all_books())
    # print(get_all_books())
    # print(get_all_users())
    #print(get_all_users())
    #print(get_copies_by_username("tony"))
    # del_copies()
    # set_copies()
    # print(get_all_copies())
    # print(get_all_books())
    # print(get_copy_by_isbn("9788004605639"))
    # test()
    # del_borrows()
    # test()
    # print(get_all_borrows())
    print(search_book(isbn="9788004605639"))
    print(search_book(title="The Grapes of Wrath"))
    print(search_book(author_id=60))
    print(search_book(author_name="John Steinbeck"))
    print(search_book(language="English"))

