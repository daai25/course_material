# Tutorial: Loading Scraped Data into a SQLite Database

After you've scraped data from the web and saved it to a file like `books.json`, the next logical step is to store it in a structured way that allows for easy querying and analysis. A relational database is perfect for this.

This tutorial walks you through the `database_loader.py` script, which is designed to read your scraped JSON data, clean it up, and insert it into a SQLite database.

## The Goal

We want to transform our list of JSON objects...

```json
{
    "title": "A Light in the Attic",
    "upc": "a897fe39b1053632",
    "price": "£51.77",
    "stock": "In stock (22 available)",
    "description": "It's hard to imagine a world without A Light in the Attic...",
    "url": "[http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html](http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html)"
}
```

...into a structured table inside a database that we can query with SQL.


## [Part 1](doc/tutorial-part01.md)
## [Part 2](doc/tutorial-part02.md)