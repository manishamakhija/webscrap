import scrapy
from urllib.parse import urlparse
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError, TCPTimedOutError
from bs4 import BeautifulSoup

class BaseSpider(scrapy.Spider):
    def start_requests(self):
        url = getattr(self, 'url', None)
        
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
            self.logger.error(f"Invalid URL: The provided URL is not from {self.name}.com.")

    def isValidUrl(self, url):
        parsed_url = urlparse(url)
        return (self.name + '.com') in parsed_url.netloc or (self.name + '.in') in parsed_url.netloc

    def handle_error(self, failure):
        self.logger.error(repr(failure))
        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error(f"HttpError on {response.url}")
        elif failure.check(DNSLookupError):
            self.logger.error("DNSLookupError: Could not resolve the domain")
        elif failure.check(TimeoutError, TCPTimedOutError):
            self.logger.error("TimeoutError: The request timed out")

    def extract_article_content(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        # This should be overridden by the specific spider
        return soup.get_text(strip=True)  # Placeholder implementation