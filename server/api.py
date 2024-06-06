import random
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

import database
import models

import sched
import time

import mail

import re
SECRET_KEY = "0ae9bd5bf97167908547da34d48b18701aa0307e84c88f5a2181139e4d5ffb02"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

scheduler = sched.scheduler(time.time, time.sleep)

class PasswordChangeRequest(BaseModel):
    new_password: str
    new_password_verify: str

class Token(BaseModel):
    access_token: str
    token_type: str
    username: str
    is_admin: bool

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username: str):
    user = database.find_user(username=username)
    return user


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def check_user(current_user: models.Reader, username: str | None = None, email: str | None = None,
               name: str | None = None):
    reply = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User is not permitted"
    )
    if current_user.username is not None:
        if current_user.username != username:
            raise reply
    elif current_user.email is not None:
        if current_user.email != email:
            raise reply
    elif current_user.name is not None:
        if current_user.name != name:
            raise reply

    else:
        raise reply


def check_if_user_allowed(user: models.Reader):
    if not user.admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not admin"
        )


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    expires_delta = expires_delta or timedelta(minutes=15)
    expire = datetime.now(timezone.utc) + expires_delta

    to_encode["exp"] = expire

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def is_valid_password(password):
    # Check length
    if len(password) < 8:
        return False

    # Check for at least one number
    if not re.search(r'\d', password):
        return False

    # Check for at least one symbol
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False

    # If all checks passed
    return True

def send_reserve_mail(waiting: models.Waiting):
    email = waiting.reader.email
    subject = "Your book is now available!"
    text = (f"Hello {waiting.reader.username}, \n The book you ordered, {waiting.book.title}, is now available at the "
            f"library for 24 hours!")
    mail.send_email(to_addr=email, sub=subject, text=text)

def check_waiting():
    database.update_waiting()
    lst = database.get_all_active_waiting()
    for w in lst:
        c = database.get_free_copy(book=w.book)
        if c is not None and c.ordered_by_email is None:
            database.save_copy(copy=c, reader=w.reader)
            send_reserve_mail(waiting=w)


def schedule_check_waiting(sc):
    check_waiting()
    # Schedule the function to be called again in 60 seconds
    scheduler.enter(60, 1, schedule_check_waiting, (sc,))



async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload["username"]
    except (JWTError, KeyError):
        raise credentials_exception

    user = get_user(username=username)
    if user is None:
        raise credentials_exception
    return user


@app.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"username": user.username}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer", username=user.username, is_admin=user.admin)


@app.post("/sign_up")
async def add_reader_to_database(username: str, email: str, name: str, password: str):
    if is_valid_password(password) is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters and contain at least one number and one symbol"
        )
    try:
        result = database.add_reader_to_database(
            models.Reader(username=username, email=email, name=name, password=get_password_hash(password)))
    except:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="One or more of the identification elements is in use"
        )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="One or more of the identification elements is in use"
        )
    return result


@app.get("/search_books")
async def search_books(current_user: Annotated[models.Reader, Depends(get_current_user)],
                       isbn: str | None = None,
                       author_name: str | None = None,
                       author_id: int | None = None,
                       title: str | None = None,
                       language: str | None = None):
    book_list = database.search_book(isbn=isbn,
                                     author_name=author_name,
                                     author_id=author_id,
                                     title=title,
                                     language=language)
    if book_list is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unknown Parameter"
        )
    return book_list


# @app.post("/addbook")
# async def add_book_to_database(isbn: int, title: str, author_name: str)

@app.get("/book_list")
async def return_book_list(username: str, current_user: Annotated[models.Reader, Depends(get_current_user)]):

    if username != current_user.username:
        check_if_user_allowed(current_user)

    return database.get_borrows_by_username(username=username)


@app.get("/books")
async def get_all_books(current_user: Annotated[models.Reader, Depends(get_current_user)]):
    print("in books")
    return database.get_all_books()


