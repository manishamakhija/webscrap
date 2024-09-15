import scrapy
from urllib.parse import urlparse
from bs4 import BeautifulSoup

class Inc42Spider(scrapy.Spider):
    name = 'inc42'

    def start_requests(self):
        url = getattr(self, 'url', None)
        
        # Validate the URL
        if url and self.is_inc42_url(url):
            yield scrapy.Request(url=url, callback=self.parse, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
            }, errback=self.handle_error)
        else:
            self.log("Invalid URL: The provided URL is not from inc42.com.")
    
    def is_inc42_url(self, url):
        """Check if the given URL belongs to inc42.com"""
        parsed_url = urlparse(url)
        return 'inc42.com' in parsed_url.netloc

    def parse(self, response):
        if response.status == 403:
            self.logger.error(f"403 Forbidden: {response.url}")
            return

        title = response.css('h1::text').get(default='').strip()
        published_date = response.css('div.date span::text').get(default='').strip()
        author_name = response.css('span.readtime a::text').get(default='').strip()
        author_url = response.css('span.readtime a::attr(href)').get(default='').strip()
        if author_url:
            author_url = response.urljoin(author_url)
        
        article_content = self.extract_article_content(response)

        yield {
            'article_url': response.url,
            'title': title,
            'author_name': author_name,
             'author_url': author_url,
            'published_date': published_date,
            'article_content': article_content
        }

    def extract_article_content(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        content_div = soup.find('div', class_='single-post-content')
        text_content = content_div.get_text(strip=True)
        return text_content

    def handle_error(self, failure):
        self.logger.error(repr(failure))

        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error(f"HttpError on {response.url}")
        elif failure.check(DNSLookupError):
            self.logger.error("DNSLookupError: Check your domain")
        elif failure.check(TimeoutError, TCPTimedOutError):
            self.logger.error("TimeoutError or TCPTimedOutError: The request timed out")
