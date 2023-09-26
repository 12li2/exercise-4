
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Create the Books table
cursor.execute('''CREATE TABLE IF NOT EXISTS Books (
                    BookID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Title TEXT NOT NULL,
                    Author TEXT NOT NULL,
                    ISBN TEXT NOT NULL,
                    Status TEXT NOT NULL
                )''')

# Create the Users table
cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Name TEXT NOT NULL,
                    Email TEXT NOT NULL
                )''')

# Create the Reservations table
cursor.execute('''CREATE TABLE IF NOT EXISTS Reservations (
                    ReservationID INTEGER PRIMARY KEY AUTOINCREMENT,
                    BookID INTEGER NOT NULL,
                    UserID INTEGER NOT NULL,
                    ReservationDate TEXT NOT NULL,
                    FOREIGN KEY (BookID) REFERENCES Books (BookID),
                    FOREIGN KEY (UserID) REFERENCES Users (UserID)
                )''')

# Add a new book to the database
def add_book():
    title = input("Enter the title of the book: ")
    author = input("Enter the author of the book: ")
    isbn = input("Enter the ISBN of the book: ")
    status = input("Enter the status of the book: ")

    cursor.execute("INSERT INTO Books (Title, Author, ISBN, Status) VALUES (?, ?, ?, ?)", (title, author, isbn, status))
    conn.commit()
    print("Book added successfully.")

# Find a book's details based on BookID
def find_book_details():
    book_id = input("Enter the BookID: ")
    cursor.execute("SELECT * FROM Books WHERE BookID = ?", (book_id,))
    book = cursor.fetchone()

    if book:
        print("Book details:")
        print("BookID:", book[0])
        print("Title:", book[1])
        print("Author:", book[2])
        print("ISBN:", book[3])
        print("Status:", book[4])
        cursor.execute('''SELECT Users.Name, Users.Email, Reservations.ReservationDate
                          FROM Reservations
                          INNER JOIN Users ON Reservations.UserID = Users.UserID
                          WHERE Reservations.BookID = ?''', (book_id,))
        reservation = cursor.fetchone()

        if reservation:
            print("Reserved by:")
            print("Name:", reservation[0])
            print("Email:", reservation[1])
            print("Reservation Date:", reservation[2])
        else:
            print("Not reserved.")
    else:
        print(" Book does not exist in the database.")

# Find a book's reservation status based on BookID, Title, UserID, and ReservationID
def find_reservation_status():
    search_text = input("Enter the BookID, Title, UserID, and ReservationID: ")

    if search_text.startswith("LB"):
        cursor.execute("SELECT Status FROM Books WHERE BookID = ?", (search_text,))
        status = cursor.fetchone()
        if status:
            print("Reservation status:", status[0])
        else:
            print("Book does not exist in the database.")
    elif search_text.startswith("LU"):
        cursor.execute('''SELECT Books.Title, Books.Status
                          FROM Reservations
                          INNER JOIN Books ON Reservations.BookID = Books.BookID
                          WHERE Reservations.UserID = ?''', (search_text,))
        books = cursor.fetchall()

        if books:
            print("Reserved books:")
            for book in books:
                print("Title:", book[0])
                print("Reservation status:", book[1])
        else:
            print("User not found or has no reservations.")
    elif search_text.startswith("LR"):
        cursor.execute('''SELECT Books.Title, Users.Name, Books.Status
                          FROM Reservations
                          INNER JOIN Books ON Reservations.BookID = Books.BookID
                          INNER JOIN Users ON Reservations.UserID = Users.UserID
                          WHERE Reservations.ReservationID = ?''', (search_text,))
        reservation = cursor.fetchone()

        if reservation:
            print("Reservation details:")
            print("Title:", reservation[0])
            print("Reserved by:", reservation[1])
            print("Reservation status:", reservation[2])
        else:
            print("Reservation not found.")
    else:
        cursor.execute('''SELECT Books.Title, Books.Author, Books.ISBN, Books.Status,
                                 Users.Name, Users.Email, Reservations.ReservationDate
                          FROM Books
                          LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                          LEFT JOIN Users ON Reservations.UserID = Users.UserID
                          WHERE Books.Title LIKE ?''', ('%' + search_text + '%',))
        books = cursor.fetchall()

        if books:
            print("Search results:")
            for book in books:
                print("Title:", book[0])
                print("Author:", book[1])
                print("ISBN:", book[2])
                print("Reservation status:", book[3])
                print("Reserved by:", book[4])
                print("Email:", book[5])
                print("Reservation Date:", book[6])
        else:
            print("Book does not exist in the database.")

# Find all the books in the database
def find_all_books():
    cursor.execute('''SELECT Books.BookID, Books.Title, Books.Author, Books.ISBN, Books.Status,
                             Users.Name, Users.Email, Reservations.ReservationDate
                      FROM Books
                      LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                      LEFT JOIN Users ON Reservations.UserID = Users.UserID''')
    books = cursor.fetchall()
    if books:
        print("All books:")
        for book in books:
            print("BookID:", book[0])
            print("Title:", book[1])
            print("Author:", book[2])
            print("ISBN:", book[3])
            print("Status:", book[4])
            print("Reserved by:", book[5])
            print("Email:", book[6])
            print("Reservation Date:", book[7])
    else:
        print("Book does not exist in the database.")

# Modify/update book details based on its BookID
def update_book_details():
    book_id = input("Enter the BookID: ")
    cursor.execute("SELECT * FROM Books WHERE BookID = ?", (book_id,))
    book = cursor.fetchone()

    if book:
        print("Current details:")
        print("Title:", book[1])
        print("Author:", book[2])
        print("ISBN:", book[3])
        print("Status:", book[4])

        choice = input("What do you want to modify? (1. Title, 2. Author, 3. ISBN, 4. Status): ")
        
        if choice == "1":
            new_title = input("Enter the new title: ")
            cursor.execute("UPDATE Books SET Title = ? WHERE BookID = ?", (new_title, book_id))
            conn.commit()
            print("Title updated successfully.")
        elif choice == "2":
            new_author = input("Enter the new author: ")
            cursor.execute("UPDATE Books SET Author = ? WHERE BookID = ?", (new_author, book_id))
            conn.commit()
            print("Author updated successfully.")
        elif choice == "3":
            new_isbn = input("Enter the new ISBN: ")
            cursor.execute("UPDATE Books SET ISBN = ? WHERE BookID = ?", (new_isbn, book_id))
            conn.commit()
            print("ISBN updated successfully.")
        elif choice == "4":
            new_status = input("Enter the new status: ")
            cursor.execute("UPDATE Books SET Status = ? WHERE BookID = ?", (new_status, book_id))
            cursor.execute("UPDATE Reservations SET Status = ? WHERE BookID = ?", (new_status, book_id))
            conn.commit()
            print("Status updated successfully.")
        else:
            print("Invalid choice.")
    else:
        print("Book does not exist in the database.")

# Delete a book based on its BookID
def delete_book():
    book_id = input("Enter the BookID: ")
    cursor.execute("SELECT * FROM Books WHERE BookID = ?", (book_id,))
    book = cursor.fetchone()

    if book:
        cursor.execute("SELECT * FROM Reservations WHERE BookID = ?", (book_id,))
        reservation = cursor.fetchone()

        if reservation:
            cursor.execute("DELETE FROM Reservations WHERE BookID = ?", (book_id,))
            conn.commit()

        cursor.execute("DELETE FROM Books WHERE BookID = ?", (book_id,))
        conn.commit()
        print("Book deleted successfully.")
    else:
        print("Book does not exist in the database.")

# Main program loop
while True:
    print("\nLibrary Management System")
    print("1. Add a new book to the database")
    print("2. Find a book's details based on BookID")
    print("3. Find a book's reservation status based on BookID, Title, UserID, or ReservationID")
    print("4. Find all the books in the database")
    print("5. Modify/update book details based on its BookID")
    print("6. Delete a book based on its BookID")
    print("7. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_book()
    elif choice == "2":
        find_book_details()
    elif choice == "3":
        find_reservation_status()
    elif choice == "4":
        find_all_books()
    elif choice == "5":
        update_book_details()
    elif choice == "6":
        delete_book()
    elif choice == "7":
        break
    else:
        print("Invalid choice.")

# Close the database connection
conn.close()