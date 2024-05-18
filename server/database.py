import datetime
import random
import time
from typing import Type

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser, FuzzyTermPlugin

import api
import models
from server.config import DATABASE_URL
from server.models import Book, Copy, Borrow, Reader, Code

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

def get_readers(admin: bool | None = None):
    with Session() as session:
        if admin is not None:
            return session.query(Reader).filter_by(admin=admin).all()

def find_user(username: str | None = None, email: str | None = None, name: str | None = None) -> Reader | None:
    with Session() as session:
        if email is not None:
            user = session.query(Reader).filter_by(email=email).first()
        elif username is not None:
            user = session.query(Reader).filter_by(username=username).first()
        elif name is not None:
            user = session.query(Reader).filter_by(name=name).first()
        else:
            user = None
    return user


def add_reader_to_database(reader: Reader) -> bool:
    if find_user(email=reader.email, username=reader.username, name=reader.name) is None:
        with Session() as session:
            session.add(reader)
            session.commit()
            return True
    return False


def change_password(email: str, new_password: str) -> bool:
    if find_user(email=email) is not None:
        with Session() as session:
            user = session.query(Reader).filter_by(email=email).first()
            user.password = api.get_password_hash(password=new_password)
            session.commit()
            return True
    return False


def email_to_username(email: str):
    user = find_user(email)
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
    user = find_user(email=email)
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
    borrow = Borrow(reader_username=reader.username, copy=copy, borrow_date=datetime.datetime.now(),
                    due_date=datetime.datetime.now() + datetime.timedelta(days=30))
    with Session() as session:
        copy.is_borrowed = True
        session.commit()
        session.add(borrow)
        session.commit()
        print(borrow)


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
                    borrow = session.query(Borrow).filter_by(copy=copy, return_date=None).first()
                    borrow.return_date = datetime.datetime.now()
                    session.commit()
                    borrow.copy.is_borrowed = False
                    session.commit()
                    print(borrow)
                    return True
    return False


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


def get_books_in_late(reader: Reader):
    books = []
    with Session() as session:
        books_borrowed_by_reader = session.query(Borrow).filter_by(reader=reader).all()
        for book in books_borrowed_by_reader:
            if book.return_date is None:
                delta_time = datetime.datetime.now() - book.borrow_date
                if delta_time.days > 30:
                    books.append(book)
    return books

def get_number_of_copies_by_user(reader: Reader):
    with Session() as session:
        num = len(session.query(Borrow).filter_by(return_date=None).filter_by(reader=reader).all())
    return num

def get_num_of_free_copies(book: Book):
    with Session() as session:
        return len(session.query(Copy).filter_by(book=book).filter_by(is_borrowed=False).all())

def get_all_copies():
    with Session() as session:
        return session.query(Copy).all()

def del_copies():
    with Session() as session:
        for copy in get_all_copies():
            session.delete(copy)
            session.commit()

def set_copies():
    books = get_all_books()
    with Session() as session:
        for book in books:
            n = random.randint(1, 5)
            for x in range(n):
                c = Copy(book=book)
                session.add(c)
                session.commit()

def get_all_codes():
    with Session() as session:
        return session.query(Code).all()

def add_code(code: int, email: str):
    with Session() as session:
        c = Code(number=code, email=email, created_at=datetime.datetime.now())
        session.add(c)
        session.commit()

def get_borrows_by_username(username: str):
    with Session() as session:
        return session.query(Borrow).filter_by(reader_username=username, return_date=None).all()

def varify_code(email: str, code: int):
    with Session() as session:
        result = session.query(Code).filter_by(email=email).order_by(Code.created_at.desc()).limit(1).first()
        if result is None:
            return False
        return result.number == code

if __name__ == '__main__':
    # Example: Search fo r books
    # print(search_books_by_anything('fun'))
    #asyncio.run(api.add_reader_to_database(username="admin", password="admin", email="admin@gmail.com", name="admin"))
    # del_copies()
    # set_copies()
    # del_borrows()
    # print(add_code(code=12357, email="asaf.bendor2@gmail.com"))
    # print(get_all_codes())
    # print(varify_code(email="asaf.bendor2@gmail.com", code=1235))
    # print(change_password(email="asaf.bendor2@gmail.com", new_password="12345678!"))
    pass

