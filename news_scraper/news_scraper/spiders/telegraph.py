import scrapy
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from .base import BaseSpider

class TelegraphSpider(BaseSpider):
    name = 'telegraphindia'

    def start_requests(self):
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
        content_div = soup.find('div', class_ = 'articlemidbox')
        text_content = content_div.get_text(strip=True)
        return text_content