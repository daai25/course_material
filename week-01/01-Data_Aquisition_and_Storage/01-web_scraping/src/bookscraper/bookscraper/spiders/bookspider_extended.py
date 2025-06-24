import scrapy

class BookSpiderExtended(scrapy.Spider):
    """
    This Spider scrapes detailed book information from books.toscrape.com.
    It starts on the first page, follows the link to each book's detail page
    to scrape more data, and then follows the pagination link to continue 
    until all pages have been visited.
    """
    name = 'bookspider_extended'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        """
        This method parses the main category pages. It finds the link to
        each book's detail page and yields a request to follow it, passing
        the response to the `parse_book_page` method. It also handles
        pagination.
        """
        # Find all the books on the current page
        books = response.css('article.product_pod')

        # For each book, follow the link to its detail page
        for book in books:
            detail_page_url = book.css('h3 a::attr(href)').get()
            yield response.follow(detail_page_url, callback=self.parse_book_page)

        # Find and follow the link to the next page, if it exists
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_book_page(self, response):
        """
        This method parses the book detail page to extract all the
        required information (title, price, stock, UPC, description).
        """
        # The data is organized in a table, so we target the table rows
        table_rows = response.css("table tr")
        
        # Yield a dictionary containing all the scraped data
        yield {
            'title': response.css('.product_main h1::text').get(),
            # The UPC is the first table data cell
            'upc': table_rows[0].css("td ::text").get(),
            'price': response.css('p.price_color::text').get(),
            # The availability text is in the 6th table row
            'stock': table_rows[5].css("td ::text").get(),
            # The description is in the <p> tag right after the div with id="product_description"
            'description': response.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),
            'url': response.url,
        }

