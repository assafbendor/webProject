import datetime
import json

from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, DateTime, Float, Boolean, event
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

from server.config import DATABASE_URL

Base = declarative_base()

import os
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
from whoosh.index import open_dir
from whoosh.writing import AsyncWriter

schema = Schema(title=TEXT(stored=True, field_boost=2.0), author=TEXT(stored=True, field_boost=2.0),
                description=TEXT(stored=False),
                isbn=ID(stored=True))

if not os.path.exists("indexdir"):
    os.mkdir("indexdir")
    index = create_in("indexdir", schema)
else:
    index = open_dir("indexdir")


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    books = relationship('Book', back_populates='author')

    def __repr__(self):
        return f"<Author(id={self.id}, name={self.name})>"


class Book(Base):
    __tablename__ = 'books'

    isbn = Column(String, primary_key=True)
    title = Column(String)
    language = Column(String)
    average_rating = Column(Float)
    cover_image_filename = Column(String)
    description = Column(String)
    pages = Column(Integer)
    author_id = Column(String, ForeignKey('authors.id'))
    author = relationship('Author', back_populates='books', lazy='joined')
    copies = relationship('Copy', back_populates='book')

    def __repr__(self):
        return f"<Book(isbn={self.isbn}, title={self.title}, author={self.author}, language={self.language}, rating={self.average_rating})>"


def add_book_to_index(mapper, connection, target: Book):
    ix = open_dir("indexdir")
    writer = AsyncWriter(ix)
    writer.add_document(title=target.title, author=target.author.name, description=target.description,
                        isbn=str(target.isbn))
    writer.commit()


def remove_book_from_index(mapper, connection, target: Book):
    ix = open_dir("indexdir")
    writer = ix.writer()
    writer.delete_by_term("isbn", str(target.isbn))
    writer.commit()


def update_book_in_index(mapper, connection, target: Book):
    remove_book_from_index(mapper, connection, target)
    add_book_to_index(mapper, connection, target)


event.listen(Book, 'after_insert', add_book_to_index)
event.listen(Book, "after_delete", remove_book_from_index)
event.listen(Book, "after_update", update_book_in_index)


class Copy(Base):
    __tablename__ = 'copies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_isbn = Column(String, ForeignKey('books.isbn'))
    book = relationship('Book', back_populates='copies', lazy='joined')
    borrows = relationship('Borrow', back_populates='copy')
    is_borrowed = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Copy(id={self.id}, book={self.book}, is_borrowed={self.is_borrowed})>"


class Reader(Base):
    __tablename__ = 'readers'

    username = Column(String, unique=True)
    email = Column(String, primary_key=True)
    name = Column(String)
    borrows = relationship('Borrow', back_populates='reader')
    password = Column(String)
    admin = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Reader(username={self.username}, email={self.email}, name={self.name}, admin={self.admin})>"


class Borrow(Base):
    __tablename__ = 'borrows'

    id = Column(Integer, primary_key=True, autoincrement=True)
    copy_id = Column(Integer, ForeignKey('copies.id'))
    copy = relationship('Copy', back_populates='borrows', lazy='joined')
    reader_username = Column(String, ForeignKey('readers.username'))
    reader = relationship('Reader', back_populates='borrows', lazy='joined')
    borrow_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime, nullable=True)
    due_date = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"<Borrow(id={self.id}, copy={self.copy}, reader={self.reader}, borrow_date={self.borrow_date}, Due_date={self.due_date}, return_date={self.return_date})>"

class Code(Base):
    __tablename__ = 'codes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(Integer)
    email = Column(String)
    created_at = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"<Code(id={self.id}, Number={self.number}, Email={self.email}, Created_at={self.created_at}"

if __name__ == '__main__':
    engine = create_engine(DATABASE_URL)

    # Create the tables
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)

    with open('books.json', 'r') as file:
        books = json.load(file)

    authors = set()
    for book in books:
        authors.add(book["author"])

    for author in authors:
        with Session() as session:
            session.add(Author(name=author))
            session.commit()

    for book in books:
        with Session() as session:
            session.add(Book(isbn=book["isbn"],
                             title=book["title"],
                             author=session.query(Author).filter_by(name=book["author"]).first(),
                             language=book["language"],
                             cover_image_filename=book["cover_image_filename"],
                             description=book["description"],
                             average_rating=book["average_rating"],
                             pages=book["pages"]))
            session.commit()

   #  readers = [
   #      {"username": "peter", "email": "peter@parker.com", "name": "Peter Parker", "password": "spiderman"},
   #      {"username": "tony", "email": "tony@stark", "name": "Tony Stark", "password": "ironman"},
   #      {"username": "bruce", "email": "bruce@wayne", "name": "Bruce Wayne", "password": "batman"},
   #  ]
#
   #  for current_reader in readers:
   #      with Session() as session:
   #          session.add(
   #              Reader(username=current_reader["username"], email=current_reader["email"], name=current_reader["name"],
   #                     password=current_reader["password"]))
   #          session.commit()

  #  copies = [
  #      {"book_isbn": "9780141439556"},
  #      {"book_isbn": "9780141439556"},
  #      {"book_isbn": "9780141439556"},
  #      {"book_isbn": "9780451524935"},
  #      {"book_isbn": "9780451524935"},
  #      {"book_isbn": "9780679722769"},
  #  ]

  #  for copy in copies:
  #      with Session() as session:
  #          session.add(Copy(book_isbn=copy["book_isbn"]))
  #          session.commit()

  #  borrows = [
  #      {"copy_id": 1, "reader_username": "peter", "borrow_date": datetime.datetime.now(), "return_date": None},
  #      {"copy_id": 2, "reader_username": "tony", "borrow_date": datetime.datetime.now(), "return_date": None},
  #      {"copy_id": 3, "reader_username": "bruce", "borrow_date": datetime.datetime.now(), "return_date": None},
  #      {"copy_id": 4, "reader_username": "peter", "borrow_date": datetime.datetime.now(), "return_date": None},
  #      {"copy_id": 5, "reader_username": "tony", "borrow_date": datetime.datetime.now(), "return_date": None},
  #      {"copy_id": 6, "reader_username": "bruce", "borrow_date": datetime.datetime.now(), "return_date": None},
  #  ]

  #  for borrow in borrows:
  #      with Session() as session:
  #          session.add(Borrow(copy_id=borrow["copy_id"], reader_username=borrow["reader_username"],
  #                             borrow_date=borrow["borrow_date"], return_date=borrow["return_date"]))
  #          session.commit()
