import sqlite3
from datetime import datetime, timedelta

# Initialize database
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

# Add a new book
def add_book():
    title = input("Enter the title of the book: ")
    author = input("Enter the author of the book: ")
    genre = input("Enter the genre of the book: ")

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO books (title, author, genre, status, due_date)
        VALUES (?, ?, ?, ?, ?)
    ''', (title, author, genre, 'available', None))
    conn.commit()
    conn.close()
    print(f"Book '{title}' by {author} added.")

# Update an existing book
def update_book():
    book_id = input("Enter the ID of the book to update: ")

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM books
        WHERE id = ?
    ''', (book_id,))
    book = cursor.fetchone()
    conn.close()

    if not book:
        print(f"Book with ID {book_id} not found.")
        return

    print(f"Current details - Title: {book[1]}, Author: {book[2]}, Genre: {book[3]}")

    title = input("Enter new title (leave blank to keep current): ").strip() or book[1]
    author = input("Enter new author (leave blank to keep current): ").strip() or book[2]
    genre = input("Enter new genre (leave blank to keep current): ").strip() or book[3]
    status = input("Enter new status (available/borrowed, leave blank to keep current): ").strip() or book[4]
    due_date = input("Enter new due date (YYYY-MM-DD, leave blank to keep current): ").strip() or book[5]

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE books
        SET title = ?, author = ?, genre = ?, status = ?, due_date = ?
        WHERE id = ?
    ''', (title, author, genre, status, due_date, book_id))
    conn.commit()
    conn.close()
    print(f"Book ID {book_id} updated.")

# Delete a book
def delete_book():
    book_id = input("Enter the ID of the book to delete: ")

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM books
        WHERE id = ?
    ''', (book_id,))
    book = cursor.fetchone()

    if not book:
        print(f"Book with ID {book_id} not found.")
        conn.close()
        return

    confirm = input(f"Are you sure you want to delete '{book[1]}' by {book[2]}? (yes/no): ").strip().lower()
    if confirm == 'yes':
        cursor.execute('''
            DELETE FROM books
            WHERE id = ?
        ''', (book_id,))
        conn.commit()
        print(f"Book ID {book_id} deleted.")
    else:
        print("Deletion cancelled.")
    
    conn.close()

# List all books
def list_books():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    conn.close()

    if books:
        print("\nList of Books:")
        for book in books:
            print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Genre: {book[3]}, Status: {book[4]}, Due Date: {book[5]}")
    else:
        print("No books found.")

# Search for books by title, author, or genre
def search_books():
    print("\nSearch Options:")
    print("1. Search by title")
    print("2. Search by author")
    print("3. Search by genre")
    print("4. Back to main menu")

    choice = input("Enter your search option (1-4): ").strip()

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if choice == '1':
        title = input("Enter title to search for: ").strip()
        cursor.execute('''
            SELECT * FROM books
            WHERE title LIKE ?
        ''', ('%' + title + '%',))
    elif choice == '2':
        author = input("Enter author to search for: ").strip()
        cursor.execute('''
            SELECT * FROM books
            WHERE author LIKE ?
        ''', ('%' + author + '%',))
    elif choice == '3':
        genre = input("Enter genre to search for: ").strip()
        cursor.execute('''
            SELECT * FROM books
            WHERE genre LIKE ?
        ''', ('%' + genre + '%',))
    elif choice == '4':
        conn.close()
        return
    else:
        print("Invalid choice.")
        conn.close()
        return

    books = cursor.fetchall()
    conn.close()

    if books:
        print("\nSearch Results:")
        for book in books:
            print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Genre: {book[3]}, Status: {book[4]}, Due Date: {book[5]}")
    else:
        print("No books found.")

# Borrow a book
def borrow_book():
    book_id = input("Enter the ID of the book to borrow: ")

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
        print(f"Book ID {book_id} borrowed.")
    else:
        print(f"Book ID {book_id} is not available for borrowing.")

    conn.close()

# Return a borrowed book
def return_book():
    book_id = input("Enter the ID of the book to return: ")

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
        print(f"Book ID {book_id} returned.")
    else:
        print(f"Book ID {book_id} is not borrowed.")

    conn.close()

# Generate a report of borrowed or overdue books
def generate_report():
    print("\nReport Options:")
    print("1. List of borrowed books")
    print("2. List of overdue books")
    print("3. Back to main menu")

    choice = input("Enter your report option (1-3): ").strip()

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if choice == '1':
        cursor.execute('''
            SELECT * FROM books
            WHERE status = 'borrowed'
        ''')
        books = cursor.fetchall()

        if books:
            print("\nList of Borrowed Books:")
            for book in books:
                print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Genre: {book[3]}, Status: {book[4]}, Due Date: {book[5]}")
        else:
            print("No borrowed books.")
    elif choice == '2':
        today = datetime.now().date()
        cursor.execute('''
            SELECT * FROM books
            WHERE status = 'borrowed' AND due_date < ?
        ''', (today,))
        books = cursor.fetchall()

        if books:
            print("\nList of Overdue Books:")
            for book in books:
                print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Genre: {book[3]}, Status: {book[4]}, Due Date: {book[5]}")
        else:
            print("No overdue books.")
    elif choice == '3':
        conn.close()
        return
    else:
        print("Invalid choice.")
    
    conn.close()

# Main menu function to interact with the library system
def main():
    initialize_database()

    while True:
        print("\nLibrary Management System")
        print("1. Add a book")
        print("2. Update a book")
        print("3. Delete a book")
        print("4. List all books")
        print("5. Search for books")
        print("6. Borrow a book")
        print("7. Return a book")
        print("8. Generate a report")
        print("9. Exit")

        choice = input("Enter your choice (1-9): ").strip()

        if choice == '1':
            add_book()
        elif choice == '2':
            update_book()
        elif choice == '3':
            delete_book()
        elif choice == '4':
            list_books()
        elif choice == '5':
            search_books()
        elif choice == '6':
            borrow_book()
        elif choice == '7':
            return_book()
        elif choice == '8':
            generate_report()
        elif choice == '9':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 9.")

if __name__ == '__main__':
    main()
