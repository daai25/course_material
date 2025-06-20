## Part 2: The Scraper (Extract)
In this part, you will create a Scrapy project that extracts news from the Google News RSS feed.

### Step 1: Create the Scrapy Project
Navigate into your `extract` directory in the terminal and run the command to create a new Scrapy project.

```bash
cd extract
scrapy startproject news_scraper
```

This command creates a `news_scraper` folder with all the necessary files for a Scrapy project.

### Step 2: Create the News Spider

Now, inside your new project, create the spider. This is the bot that will visit the website and extract the data.

Create the file `extract/news_scraper/news_scraper/spiders/news_spider.py` and add the following code:

```python
import scrapy

class NewsSpider(scrapy.Spider):
    # The name we use to call this spider
    name = 'news_spider'
    
    # The URL of the Google News RSS feed for Technology
    start_urls = ['https://news.google.com/rss/search?q=technology']

    def parse(self, response):
        # RSS feeds are XML. remove_namespaces() helps with parsing.
        response.selector.remove_namespaces()
        
        # We loop through each <item> tag in the XML, which represents one news article.
        for item in response.xpath('//item'):
            # yield is like 'return', but for generators. It sends one item at a time.
            yield {
                'title': item.xpath('title/text()').get(),
                'link': item.xpath('link/text()').get(),
                'pub_date': item.xpath('pubDate/text()').get(),
                'source': item.xpath('source/text()').get(),
            }
```


### Step 3: Test Your Spider
From inside the `extract/news_scraper` directory, run your spider and save the output to a test file.

```bash
cd extract/news_scraper
scrapy crawl news_spider -o test_output.json
```

If it works, you will see a `test_output.json` file full of news articles! You have successfully built your extractor
