## Part 1: The `database_loader.py` Script


The script uses four standard Python libraries:
* `sqlite3`: For interacting with a SQLite database.
* `json`: For parsing the `.json` file.
* `re`: The regular expressions module, used for advanced string searching to clean our data.
* `argparse`: For parsing command-line arguments, making our script flexible.

### Function 1: `create_database()`

This function sets up our database file and the table schema.

```python
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
```
This SQL command defines the columns of our `books` table, including data types (`TEXT`, `REAL`, `INTEGER`) and constraints (`PRIMARY KEY`, `UNIQUE`, `NOT NULL`).

### Functions 2 & 3: Data Cleaning

Raw scraped data is often "dirty." These helper functions clean the data before it's inserted into the database.

* `clean_price(price_str)`: Removes the `£` symbol and converts the string to a floating-point number.
* `get_stock_count(stock_str)`: Uses a regular expression `r'\d+'` to find the digits in the availability string and converts them to an integer.

### Function 4: `load_data_to_db()`

This is the core of the script. It connects to the database, loads the JSON data from the file provided, loops through each book, cleans the relevant fields, and executes a SQL `INSERT` command to add the book to the `books` table.

### The Main Execution Block: Making the Script Reusable

To make our script independent and reusable, we don't want to hardcode filenames. We use `argparse` to read the filename from the command line.

```python
if __name__ == '__main__':
    # Set up the argument parser
    parser = argparse.ArgumentParser(
        description="Load book data from a scraped JSON file into a SQLite database."
    )
    
    # Add a required argument for the input JSON file path
    parser.add_argument(
        "json_file", 
        help="Path to the input JSON file (e.g., 'bookscraper/books.json')."
    )
    
    # Parse the arguments provided by the user
    args = parser.parse_args()

    # Run our functions using the provided filename
    create_database()
    load_data_to_db(json_file=args.json_file)
```
This block now does the following:
1. Sets up an `ArgumentParser` to understand command-line arguments.
2. Defines a required argument, `json_file`, which is the path to our data.
3. When you run the script, it calls the main functions using the filename you provide.

To run the script, you now open your terminal and provide the path to the JSON file as an argument:
```bash
python database_loader.py bookscraper/books.json
```
This completes the journey from unstructured web data to a clean, structured, and queryable relational database.
                
