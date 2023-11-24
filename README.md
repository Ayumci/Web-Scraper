# Web Scraper

This script scrapes a website for specific HTML tags and saves the data in a CSV or JSON file.

## Usage

Run the script with the following command-line arguments:

```bash
python main.py base_url num_pages tag --class_name class_name --format format
```
base_url: The base URL of the website to scrape.
num_pages: The number of pages to scrape.
tag: The HTML tag to scrape.
class_name (optional): The class of the HTML tag to scrape.
format (optional): The format to save the data in (csv or json). Default is csv.
The script respects the website's robots.txt file and uses multithreading to scrape multiple pages at the same time. It logs the progress and any errors to a file named 'web_scraper.log'.

Requirements:

Python 3

requests

BeautifulSoup

urllib


