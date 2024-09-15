# Web Scraping for News Articles
This project is designed to scrape articles from multiple categories across several news websites, including Livemint, Economist, Telegraf, Inc42, and Digital Terminal. The scraper automatically detects the source based on the URL and extracts relevant information such as the article's title, author, publication date, content, and category.

## Supported Websites
The following websites are supported for article scraping:
* Livemint
* Economist
* Telegraf
* Inc42
* Digital Terminal
## Getting Started
These instructions will guide you on how to set up and run the web scraper locally to extract articles from supported websites.

## Prerequisites
Before you begin, ensure you have met the following requirements:

* You are using a machine with Python 3.9 or later installed.
* You have installed the required libraries listed in the requirements.txt file or follow the instructions in this README to install them manually.

## Installation

### 1. Clone the Repository
To get started, clone the repository to your local machine:
```console
git clone https://github.com/manishamakhija/webscrap.git
cd webscrap/news_scraper/news_scraper
```
### 2. Install Python
If you're on macOS and Python is not installed, you can install Python 3.9 using Homebrew:
```console
brew install python@3.9
```
On other operating systems, you can download Python from the official Python website.

### 3. Install Required Libraries
Next, install the necessary dependencies for the project:
```console
pip install scrapy beautifulsoup4 selenium
```

## Usage
### 4. Run the Scraper
You can run the scraper by providing the URL of the article you want to scrape. The scraper will automatically identify which spider to use based on the website.

To run the scraper:
```console
url=<article url eg: https://digitalterminal.in/trending/ai-and-automation-drive-50-faster-software-development-outsystems-and-kpmg-survey-reveals>
python3 run_spiders.py $(echo $url)
```
This will scrape the specified article and save the output in a JSON file.

### 5. View the Output
After running the script, the scraped data will be saved in the ./output directory. The file name will be based on the website name, such as output_digitalterminal.json for Digital Terminal articles.

Sample response format for a Digital Terminal article:

```console
[
  {
    "article_url": "https://digitalterminal.in/trending/ai-and-automation-drive-50-faster-software-development-outsystems-and-kpmg-survey-reveals",
    "title": "AI and Automation Drive 50% Faster Software Development, OutSystems and KPMG Survey Reveals",
    "published_date": "2024-09-14T05:46:35.076Z",
    "article_content": "<content>",
    "category": "Trending"
  }
]
```

## Examples
Here’s how you can use the scraper for different websites:
### Livemint Example
```console
url=https://www.livemint.com/news/india/rg-kar-ex-principal-sandip-ghosh-arrested-by-cbi-in-kolkata-doctors-rape-case-11726331284013.html
python3 run_spiders.py $(echo $url)
```
### Economist Example
```console
url=https://www.economist.com/briefing/2024/09/12/what-will-happen-if-americas-election-result-is-contested
python3 run_spiders.py $(echo $url)
```
### Digital Terminal Example
```console
url=https://digitalterminal.in/trending/ai-and-automation-drive-50-faster-software-development-outsystems-and-kpmg-survey-reveals
python3 run_spiders.py $(echo $url)
```
### Inc42 Example
```console
url=https://inc42.com/buzz/dggi-detected-tax-evasion-of-inr-81875-cr-in-indian-online-gaming-space-in-fy24/
python3 run_spiders.py $(echo $url)
```
### Telegraphindia Example
```console
url=https://www.telegraphindia.com/opinion/junk-living-consumerism-and-dopamine-spike-has-miniaturised-desire/cid/2048086
python3 run_spiders.py $(echo $url)
```
