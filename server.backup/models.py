import json

from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, DateTime, Float
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

from server.config import DATABASE_URL
import datetime

Base = declarative_base()


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
        return f"<Book(isbn={self.isbn}, title={self.title}, author={self.author}, language={self.language})>"


class Copy(Base):
    __tablename__ = 'copies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_isbn = Column(String, ForeignKey('books.isbn'))
    book = relationship('Book', back_populates='copies', lazy='joined')
    borrows = relationship('Borrow', back_populates='copy')
    is_borrowed: bool = False

    def __repr__(self):
        return f"<Copy(id={self.id}, book={self.book})>"


class Reader(Base):
    __tablename__ = 'readers'

    username = Column(String, unique=True)
    email = Column(String, primary_key=True)
    name = Column(String)
    borrows = relationship('Borrow', back_populates='reader')
    password = Column(String)
    admin: bool | None = False

    def __repr__(self):
        return f"<Reader(username={self.username}, email={self.email}, name={self.name}, admin={self.admin})>"


class Borrow(Base):
    __tablename__ = 'borrows'

    id = Column(Integer, primary_key=True, autoincrement=True)
    copy_id = Column(Integer, ForeignKey('copies.id'))
    copy = relationship('Copy', back_populates='borrows', lazy='joined')
    reader_username = Column(String, ForeignKey('readers.username'))
    reader = relationship('Reader', back_populates='borrows', lazy='joined')
    borrow_date = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    return_date = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Borrow(id={self.id}, copy={self.copy}, reader={self.reader}, borrow_date={self.borrow_date}, return_date={self.return_date})>"


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

    readers = [
        {"username": "peter", "email": "peter@parker.com", "name": "Peter Parker", "password": "spiderman"},
        {"username": "tony", "email": "tony@stark", "name": "Tony Stark", "password": "ironman"},
        {"username": "bruce", "email": "bruce@wayne", "name": "Bruce Wayne", "password": "batman"},
    ]

    for current_reader in readers:
        with Session() as session:
            session.add(Reader(username=current_reader["username"], email=current_reader["email"], name=current_reader["name"], password=current_reader["password"]))
            session.commit()

    copies = [
        {"book_isbn": "9780141439556"},
        {"book_isbn": "9780141439556"},
        {"book_isbn": "9780141439556"},
        {"book_isbn": "9780451524935"},
        {"book_isbn": "9780451524935"},
        {"book_isbn": "9780679722769"},
    ]

    for copy in copies:
        with Session() as session:
            session.add(Copy(book_isbn=copy["book_isbn"]))
            session.commit()

    borrows = [
        {"copy_id": 1, "reader_username": "peter", "borrow_date": datetime(2021, 1, 1), "return_date": datetime(2021, 1, 15)},
        {"copy_id": 2, "reader_username": "tony", "borrow_date": datetime(2021, 1, 2), "return_date": datetime(2021, 1, 16)},
        {"copy_id": 3, "reader_username": "bruce", "borrow_date": datetime(2021, 1, 3), "return_date": datetime(2021, 1, 17)},
        {"copy_id": 4, "reader_username": "peter", "borrow_date": datetime(2021, 1, 4), "return_date": datetime(2021, 1, 18)},
        {"copy_id": 5, "reader_username": "tony", "borrow_date": datetime(2021, 1, 5), "return_date": datetime(2021, 1, 19)},
        {"copy_id": 6, "reader_username": "bruce", "borrow_date": datetime(2021, 1, 6), "return_date": datetime(2021, 1, 20)},
    ]

    for borrow in borrows:
        with Session() as session:
            session.add(Borrow(copy_id=borrow["copy_id"], reader_username=borrow["reader_username"], borrow_date=borrow["borrow_date"], return_date=borrow["return_date"]))
            session.commit()

