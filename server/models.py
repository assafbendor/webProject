from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, DateTime
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

from server.config import DATABASE_URL

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
    author_id = Column(String, ForeignKey('authors.id'))
    author = relationship('Author', back_populates='books', lazy='joined')
    copies = relationship('Copy', back_populates='book')

    def __repr__(self):
        return f"<Book(isbn={self.isbn}, title={self.title}, author={self.author})>"


class Copy(Base):
    __tablename__ = 'copies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_isbn = Column(String, ForeignKey('books.isbn'))
    book = relationship('Book', back_populates='copies', lazy='joined')
    borrows = relationship('Borrow', back_populates='copy')

    def __repr__(self):
        return f"<Copy(id={self.id}, book={self.book})>"


class Reader(Base):
    __tablename__ = 'readers'

    username = Column(String, unique=True)
    email = Column(String, primary_key=True)
    name = Column(String)
    borrows = relationship('Borrow', back_populates='reader')
    password = Column(String)

    def __repr__(self):
        return f"<Reader(username={self.username}, email={self.email}, name={self.name})>"


class Borrow(Base):
    __tablename__ = 'borrows'

    id = Column(Integer, primary_key=True, autoincrement=True)
    copy_id = Column(Integer, ForeignKey('copies.id'))
    copy = relationship('Copy', back_populates='borrows', lazy='joined')
    reader_username = Column(String, ForeignKey('readers.username'))
    reader = relationship('Reader', back_populates='borrows', lazy='joined')
    borrow_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Borrow(id={self.id}, copy={self.copy}, reader={self.reader}, borrow_date={self.borrow_date}, return_date={self.return_date})>"


if __name__ == '__main__':
    engine = create_engine(DATABASE_URL)

    # Create the tables
    Base.metadata.create_all(engine)

    # fill the tables with random, but real data

    Session = sessionmaker(bind=engine)

    books = [
        {"isbn": "9780141439556", "title": "Pride and Prejudice", "author": "Jane Austen"},
        {"isbn": "9780451524935", "title": "1984", "author": "George Orwell"},
        {"isbn": "9780679722769", "title": "Crime and Punishment", "author": "Fyodor Dostoevsky"},
        {"isbn": "9780743482752", "title": "Hamlet", "author": "William Shakespeare"},
        {"isbn": "9780061120091", "title": "One Hundred Years of Solitude", "author": "Gabriel García Márquez"},
        {"isbn": "9780143035008", "title": "Anna Karenina", "author": "Lev Tolstoy"},
        {"isbn": "9780140449112", "title": "The Odyssey", "author": "Homer"},
        {"isbn": "9780679720208", "title": "The Stranger", "author": "Albert Camus"},
        {"isbn": "9780679721755", "title": "The Brothers Karamazov", "author": "Fyodor Dostoevsky"},
        {"isbn": "9780679723162", "title": "Lolita", "author": "Vladimir Nabokov"},
        {"isbn": "9780141439563", "title": "Great Expectations", "author": "Charles Dickens"},
        {"isbn": "9780684801223", "title": "The great Gatsby", "author": "F. Scott Fitzgerald"},
    ]

    authors = set()
    for book in books:
        authors.add(book["author"])

    for author in authors:
        with Session() as session:
            session.add(Author(name=author))
            session.commit()

    for book in books:
        with Session() as session:
            session.add(Book(isbn=book["isbn"], title=book["title"], author=session.query(Author).filter_by(name=book["author"]).first()))
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


