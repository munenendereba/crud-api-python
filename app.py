from multiprocessing import connection
from fastapi import FastAPI
import sqlite3

from book import BookCreate

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to crud ala nikii"}


@app.post("/books/")
def create_book_endpoint(book: BookCreate):
    book_id = create_book(book)
    return {"id": book_id, **book.dict()}


@app.get("/books/")
def get_books_endpoint():
    return get_books()


def create_connection():
    connection = sqlite3.connect("books.db")
    return connection


def create_book_table():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
                  CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL
                   )                  
                   """
    )

    connection.commit()
    connection.close()


def create_book(book: BookCreate):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO books (title, author) VALUES (?, ?)", (book.title, book.author)
    )
    connection.commit()
    connection.close()


def get_books():
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM books")

    allBooks = cursor.fetchall()

    return allBooks


create_book_table()
