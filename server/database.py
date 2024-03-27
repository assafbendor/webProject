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


def add_reader_to_database(username: str, email: str, name: str, password: str) -> bool:
    reader = models.Reader(username=username, email=email, name=name, password=api.get_password_hash(password))
    if find_users(email=email) is not None:
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
    # print(add_reader_to_database(username="Assaf", email="asaf.bendor2@gmail.com", name="Assaf Ben Dor", password="assaf6656ben"))
    # print(find_users(email="asaf.bendor2@gmail.com"))
    # print(delete_reader(email="asaf.bendor2@gmail.com"))


