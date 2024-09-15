import scrapy
from urllib.parse import urlparse
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError, TCPTimedOutError
from bs4 import BeautifulSoup


class LivemintSpider(scrapy.Spider):
    name = 'livemint'

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
            self.logger.error("Invalid URL: The provided URL is not from livemint.com.")
    
    def isValidUrl(self, url):
        parsed_url = urlparse(url)
        return (self.name +'.com') in parsed_url.netloc

    def parse(self, response):
        if response.status == 403:
            self.logger.error(f"403 Forbidden: {response.url}")
            return
        title = response.css('title::text').get(default='').strip()
        content = self.extract_article_content(response)

        yield {
            'article_url': response.url,
            'title': title,
            'author_name': response.css('div.storyPage_authorDesc__zPjwo a strong::text').get(),
            'author_url': response.css('div.storyPage_authorDesc__zPjwo a::attr(href)').get(),
            'published_date': response.css('div.storyPage_date__JS9qJ.storyPage_top__RFRL3 span::text').get(),
            'article_content': content
        }
    def extract_article_content(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        content_div = soup.find('div', class_='storyPage_storyContent__m_MYl')
        text_content = content_div.get_text(strip=True)
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