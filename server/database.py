import datetime
from typing import Type

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser, FuzzyTermPlugin

import api
import models
from server.config import DATABASE_URL
from server.models import Book, Copy, Borrow, Reader

engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)


def get_all_books() -> list[Type[Book]]:
    with Session() as session:
        book_list = session.query(Book).all()
        return book_list


def get_all_users():
    with Session() as session:
        users = session.query(Reader).all()
    return users


def get_copies_by_username(username: str):
    with Session() as session:
        borrows = session.query(Borrow).filter_by(reader_username=username, return_date=None).all()
        return [borrow.copy for borrow in borrows]


def find_users(username: str | None = None, email: str | None = None, name: str | None = None) -> Reader | None:
    with Session() as session:
        if email is not None:
            user = session.query(Reader).filter_by(email=email).first()
        elif username is not None:
            user = session.query(Reader).filter_by(username=username).first()
        elif name is not None:
            user = session.query(Reader).filter_by(name=name)
        else:
            user = None
    return user


def add_reader_to_database(reader: Reader) -> bool:
    if find_users(email=reader.email, username=reader.username, name=reader.name) is None:
        with Session() as session:
            session.add(reader)
            session.commit()
            return True
    return False


def change_password(email: str, new_password) -> bool:
    if find_users(email=email) is not None:
        with Session() as session:
            user = session.query(Reader).filter_by(email=email).first()
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
                title: str | None = None) -> list[Book] | None:
    with Session() as session:
        books = session.query(Book).filter_by(isbn=isbn).all()
        return books


def delete_reader(email: str) -> bool:
    user = find_users(email=email)
    if user is not None:
        with Session() as session:
            session.delete(user)
            session.commit()
            return True
    return False


def delete_book(isbn: str) -> bool:
    with Session() as session:
        result = session.query(Book).filter_by(isbn=isbn).delete() == 1
        session.commit()
        return result


def add_book_to_database(book: Book):
    if search_book(isbn=book.isbn)[0] is None:
        with Session() as session:
            session.add(book)
            session.commit()
        return True
    return False


def borrow_book(reader: Reader, copy: Copy):
    borrow = Borrow(reader_username=reader.username, copy=copy, borrow_date=datetime.datetime.now())
    with Session() as session:
        copy.is_borrowed = True
        session.add(borrow)
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


def return_book(reader: Reader, book: Book):
    lst = get_copies_by_username(reader.username)
    for copy in lst:
        if copy.book.isbn == book.isbn:
            if copy.is_borrowed:
                with Session() as session:
                    borrow = session.query(Borrow).filter_by(copy=copy).first()
                    borrow.return_date = datetime.datetime.now()
                    session.commit()
                    borrow.copy.is_borrowed = False
                    session.commit()
                    return True
    return False


def add_admin(reader: Reader):
    with Session() as session:
        reader.admin = True
        session.commit()


def return_high_score_books(number_of_books: int):
    with Session() as session:
        return session.query(Book).order_by(Book.average_rating.desc()).limit(number_of_books).all()


def search_books_by_anything(query_str: str):
    ix = open_dir("indexdir")
    with ix.searcher() as searcher:
        parser = MultifieldParser(["title", "author", "description"], ix.schema)
        parser.add_plugin(FuzzyTermPlugin())
        fuzzy_query_string = " ".join(f"{word}~2" for word in query_str.split())
        query = parser.parse(fuzzy_query_string)
        results = searcher.search(query)
        return [result["isbn"] for result in results]


if __name__ == '__main__':
    # Example: Search fo r books
    print(search_books_by_anything('fun'))
