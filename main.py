import requests
import csv
import json
import logging
import argparse
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# Set up logging
logging.basicConfig(filename='web_scraper.log', level=logging.INFO)

# Set up command-line arguments
parser = argparse.ArgumentParser(description='Web scraper')
parser.add_argument('base_url', help='The base URL of the website to scrape')
parser.add_argument('num_pages', type=int, help='The number of pages to scrape')
parser.add_argument('tag', help='The HTML tag to scrape')
parser.add_argument('--class_name', help='The class of the HTML tag to scrape (optional)')
parser.add_argument('--format', choices=['csv', 'json'], default='csv', help='The format to save the data in (default: csv)')
args = parser.parse_args()

# Define the function to scrape a page
def scrape_page(page_num):
    url = args.base_url + str(page_num)
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.HTTPError as http_err:
        logging.error(f'HTTP error occurred on page {page_num}: {http_err}')
        return
    except Exception as err:
        logging.error(f'Other error occurred on page {page_num}: {err}')
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    if args.class_name:
        data = soup.find_all(args.tag, class_=args.class_name)
    else:
        data = soup.find_all(args.tag)

    if args.format == 'csv':
        with open('data.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for item in data:
                writer.writerow([item.text])
    elif args.format == 'json':
        with open('data.json', 'a') as jsonfile:
            for item in data:
                json.dump(item.text, jsonfile)

    logging.info(f'Successfully scraped page {page_num}')

# Use multithreading to scrape multiple pages at the same time
with ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(scrape_page, range(1, args.num_pages + 1))