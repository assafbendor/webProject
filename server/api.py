from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

import database
import models
SECRET_KEY = "0ae9bd5bf97167908547da34d48b18701aa0307e84c88f5a2181139e4d5ffb02"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Token(BaseModel):
    access_token: str
    token_type: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username: str):
    user = database.find_user_by_username(username)
    return user


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return None
    if not verify_password(password, get_password_hash(user.password)):
        return None
    return user

def check_user(current_user: models.Reader, username: str):
    if current_user.username != username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not permitted"
        )

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    expires_delta = expires_delta or timedelta(minutes=15)
    expire = datetime.now(timezone.utc) + expires_delta

    to_encode["exp"] = expire

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload["username"]
    except JWTError | KeyError:
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
    return Token(access_token=access_token, token_type="bearer")


@app.post("/sign_up")
async def add_reader_to_database(username: str, email: str, name: str, password: str):
    result = database.add_reader_to_database(models.Reader(username=username, email=email, name=name, password=password))
    if not result:
        raise HTTPException(
            status_code=status.HTTP_226_IM_USED,
            detail="One or more of the identification is in use"
        )
    return result

@app.get("users/if_exist/")
async def check_if_user_exists_by_email(email: str):
    return database.find_users(email=email) is not None

@app.get("/search_books")
async def search_books(isbn: str | None = None, author_name: str | None = None, author_id: int | None = None, title: str | None = None):
    book_list = database.search_book(isbn=isbn, author_name=author_name, author_id=author_id, title=title)
    if book_list is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unknown Parameter"
        )
    return book_list

#@app.post("/addbook")
# async def add_book_to_database(isbn: int, title: str, author_name: str)

@app.get("/book_list")
async def return_book_list(username: str, current_user: Annotated[models.Reader, Depends(get_current_user)]):
    check_user(current_user, username)

    return database.get_copies_by_username(username=username)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
