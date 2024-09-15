import scrapy
from urllib.parse import urlparse
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError, TCPTimedOutError
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy.http import HtmlResponse

class TelegraphSpider(scrapy.Spider):
    name = 'telegraphindia'

    def start_requests(self):
        # The URL will be passed as an argument via the command line
        url = getattr(self, 'url', None)
        
        # Validate the URL
        if url and self.isValidUrl(url):
            url = getattr(self, 'url', None)
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(url)
            html = driver.page_source
            driver.quit()
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                errback=self.handle_error,
                meta={'html': html}
            )
        else:
            self.logger.error("Invalid URL: The provided URL is not from " + self.name + ".com.")
    
    def isValidUrl(self, url):
        parsed_url = urlparse(url)
        return (self.name +'.com') in parsed_url.netloc

    def parse(self, response):
        if response.status == 403:
            self.logger.error(f"403 Forbidden: {response.url}")
            return
        
        title = response.css('title::text').get(default='').strip()
        soup = BeautifulSoup(response.text, 'html.parser')
        publish_date_div = soup.find('div', class_='publishdate mt-32')
        date = ''
        city = ''
        other_name = ''
        if publish_date_div:
            strong_tag = publish_date_div.find('strong')
            if strong_tag:
                other_name = strong_tag.get_text(strip=True)
            span_tag = publish_date_div.find('span')
            if span_tag:
                city = span_tag.get_text(strip=True)
            publish_date_text = publish_date_div.get_text(separator=' ', strip=True)
            parts = publish_date_text.split('Published', 1)
            if len(parts) > 1:
                date = parts[1].strip()
        article_contents = self.extract_article_content(response)
        

        yield {
            'article_url': response.url,
            'title': title,
            'author_name': other_name,
            'published_date': date,
            'city': city,
            'article_content': article_contents
             }

    def extract_article_content(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        content_divs = soup.find_all('article', id = 'contentbox')
        text_content = ' '.join(div.get_text(strip=True) for div in content_divs)
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

