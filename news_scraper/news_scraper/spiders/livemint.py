import scrapy
from bs4 import BeautifulSoup
from .base import BaseSpider


class LivemintSpider(BaseSpider):
    name = 'livemint'

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