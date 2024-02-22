import sqlite3
from sqlite3 import Error
import init_library

DATABASE = r"/Users/assafbendor/PycharmProjects/webProject/db/ldb.db"


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_book(book):
    conn = create_connection(DATABASE)
    sql = '''
    INSERT INTO books(id, name, author, picture, available) VALUES(?, ?, ?, ?, ?)
    '''
    cur = conn.cursor()
    cur.execute(sql, book)
    conn.commit()
    conn.close()
    return cur.lastrowid


def create_user(user):
    print(user)
    conn = create_connection(DATABASE)
    sql = '''
    INSERT INTO users(username, password, name) VALUES(?, ?, ?)
    '''
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()
    conn.close()
    return cur.lastrowid

def update_book(conn, book): # id last parameter
    sql = ''' UPDATE books
                  SET name = ? ,
                      author = ? ,
                      picture = ? ,
                      available = ? ,
                      username = ?
                WHERE id = ?'''

    cur = conn.cursor()
    cur.execute(sql, book)
    conn.commit()

def select_all_books(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM books")

    rows = cur.fetchall()

    for row in rows:
        print(row)

def select_all_users(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")

    rows = cur.fetchall()

    for row in rows:
        print(row)

def delete_book(conn, id):
    sql = 'DELETE FROM books WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()
def main():

    books_table = """
    CREATE TABLE IF NOT EXISTS books(
    id integer PRIMARY KEY,
    name text NOT NULL,
    author text NOT NULL,
    picture text,
    available timestamp,
    username text,
    FOREIGN KEY (username) REFERENCES users_table (username)
    );"""

    users_table = """
    CREATE TABLE IF NOT EXISTS users(
    username text PRIMARY KEY,
    password text NOT NULL,
    email text
    );"""
    ''
    # create a database connection
    conn = create_connection(DATABASE)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, books_table)

        # create tasks table
        create_table(conn, users_table)
    else:
        print("Error! cannot create the database connection.")

    def init_list():
        with conn:
            book_list = init_library.main()
            for book in book_list:
                create_book(conn, book)

    select_all_users(conn)

if __name__ == '__main__':
    main()

