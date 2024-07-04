# Library Management System

This Python script provides a command-line interface for managing a library system. It utilizes SQLite for database operations and supports functionalities such as adding, updating, deleting books, searching by various criteria, borrowing and returning books, and generating reports on borrowed and overdue books.

## Features

- **Database Integration**: Utilizes SQLite for storing and managing book records.
- **CRUD Operations**: Allows adding, updating, and deleting books from the library.
- **Search Functionality**: Enables searching for books by title, author, or genre.
- **Borrowing and Returning Books**: Tracks book status (available or borrowed) and due dates.
- **Reporting**: Generates reports on borrowed books and books overdue for return.
- **User-Friendly Interface**: Menu-driven interface for easy navigation.

## Getting Started

### Prerequisites

- Python 3.x
- SQLite 3

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/library-management.git
   cd library-management
   ```

2. Install dependencies (if any):
   ```
   pip install -r requirements.txt
   ```

### Usage

1. Initialize the database:
   ```
   python library.py
   ```

2. Follow the menu prompts to perform various operations:

   **Menu Options:**
   - **1. Add a book**: Enter details to add a new book to the library.
   - **2. Update a book**: Modify details of an existing book by entering its ID.
   - **3. Delete a book**: Remove a book from the library by entering its ID.
   - **4. List all books**: Display a list of all books currently in the library.
   - **5. Search for books**: Search for books by title, author, or genre.
   - **6. Borrow a book**: Borrow a book by entering its ID (if available).
   - **7. Return a book**: Return a borrowed book by entering its ID.
   - **8. Generate a report**: Choose to generate a list of borrowed books or overdue books.
   - **9. Exit**: Quit the program.

3. Exit the program when done.

## Contributing

Contributions are welcome! Please feel free to fork the repository and submit pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by the need for a simple yet effective library management tool.
- Built with Python and SQLite.