@app.post("/borrow_book")
async def borrow_book(current_user: Annotated[models.Reader, Depends(get_current_user)],
                      book_isbn: str, username: str):
    check_if_user_allowed(current_user)
    book = database.search_book(isbn=book_isbn)
    reader = database.find_user(username=username)
    if len(book) == 0:
        response = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book is not found"
        )

    elif len(database.get_books_in_late(reader=reader)) > 0:
        response = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Reader has to return old books first"
        )
    elif database.get_number_of_copies_by_user(reader=reader) > 3:
        response = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Reader has more then 3 books"
        )
    else:
        copy = database.get_free_copy(book[0])
        if copy is None:
            response = HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="All copies are borrowed"
            )
        elif copy.ordered_by_email is not None and copy.ordered_by_email is not reader:
            response = HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="All copies are borrowed"
            )
        else:
            database.borrow_book(reader=reader, copy=copy)

            response = HTTPException(
                status_code=status.HTTP_200_OK,
                detail="book was borrowed successfully"
            )
    raise response


@app.post("/return_book")
async def return_book(current_user: Annotated[models.Reader, Depends(get_current_user)], book_isbn: str,
                      username: str):
    check_if_user_allowed(current_user)
    reader = database.find_user(username=username)
    book = database.search_book(isbn=book_isbn)[0]
    if book is None:
        response = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book was not found"
        )
    else:
        if not database.return_book(reader=reader, book=book):
            response = HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book is not borrowed by the user"
            )
        else:
            response = HTTPException(
                status_code=status.HTTP_200_OK,
                detail="Book was returned successfully"
            )
    raise response


@app.get("/highest_rating_books")
async def return_most_high_score_books(current_user: Annotated[models.Reader, Depends(get_current_user)],
                                       number_of_books: int):
    if number_of_books < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Value mast be positive"
        )
    else:
        return database.return_high_score_books(number_of_books=number_of_books)


@app.get("/search_books_by_anything")
async def search_books_by_anything(current_user: Annotated[models.Reader, Depends(get_current_user)], query_str: str):
    return [database.search_book(isbn=isbn)[0] for isbn in database.search_books_by_anything(query_str)]

@app.get("/get_readers")
async def get_readers(current_user: Annotated[models.Reader, Depends(get_current_user)]):
    check_if_user_allowed(user=current_user)
    readers = database.get_readers(admin=False)
    return readers

@app.post("/forgot_password")
async def forgot_password(email: str):
    user = database.find_user(email=email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email is not registered"
        )
    code = random.randint(1000, 9999)
    result = mail.send_email(to_addr=email, sub="Reset Your Password", text=f"your code is {code}. \n It will be expired in 3 "
                                                                   f"minutes from now.")
    if result is True:
        database.add_code(code=code, email=email)
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Email sent successfully!"
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result
        )

@app.post("/verify_code")
async def verify_code(code: int, email: str, request: PasswordChangeRequest):
    result = database.varify_code(email=email, code=code)
    if result is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email or code are not correct"
        )
    if request.new_password != request.new_password_verify:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )

    user = database.find_user(email=email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email or code are not correct",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if is_valid_password(request.new_password) is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters and contain at least one number and one symbol"
        )
    password_changed = database.change_password(email=email, new_password=request.new_password)
    if password_changed is False:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user"
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"username": user.username}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer", username=user.username, is_admin=user.admin)

@app.post("/change_password")
async def change_password(current_user: Annotated[models.Reader, Depends(get_current_user)],
                          request: PasswordChangeRequest):
    if is_valid_password(request.new_password) is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters and contain at least one number and one symbol"
        )
    if request.new_password != request.new_password_verify:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )

    database.change_password(email=current_user.email, new_password=request.new_password)

@app.post("/reserve")
async def reserve(current_user: Annotated[models.Reader, Depends(get_current_user)], username: str, isbn: str):
    reader = database.find_user(username=username)
    book = database.search_book(isbn=isbn)
    if reader is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )
    if len(book) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book does not exist"
        )
    result = database.add_waiting(reader=reader, book=book[0])
    if result is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Something went wrong"
        )

@app.get("/reservations")
async def reservations(current_user: Annotated[models.Reader, Depends(get_current_user)], username: str):
    user = database.find_user(username=username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )
    if current_user.admin is True:
        return database.get_waiting_by_reader(reader=user)
    else:
        return database.get_waiting_by_reader(reader=current_user)

@app.get("/history")
async def get_history(current_user: Annotated[models.Reader, Depends(get_current_user)], username: str):
    reader = database.find_user(username=username)
    if reader is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exists"
        )
    if current_user.username != username:
        check_if_user_allowed(user=current_user)

    return database.get_borrow_by_user(reader=reader)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
    scheduler.enter(60, 1, schedule_check_waiting, (scheduler,))
    scheduler.run()