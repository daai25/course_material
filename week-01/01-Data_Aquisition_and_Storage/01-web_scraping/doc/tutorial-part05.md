# Part 5: Scraping JavaScript-Rendered Content using Scrapy and Playwright

This tutorial shows how to use [Scrapy](https://scrapy.org/) with [Playwright](https://playwright.dev/) to scrape dynamically rendered content from websites. We'll walk through setting up a Scrapy spider using the `scrapy-playwright` integration.

> **Goal**: Scrape the website `https://quotes.toscrape.com/js/` and extract the quotes and the authors.
---

## 1. Setup
1. **Activate the Virtual Environment:**  
   * **On macOS and Linux:**  
     ```bash
     source venv/bin/activate
     ```
   * **On Windows:**  
   	```bash
	.\venv\Scripts\activate
    ```

2. **Install the required packages using pip**   

    ```bash
    pip install scrapy-playwright beautifulsoup4
    playwright install
    ```

3. **Create and enter a new Scrapy project**

    ```bash
    scrapy startproject myspiderjs
    cd myspiderjs
    ```

---


## 2. Step-by-Step Approach

We will demonstrate the impact of JavaScript rendering by first scraping the website **without** Playwright, and then **with** Playwright.

---

### 2.1 Spider WITHOUT Playwright

This version does not render JavaScript, so it is unlikely to extract dynamic content.

Create `spiders/noplaywright_spider.py`:

```python
from scrapy.spiders import Spider
from bs4 import BeautifulSoup

class NoPlaywrightSpider(Spider):
    name = 'noplaywright'
    start_urls = ['https://quotes.toscrape.com/js/']  
    allowed_domains = ['quotes.toscrape.com']

    
    def parse(self, response, **kwargs):
        """
        Parse the response and extract quotes data.
        This method processes the HTML after JavaScript has been executed.
        """
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all quote containers using CSS selector
        quotes = soup.select('.quote')
        
        # Loop through each quote and extract data
        for quote in quotes:
            # Extract quote text (remove quotes and whitespace)
            text = quote.select_one('.text').get_text(strip=True)
            
            # Extract author name
            author = quote.select_one('.author').get_text(strip=True)
            
            # Extract all tags associated with this quote
            tags = [tag.get_text(strip=True) for tag in quote.select('.tag')]
            
            # Yield the extracted data as a dictionary
            yield {
                'text': text,
                'author': author,
                'tags': tags
            }

```

**Run it:**

```bash
scrapy crawl noplaywright -O output_noplaywright.json
```

You’ll likely notice that no quotes where extracted.

---

### 2.2 Spider WITH Playwright

Create `spiders/playwright_spider.py` and enable Playwright rendering:

Often Websites use dynamically loaded content. To catch this dynamically loaded content the scraper needs to render the page. Normally scrapy only downloads the HTML document. One of different possibilities is, to use scrapy implementation for playwright, scrapy-playwright. A possible implementation could look like this:

```python
from scrapy.spiders import Spider
import scrapy
from scrapy.linkextractors import LinkExtractor  # Utility to extract links from response
from bs4 import BeautifulSoup  # For parsing HTML and extracting text
import re  # Regular expressions for pattern matching
from scrapy_playwright.page import PageMethod  # For executing methods like 'wait_for_load_state' in Playwright

class ASpider(Spider):
    name = 'playwright'
    start_urls = ['https://quotes.toscrape.com/js/']  
    allowed_domains = ['quotes.toscrape.com']

    custom_settings = {
        # Use asyncio-based Twisted reactor for Playwright compatibility
        'TWISTED_REACTOR': 'twisted.internet.asyncioreactor.AsyncioSelectorReactor',
        
        # Use Firefox as the Playwright browser (can also use 'chromium' or 'webkit')
        'PLAYWRIGHT_BROWSER_TYPE': 'firefox',

        # Set download handlers to use Playwright for HTTP and HTTPS requests
        'DOWNLOAD_HANDLERS': {
            'http': 'scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler',
            'https': 'scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler',
        },

        # Browser launch settings for Playwright
        'PLAYWRIGHT_LAUNCH_OPTIONS': {
            'headless': True,  # Run without UI
            'timeout': 30 * 1000,  # Increased timeout to 30 seconds
        },

        # Navigation timeout for Playwright page loads (60 seconds)
        'PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT': 60 * 1000,

        # Define context such as screen size for the headless browser
        'PLAYWRIGHT_CONTEXTS': {
            'default': {
                'viewport': {'width': 2560, 'height': 1440},
                'user_agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            },
        },

        # Add retry settings
        'RETRY_TIMES': 3,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 408, 429],
        
        # Add download delay to be more respectful
        'DOWNLOAD_DELAY': 2,
        'RANDOMIZE_DOWNLOAD_DELAY': True,

        # Stop spider if no items are scraped within 120 seconds
        'CLOSESPIDER_TIMEOUT_NO_ITEM': 120,
    }

    def parse(self, response, **kwargs):
        """
        Parse the response and extract quotes data.
        This method processes the HTML after JavaScript has been executed.
        """
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all quote containers using CSS selector
        quotes = soup.select('.quote')
        
        # Loop through each quote and extract data
        for quote in quotes:
            # Extract quote text (remove quotes and whitespace)
            text = quote.select_one('.text').get_text(strip=True)
            
            # Extract author name
            author = quote.select_one('.author').get_text(strip=True)
            
            # Extract all tags associated with this quote
            tags = [tag.get_text(strip=True) for tag in quote.select('.tag')]
            
            # Yield the extracted data as a dictionary
            yield {
                'text': text,
                'author': author,
                'tags': tags
            }

    def start_requests(self):
        """
        Generate the initial requests with Playwright configuration.
        This method enables JavaScript rendering for each URL.
        """
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={
                    # Enable Playwright for this request (JavaScript execution)
                    'playwright': True,
                    
                    # Define page methods to execute in the browser
                    'playwright_page_methods': [
                        # Wait for quote elements to appear (JavaScript loaded content)
                        PageMethod('wait_for_selector', '.quote'),
                        
                        # Wait until no network requests are ongoing (page fully loaded)
                        PageMethod('wait_for_load_state', 'networkidle'),
                    ],
                }
            )
```

**Run it:**

```bash
scrapy crawl playwright -O output_playwright.json
```

This time, you should see output containing quotes and authors.

---

## 3. Following Links with Playwright

If you want your spider to follow links to other pages (for example, to scrape quotes from multiple pages), you can use Scrapy's `LinkExtractor` together with Playwright. Here’s how you can do it inside your `parse` method:

```python
from scrapy.linkextractors import LinkExtractor
from scrapy_playwright.page import PageMethod

def parse(self, response, **kwargs):
    # ... your other code ...

    # Extract links to follow (e.g., pagination)
    links = LinkExtractor(allow_domains=self.allowed_domains).extract_links(response)
    for link in links:
        yield response.follow(
            link.url,
            self.parse,
            meta={
                "playwright": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_load_state", "networkidle")
                ]
            }
        )
```

This approach ensures that each followed link is also rendered with Playwright, allowing you to scrape JavaScript-generated content on every page.
