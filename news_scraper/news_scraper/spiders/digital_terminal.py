import scrapy
from urllib.parse import urlparse
from bs4 import BeautifulSoup

class DigitalTerminalSpider(scrapy.Spider):
    name = 'digital_terminal'

    def start_requests(self):
        # The URL will be passed as an argument via the command line
        url = getattr(self, 'url', None)
        
        # Validate the URL
        if url and self.is_digital_terminal_url(url):
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
                },
                errback=self.handle_error
            )
        else:
            self.log("Invalid URL: The provided URL is not from digitalterminal.in.")
    
    def is_digital_terminal_url(self, url):
        """Check if the given URL belongs to digitalterminal.in"""
        parsed_url = urlparse(url)
        return 'digitalterminal.in' in parsed_url.netloc

    def parse(self, response):
        if response.status == 403:
            self.logger.error(f"403 Forbidden: {response.url}")
            return
        soup = BeautifulSoup(response.text, 'html.parser')
        title = response.css('title::text').get(default='').strip()
        article_content = self.extract_article_content(response)
        category = self.extract_category(soup)
        yield {
            'article_url': response.url,
            'title': title,
            'published_date': response.css('time::attr(datetime)').get(),  # Adjust this if necessary
            'article_content': article_content,
            # 'category': response.css('div.category a::text').get()
            'category' : category

        }
    def extract_article_content(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        content_div = soup.find('div', class_='arr--story-page-card-wrapper')
        text_content = content_div.get_text(strip=True)
        return text_content
    
    def extract_category(self, soup):
        """Extract the category from the soup object."""
        try:
            # Locate the div containing the category
            category_div = soup.find('div', class_='text-story-m_header-details__3D-Xf')
            if category_div:
                # Extract the category from the span with class 'section-tag'
                category_span = category_div.find('span', class_='section-tag')
                if category_span:
                    return category_span.get_text(strip=True)
        except Exception as e:
            self.logger.error(f"Error extracting category: {e}")
        return ''

    def handle_error(self, failure):
        # Log the error
        self.logger.error(repr(failure))

        # Check if failure is a response failure
        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error(f"HttpError on {response.url}")
        elif failure.check(DNSLookupError):
            self.logger.error("DNSLookupError: Check your domain")
        elif failure.check(TimeoutError, TCPTimedOutError):
            self.logger.error("TimeoutError or TCPTimedOutError: The request timed out")
