import subprocess
import os
import sys
from urllib.parse import urlparse

# Define a mapping of spider names and their respective base domains
SPIDER_MAP = {
    'livemint': 'livemint.com',
    'economist': 'economist.com',
    'digitalterminal': 'digitalterminal.in',
    'inc42': 'inc42.com',
    'telegraphindia': 'telegraphindia.com'
    # Add more spiders and their corresponding domains here
}

def get_spider_name(url):
    """
    Determine the spider name based on the URL domain.
    """
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()

    for spider_name, base_domain in SPIDER_MAP.items():
        if base_domain in domain:
            return spider_name
    return None

def run_spider(url):
    """
    Run the appropriate Scrapy spider based on the provided URL.
    """
    spider_name = get_spider_name(url)
    if spider_name is None:
        print(f"No spider found for the URL '{url}'.")
        return

    # Create the output directory if it doesn't exist
    output_dir = './output/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Format output file name based on the spider name
    output_file = f'{output_dir}/output_{spider_name}.json'

    # Run the Scrapy spider using subprocess
    try:
        command = [
            'scrapy', 'crawl', spider_name,
            '-a', f'url={url}',
            '-O', output_file
        ]
        print(f"Running: {' '.join(command)}")
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running spider '{spider_name}': {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_spiders.py <url>")
        sys.exit(1)

    # Get URL from command-line arguments
    url = sys.argv[1]

    # Run the spider based on the URL
    run_spider(url)
