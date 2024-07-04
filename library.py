import sqlite3
import argparse
from datetime import datetime, timedelta

def initialize_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            genre TEXT NOT NULL,
            status TEXT NOT NULL,
            due_date DATE
        )
    ''')
    conn.commit()
    conn.close()

def add_book(title, author, genre, status='available', due_date=None):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO books (title, author, genre, status, due_date)
        VALUES (?, ?, ?, ?, ?)
    ''', (title, author, genre, status, due_date))
    conn.commit()
    conn.close()

def update_book(book_id, title=None, author=None, genre=None, status=None, due_date=None):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    fields = []
    values = []
    if title:
        fields.append("title = ?")
        values.append(title)
    if author:
        fields.append("author = ?")
        values.append(author)
    if genre:
        fields.append("genre = ?")
        values.append(genre)
    if status:
        fields.append("status = ?")
        values.append(status)
    if due_date:
        fields.append("due_date = ?")
        values.append(due_date)
    values.append(book_id)
    if fields:
        cursor.execute(f'''
            UPDATE books
            SET {', '.join(fields)}
            WHERE id = ?
        ''', values)
        conn.commit()
    conn.close()

def delete_book(book_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM books
        WHERE id = ?
    ''', (book_id,))
    conn.commit()
    conn.close()

def get_books(sort_by=None, filter_by=None, filter_value=None):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query = 'SELECT * FROM books'
    params = []
    if filter_by and filter_value:
        query += f' WHERE {filter_by} LIKE ?'
        params.append(f'%{filter_value}%')
    if sort_by:
        query += f' ORDER BY {sort_by}'
    cursor.execute(query, params)
    books = cursor.fetchall()
    conn.close()
    return books

def search_books(field, value):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(f'''
        SELECT * FROM books
        WHERE {field} LIKE ?
    ''', ('%' + value + '%',))
    books = cursor.fetchall()
    conn.close()
    return books

def borrow_book(book_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT status FROM books
        WHERE id = ?
    ''', (book_id,))
    status = cursor.fetchone()
    if status and status[0] == 'available':
        due_date = (datetime.now() + timedelta(days=14)).date()
        cursor.execute('''
            UPDATE books
            SET status = 'borrowed', due_date = ?
            WHERE id = ?
        ''', (due_date, book_id))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

def return_book(book_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT status FROM books
        WHERE id = ?
    ''', (book_id,))
    status = cursor.fetchone()
    if status and status[0] == 'borrowed':
        cursor.execute('''
            UPDATE books
            SET status = 'available', due_date = NULL
            WHERE id = ?
        ''', (book_id,))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

def generate_report(report_type):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    if report_type == 'borrowed':
        cursor.execute('''
            SELECT * FROM books
            WHERE status = 'borrowed'
        ''')
    elif report_type == 'overdue':
        today = datetime.now().date()
        cursor.execute('''
            SELECT * FROM books
            WHERE status = 'borrowed' AND due_date < ?
        ''', (today,))
    else:
        conn.close()
        return []
    books = cursor.fetchall()
    conn.close()
    return books

def main():
    parser = argparse.ArgumentParser(description='Library Management System')
    subparsers = parser.add_subparsers(dest='command')

    # Add book
    add_parser = subparsers.add_parser('add', help='Add a new book')
    add_parser.add_argument('title', type=str, help='Title of the book')
    add_parser.add_argument('author', type=str, help='Author of the book')
    add_parser.add_argument('genre', type=str, help='Genre of the book')
    
    # Update book
    update_parser = subparsers.add_parser('update', help='Update a book')
    update_parser.add_argument('book_id', type=int, help='ID of the book')
    update_parser.add_argument('--title', type=str, help='Title of the book')
    update_parser.add_argument('--author', type=str, help='Author of the book')
    update_parser.add_argument('--genre', type=str, help='Genre of the book')
    update_parser.add_argument('--status', type=str, choices=['available', 'borrowed'], help='Status of the book')

    # Delete book
    delete_parser = subparsers.add_parser('delete', help='Delete a book')
    delete_parser.add_argument('book_id', type=int, help='ID of the book')
    
    # List books
    list_parser = subparsers.add_parser('list', help='List all books')
    list_parser.add_argument('--sort_by', type=str, choices=['title', 'author', 'genre', 'status'], help='Field to sort by')
    list_parser.add_argument('--filter_by', type=str, choices=['title', 'author', 'genre', 'status'], help='Field to filter by')
    list_parser.add_argument('--filter_value', type=str, help='Value to filter by')

    # Search books
    search_parser = subparsers.add_parser('search', help='Search for books')
    search_parser.add_argument('field', choices=['title', 'author', 'genre'], help='Field to search by')
    search_parser.add_argument('value', type=str, help='Value to search for')
    
    # Borrow book
    borrow_parser = subparsers.add_parser('borrow', help='Borrow a book')
    borrow_parser.add_argument('book_id', type=int, help='ID of the book')

    # Return book
    return_parser = subparsers.add_parser('return', help='Return a book')
    return_parser.add_argument('book_id', type=int, help='ID of the book')

    # Generate report
    report_parser = subparsers.add_parser('report', help='Generate a report')
    report_parser.add_argument('report_type', choices=['borrowed', 'overdue'], help='Type of report to generate')

    args = parser.parse_args()

    if args.command == 'add':
        try:
            add_book(args.title, args.author, args.genre)
            print(f"Book '{args.title}' by {args.author} added.")
        except Exception as e:
            print(f"Error adding book: {e}")
    elif args.command == 'update':
        try:
            update_book(args.book_id, args.title, args.author, args.genre, args.status)
            print(f"Book ID {args.book_id} updated.")
        except Exception as e:
            print(f"Error updating book: {e}")
    elif args.command == 'delete':
        try:
            delete_book(args.book_id)
            print(f"Book ID {args.book_id} deleted.")
        except Exception as e:
            print(f"Error deleting book: {e}")
    elif args.command == 'list':
        try:
            books = get_books(args.sort_by, args.filter_by, args.filter_value)
            if books:
                for book in books:
                    print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Genre: {book[3]}, Status: {book[4]}, Due Date: {book[5]}")
            else:
                print("No books found.")
        except Exception as e:
            print(f"Error listing books: {e}")
    elif args.command == 'search':
        try:
            books = search_books(args.field, args.value)
            if books:
                for book in books:
                    print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Genre: {book[3]}, Status: {book[4]}, Due Date: {book[5]}")
            else:
                print(f"No books found for {args.field} '{args.value}'.")
        except Exception as e:
            print(f"Error searching for books: {e}")
    elif args.command == 'borrow':
        try:
            if borrow_book(args.book_id):
                print(f"Book ID {args.book_id} borrowed.")
            else:
                print(f"Book ID {args.book_id} is not available for borrowing.")
        except Exception as e:
            print(f"Error borrowing book: {e}")
    elif args.command == 'return':
        try:
            if return_book(args.book_id):
                print(f"Book ID {args.book_id} returned.")
            else:
                print(f"Book ID {args.book_id} is not borrowed.")
        except Exception as e:
            print(f"Error returning book: {e}")
    elif args.command == 'report':
        try:
            books = generate_report(args.report_type)
            if books:
                for book in books:
                    print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Genre: {book[3]}, Status: {book[4]}, Due Date: {book[5]}")
            else:
                print(f"No books found for report type '{args.report_type}'.")
        except Exception as e:
            print(f"Error generating report: {e}")

if __name__ == '__main__':
    initialize_database()
    main()

                      
