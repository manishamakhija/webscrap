import scrapy
from bs4 import BeautifulSoup
from .base import BaseSpider

class EconomistSpider(BaseSpider):
    name = 'economist'

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
