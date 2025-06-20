## Part 2: Querying Your Data - The Payoff!

Now that our data is in a `books.db` file, we can start asking questions. While you can use a command-line tool, it's often easier to use a graphical program (GUI) to explore your database.

### Using a GUI Tool
A great, simple, and free tool for this is **DB Browser for SQLite**.
* It is free, open-source, and works on Windows, macOS, and Linux.
* It gives you a spreadsheet-like view of your data.
* It has an area to write and run SQL queries easily.

You can download it from: [https://sqlitebrowser.org/](https://sqlitebrowser.org/)

After installing, just use it to open the `books.db` file and you can start exploring and running the queries below.

### Using the Command Line
If you prefer the command line, you can open the database file like this:
```bash
sqlite3 books.db
```
Your terminal prompt will change to `sqlite>`. Now you are ready to run SQL queries!

### Query 1: Find the 5 most expensive books
We want to see the `title` and `price`, sorted by `price` in descending order, and we only want the top 5.

```sql
SELECT title, price FROM books ORDER BY price DESC LIMIT 5;
```

### Query 2: How many books have more than 20 items in stock?
Here we use the `COUNT(*)` function to count the rows that match our `WHERE` clause.

```sql
SELECT COUNT(*) FROM books WHERE stock > 20;
```

### Query 3: Find all books that have the word "Secret" in the title
The `LIKE` operator is used for pattern matching in text. The `%` symbol is a wildcard that means "match any sequence of characters."

```sql
SELECT title, price, stock FROM books WHERE title LIKE '%Secret%';
```

### Query 4: What is the average price of all books?
The `AVG()` function calculates the average value of a numeric column. We can use `ROUND()` to make the output cleaner.

```sql
SELECT ROUND(AVG(price), 2) AS average_price FROM books;
```

### Query 5: Which books are the cheapest but still have at least 15 in stock?
Let's combine filtering and sorting to find the 10 cheapest books that are readily available.

```sql
SELECT title, price, stock FROM books WHERE stock >= 15 ORDER BY price ASC LIMIT 10;
```

To exit the SQLite command line, just type `.quit` and press Enter.

These examples are just the beginning. By having the data in a structured database, you can perform powerful and complex analysis that would be very difficult with a simple JSON file.
                