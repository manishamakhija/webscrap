import scrapy
from bs4 import BeautifulSoup
from .base import BaseSpider

class DigitalTerminalSpider(BaseSpider):
    name = 'digitalterminal'

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
