import scrapy
from bs4 import BeautifulSoup
from .base import BaseSpider

class Inc42Spider(BaseSpider):
    name = 'inc42'

    def parse(self, response):
        if response.status == 403:
            self.logger.error(f"403 Forbidden: {response.url}")
            return

        title = response.css('title::text').get(default='').strip()
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
