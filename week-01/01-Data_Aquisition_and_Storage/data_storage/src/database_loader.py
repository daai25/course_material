import sqlite3
import json
import re
import argparse

def clean_price(price_str):
    """Removes currency symbol and converts to float."""
    if price_str is None:
        return None
    # Remove the '£' symbol and convert to float
    return float(price_str.replace('£', ''))

def get_stock_count(stock_str):
    """Extracts the integer count from the availability string."""
    if stock_str is None:
        return 0
    # Use regex to find all digits in the string
    match = re.search(r'\d+', stock_str)
    if match:
        return int(match.group(0))
    return 0

def create_database(db_name='books.db'):
    """Creates the SQLite database and the books table."""
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Drop the table if it already exists to ensure a clean start
    c.execute('DROP TABLE IF EXISTS books')

    # Create table with appropriate data types and constraints
    c.execute('''
        CREATE TABLE books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE,
            title TEXT NOT NULL,
            upc TEXT NOT NULL UNIQUE,
            price REAL NOT NULL,
            stock INTEGER NOT NULL,
            description TEXT
        )
    ''')

    print(f"Database '{db_name}' and table 'books' created successfully.")
    conn.commit()
    conn.close()

def load_data_to_db(json_file, db_name='books.db'):
    """Loads data from the JSON file into the SQLite database."""
    # Connect to the database
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Load the JSON data
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{json_file}' was not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from the file '{json_file}'.")
        return


    # Iterate through each book in the JSON file
    for book in data:
        # Clean the data before insertion
        cleaned_price = clean_price(book.get('price'))
        stock_count = get_stock_count(book.get('stock'))

        # Insert a row of data
        try:
            c.execute('''
                INSERT INTO books (url, title, upc, price, stock, description)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                book.get('url'),
                book.get('title'),
                book.get('upc'),
                cleaned_price,
                stock_count,
                book.get('description')
            ))
        except sqlite3.IntegrityError as e:
            print(f"Could not insert book with UPC {book.get('upc')}. Error: {e}")


    # Save (commit) the changes and close the connection
    conn.commit()
    conn.close()
    print(f"Successfully loaded {len(data)} records into '{db_name}'.")

if __name__ == '__main__':
    # Set up the argument parser to handle command-line arguments
    parser = argparse.ArgumentParser(
        description="Load book data from a scraped JSON file into a SQLite database."
    )
    
    # Add a required argument for the input JSON file path
    parser.add_argument(
        "json_file", 
        type=str, 
        help="Path to the input JSON file (e.g., 'bookscraper/books.json')."
    )
    
    # Add an optional argument to specify the database file name
    parser.add_argument(
        "--db", 
        type=str, 
        default="books.db", 
        help="Name of the SQLite database file to create. (default: books.db)"
    )
    
    # Parse the arguments provided by the user
    args = parser.parse_args()

    # The main execution block, using the provided arguments
    create_database(db_name=args.db)
    load_data_to_db(json_file=args.json_file, db_name=args.db)

