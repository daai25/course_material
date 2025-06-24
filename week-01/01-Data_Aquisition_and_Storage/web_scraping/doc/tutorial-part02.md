# **Part 2: Creating Your First Scrapy Spider**

In Part 1, we set up our Python environment and installed Scrapy. Now, we'll create a Scrapy project and build a "spider" to crawl the web.

## **What's a Spider?**

In Scrapy, "spiders" are the classes that you define to do the scraping. Scrapy uses these spiders to crawl one or more websites, identify the information you want, and extract it from the page.

## **Step 1: Create a Scrapy Project**

First, make sure you are in your scrapy_tutorial directory and that your virtual environment is activated ((venv) should be visible in your terminal prompt).

Now, run the following command to create a new Scrapy project:

```bash
scrapy startproject bookscraper
```

Scrapy will create a new folder named bookscraper with the following structure:

```bash
bookscraper/
├── scrapy.cfg            # deploy configuration file
└── bookscraper/          # project's Python module, you'll import your code from here
    ├── __init__.py
    ├── items.py          # project items file
    ├── middlewares.py    # project middlewares file
    ├── pipelines.py      # project pipelines file
    ├── settings.py       # project settings file
    └── spiders/          # a directory where you'll later put your spiders
        └── __init__.py
```

Don't worry about all these files for now. The most important ones for us are `settings.py` (where we can customize our scraper's behavior) and the spiders/ directory (where our spiders will live).


## **Step 2: Create Your First Spider**

Now, we need to tell Scrapy to create a basic spider for us. First, navigate into the newly created project directory:

```bash
cd bookscraper
```

From inside this directory, run the `genspider` command:

```bash
scrapy genspider bookspider books.toscrape.com
```

Let's break that command down:

- `genspider`: This is the command to generate a new spider.
- `bookspider`: This is the name we are giving our spider.
- `books.toscrape.com`: This is the base domain our spider is allowed to crawl.

Scrapy will create a new file at `bookscraper/spiders/bookspider.py`.


## **Step 3: Understanding the Spider Code**

Open the new `bookscraper/spiders/bookspider.py` file in a text editor. It should look like this:

```
import scrapy

class BookspiderSpider(scrapy.Spider):
    name = 'bookspider'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        pass
```


Let's look at what each part does:

- `name = 'bookspider'`: This is the unique identifier for our spider. We will use this name to tell Scrapy which spider to run.
- `allowed_domains = ['books.toscrape.com']`: This is a safeguard. It ensures our spider doesn't accidentally wander off to other websites we don't intend to scrape.
- `start_urls = ['http://books.toscrape.com/']`: This is a list of URLs where the spider will begin its crawl.
- `def parse(self, response):`: This is the core method of the spider. Scrapy automatically calls this method for each of the `start_urls`. The `response` object contains the page's content, and it's our job to "parse" it and extract the data we need. For now, it doesn't do anything (`pass`).


## **Step 4: Running Your Spider**


Let's run our spider to see it in action. In your terminal (make sure you're still in the `bookscraper` project directory), run:

```bash
scrapy crawl bookspider
```

You'll see a lot of text scroll by. This is Scrapy's log output, and it's very useful for debugging. If you look through it, you should see lines indicating a successful crawl:


```bash
...
[scrapy.core.engine] INFO: Spider opened
...
[scrapy.core.scraper] DEBUG: Scraped from <200 http://books.toscrape.com/>
...
[scrapy.core.engine] INFO: Spider closed (finished)
...
```

The `200` status code means the request was successful. Our spider successfully fetched the homepage! It didn't extract any data yet, but we've confirmed that it can access the website.

In the [next part](./tutorial-part03.md), we'll modify the `parse` method to start extracting the book titles and prices from the page.
