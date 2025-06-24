import scrapy

class BookSpider(scrapy.Spider):
    """
    This Spider scrapes book information (title and price) from books.toscrape.com.
    It starts on the first page, scrapes all the books, and then follows the 
    pagination link to continue scraping until all pages have been visited.
    """
    
    # The unique name for the spider. This is used to run the spider from the CLI.
    # Example: `scrapy crawl bookspider`
    name = 'bookspider'
    
    # An optional list of strings containing domains that this spider is allowed to crawl.
    # Requests for URLs not belonging to the domains specified here will not be followed.
    allowed_domains = ['books.toscrape.com']
    
    # A list of URLs where the spider will begin to crawl from.
    # Subsequent URLs will be generated from the data contained in these pages.
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        """
        This is the default callback method used by Scrapy to process downloaded responses.
        
        It is responsible for:
        1. Parsing the response data (the HTML of the page).
        2. Extracting the scraped data (book titles and prices).
        3. Finding new URLs to follow (the 'next' page link).
        
        Args:
            response: The Response object containing the page content.
        """
        
        # --- Scrape data from the current page ---
        
        # Select all <article> elements with the class 'product_pod'. Each of these
        # elements represents a single book.
        books = response.css('article.product_pod')

        # Loop through each book element found on the page.
        for book in books:
            # The 'yield' keyword is used to return data from the spider.
            # Scrapy collects these yielded dictionaries.
            yield {
                'title': book.css('h3 a::attr(title)').get(),
                'price': book.css('.product_price .price_color::text').get(),
            }

        # --- Follow pagination link to the next page ---
        
        # Find the link to the next page using its CSS selector.
        # The selector targets the 'href' attribute of the <a> tag inside the
        # <li> element with the class 'next'.
        next_page = response.css('li.next a::attr(href)').get()

        # Check if a 'next' page link was found.
        if next_page is not None:
            # If a link was found, yield a new request to that URL.
            # `response.follow` is a helper that handles relative URLs automatically.
            # The `callback=self.parse` tells Scrapy to use this same method
            # to parse the response from the next page.
            yield response.follow(next_page, callback=self.parse)

