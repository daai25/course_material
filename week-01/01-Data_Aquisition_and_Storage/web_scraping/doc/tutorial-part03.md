# Part 3: Extracting Data with Selectors

Our spider can now visit the website, but it doesn't do anything with the page content. In this part, we'll learn how to use Scrapy's **selectors** to find and extract the data we want, specifically the title and price of each book on the first page.

## Step 1: Inspecting the Web Page

Before you can extract data, you need to know where it is in the HTML structure.

1.  Open [books.toscrape.com](http://books.toscrape.com) in your web browser (like Chrome or Firefox).
2.  Right-click on the title of the first book ("A Light in the Attic") and select "Inspect" or "Inspect Element".
3.  Your browser's developer tools will open, highlighting the HTML for that element.

You'll see something like this:
```html
<article class="product_pod">
    <div class="image_container">
        ...
    </div>
    <p class="star-rating Three">
        ...
    </p>
    <h3><a href="catalogue/a-light-in-the-attic_1000/index.html" title="A Light in the Attic">A Light in the ...</a></h3>
    <div class="product_price">
        <p class="price_color">£51.77</p>
        ...
    </div>
    ...
</article>
```
From this, we can see:
* Each book is contained within an `<article>` tag with the class `product_pod`.
* The title is inside an `<a>` tag, which is inside an `<h3>` tag. The title itself is the `title` attribute of the `<a>` tag.
* The price is inside a `<p>` tag with the class `price_color`.

## Step 2: Using CSS Selectors in Scrapy

Scrapy allows us to use powerful CSS selectors to pinpoint these elements. Let's modify our spider to use them.

Open `bookscraper/spiders/bookspider.py` and update the `parse` method:

```python
import scrapy

class BookspiderSpider(scrapy.Spider):
    name = 'bookspider'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['[http://books.toscrape.com/](http://books.toscrape.com/)']

    def parse(self, response):
        # We'll find all the book containers first
        books = response.css('article.product_pod')

        # Then we'll loop through each book container
        for book in books:
            # We use the .css() method on each book container
            # to find the elements *within* that book.
            title = book.css('h3 a::attr(title)').get()
            price = book.css('.product_price .price_color::text').get()

            # yield is like 'return', but for generators.
            # It sends the scraped data back to Scrapy.
            yield {
                'title': title,
                'price': price
            }
```

### Selector Breakdown:

* `response.css('article.product_pod')`: This selects all `<article>` elements that have the class `product_pod`. It returns a list-like object of selectors.
* `book.css('h3 a::attr(title)').get()`:
    * `h3 a`: Selects the `<a>` tag inside an `<h3>` tag.
    * `::attr(title)`: This is a CSS pseudo-selector that extracts the `title` attribute from the selected `<a>` tag.
    * `.get()`: This gets the first result found.
* `book.css('.product_price .price_color::text').get()`:
    * `.product_price .price_color`: Selects an element with class `price_color` that is a descendant of an element with class `product_price`.
    * `::text`: This pseudo-selector extracts the text content from the selected `<p>` tag.
    * `.get()`: Gets the first result.

## Step 3: Running the Spider and Seeing the Data

Now, let's run the crawl again, but this time we'll save the output to a file to see our results clearly.

In your terminal, run:

```bash
scrapy crawl bookspider -o books.json
```

The `-o books.json` flag tells Scrapy to take the data we `yield` and save it into a JSON file named `books.json`.

After the spider finishes, you'll find a `books.json` file in your project directory. Open it, and you'll see the structured data you just scraped!

```json
[
{"title": "A Light in the Attic", "price": "\\u00a351.77"},
{"title": "Tipping the Velvet", "price": "\\u00a353.74"},
{"title": "Soumission", "price": "\\u00a350.10"},
{"title": "Sharp Objects", "price": "\\u00a347.82"},
...and so on for all 20 books on the page
]
```
(Note: `\u00a3` is the unicode representation for the pound sign `£`.)

Success! You've extracted your first pieces of data.

In the final part, we'll learn how to follow links to scrape data from every page of the bookstore, not just the first one.
                