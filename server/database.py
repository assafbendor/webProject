from typing import List, Type

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from server.config import DATABASE_URL
from server.models import Book, Copy, Borrow

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
    print(get_copies_by_username('peter'))
