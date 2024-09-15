import scrapy
from urllib.parse import urlparse
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError, TCPTimedOutError
from bs4 import BeautifulSoup

class EconomistSpider(scrapy.Spider):
    name = 'economist'

    def start_requests(self):
        # The URL will be passed as an argument via the command line
        url = getattr(self, 'url', None)
        
        # Validate the URL
        if url and self.isValidUrl(url):
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
                },
                errback=self.handle_error
            )
        else:
            self.logger.error("Invalid URL: The provided URL is not from economist.com.")
    
    def isValidUrl(self, url):
        parsed_url = urlparse(url)
        return (self.name +'.com') in parsed_url.netloc

    def parse(self, response):
        if response.status == 403:
            self.logger.error(f"403 Forbidden: {response.url}")
            return
        
        title = response.css('title::text').get(default='').strip()

        published_date = response.css('time::attr(datetime)').get()

        content = self.extract_article_content(response)

        category = response.css('a[data-analytics="sidebar:section"] span::text').get()

        yield {
            'article_url': response.url,
            'title': title,
            'published_date': published_date,
            'article_content': content,
            'category': category
        }

    def extract_article_content(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        content_div = soup.find('div', class_='css-11m2wk0 e19oi8vf2')
        if content_div:
            text_content = content_div.get_text(strip=True)
        else:
            text_content = ''
        return text_content

    def handle_error(self, failure):
        self.logger.error(repr(failure))
        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error(f"HttpError on {response.url}")
        elif failure.check(DNSLookupError):
            self.logger.error("DNSLookupError: Could not resolve the domain")
        elif failure.check(TimeoutError, TCPTimedOutError):
            self.logger.error("TimeoutError: The request timed out")
