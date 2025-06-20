# Part 4: Handling Pagination and Following Links

Congratulations on making it to the final part! So far, our spider can only scrape the first page of the bookstore. To get *all* the books, we need to teach it how to navigate to the next page and the page after that, until there are no pages left. This is called **pagination**.

## Step 1: Finding the "Next" Button Link

As always, the first step is to inspect the page. Go to [books.toscrape.com](http://books.toscrape.com) and scroll to the bottom. You'll see a "next" button. Right-click it and choose "Inspect".

You will find the following HTML structure:
```html
<li class="next"><a href="catalogue/page-2.html">next</a></li>
```
This is great! There's a `<li>` element with the class `next`, and inside it is an `<a>` tag with the link (`href`) to the next page. This is the link we need to follow.

## Step 2: Teaching the Spider to Follow Links

Scrapy has a wonderfully elegant way to handle this. We can find the link, and if it exists, we tell Scrapy to "follow" it and run the same `parse` method on the new page.

Let's update our `bookscraper/spiders/bookspider.py` file one last time.

```python
import scrapy

class BookspiderSpider(scrapy.Spider):
    name = 'bookspider'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['[http://books.toscrape.com/](http://books.toscrape.com/)']

    def parse(self, response):
        # --- (Code for scraping books on the current page - no changes here) ---
        books = response.css('article.product_pod')
        for book in books:
            yield {
                'title': book.css('h3 a::attr(title)').get(),
                'price': book.css('.product_price .price_color::text').get(),
            }

        # --- (New code for finding and following the next page link) ---
        # 1. Find the 'next' button's link
        next_page = response.css('li.next a::attr(href)').get()

        # 2. If a 'next' page link exists, follow it
        if next_page is not None:
            # response.follow is a shortcut for creating a new request
            # We tell it to use the same 'parse' method for the next page
            yield response.follow(next_page, callback=self.parse)
```

### How It Works:

1.  After scraping all the books on the current page, our code looks for the "next" button's link using `response.css('li.next a::attr(href)').get()`.
2.  If it finds a link (`next_page is not None`), it uses `response.follow()`.
3.  `response.follow(next_page, callback=self.parse)` is a powerful helper that does two things:
    * It automatically creates a full URL from the relative path (`catalogue/page-2.html` becomes `http://books.toscrape.com/catalogue/page-2.html`).
    * It creates a new `Request` for that URL and schedules it. Crucially, it sets the `callback` to `self.parse`, meaning when the next page is downloaded, Scrapy will send its response right back to this same method.

This creates a loop: the spider parses a page for books, finds the next link, follows it, and then runs the exact same logic on the next page. This continues until it reaches the last page, where there is no "next" button, `next_page` becomes `None`, and the spider stops.

## Step 3: Run the Full Scrape

You're ready for the final run. Go to your terminal and execute the crawl command, overwriting the old JSON file.

```bash
scrapy crawl bookspider -o books.json
```

Watch the log output! You'll see Scrapy scraping page 1, then page 2, then page 3, and so on, all the way to page 50.

Once it's finished, open your `books.json` file. It will now contain all 1,000 books from the entire website!

## Conclusion

You did it! You have successfully built a web scraper that can:
* Start from a specific URL.
* Extract structured data (title and price) from a page.
* Identify and follow pagination links to crawl an entire website.
* Save the collected data into a clean JSON file.

This is the foundation of web scraping. From here, you can explore more advanced topics like handling different item fields, dealing with logins, using proxies, and deploying your spiders to the cloud. Happy scraping!

                