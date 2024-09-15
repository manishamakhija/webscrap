# Web Scrapping for news Articles
Scrape articles from all categories on the provided websites Livemint , Economics, Telegraf, Inc42, Digital Terminal

## Getting Started
To setup please follow following steps

### 1. Clone the Repository
```console
https://github.com/manishamakhija/webscrap.git
cd news_scraper/news_scraper
```
### 2. install python
if using mac
```console
brew install python@3.9
```

### 3. install required lib
```console
pip install scrapy
pip install beautifulsoup4
pip install selenium
```

### 4. Run script
Run run_spiders.py script while passing article url
```console
url=<article url eg: https://digitalterminal.in/trending/ai-and-automation-drive-50-faster-software-development-outsystems-and-kpmg-survey-reveals>
python3 run_spiders.py $(echo $url)
```

### 5. See output file
Output response will be generated in .output folder
for digitalterminal articles
file name will be output_digitalterminal.json
Sample res

```console
[
{
    "article_url": "https://digitalterminal.in/trending/ai-and-automation-drive-50-faster-software-development-outsystems-and-kpmg-survey-reveals",
    "title": "AI and Automation Drive 50% Faster Software Development, OutSystems and KPMG Survey Reveals",
    "published_date": "2024-09-14T05:46:35.076Z",
    "article_content": <content>,
    "category": "Trending"
}
]
```
