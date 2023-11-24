import requests
import csv
import json
import logging
import argparse
import configparser
import tkinter as tk
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse, urljoin
from urllib.robotparser import RobotFileParser
import xml.etree.ElementTree as ET
import sqlite3

# Set up logging
logging.basicConfig(filename='web_scraper.log', level=logging.INFO)

# Read configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Set up command-line arguments
parser = argparse.ArgumentParser(description='Web scraper')
parser.add_argument('--base_url', default=config.get('DEFAULT', 'base_url'), help='The base URL of the website to scrape')
parser.add_argument('--num_pages', type=int, default=config.getint('DEFAULT', 'num_pages'), help='The number of pages to scrape')
parser.add_argument('--tag', default=config.get('DEFAULT', 'tag'), help='The HTML tag to scrape')
parser.add_argument('--class_name', default=config.get('DEFAULT', 'class_name'), help='The class of the HTML tag to scrape (optional)')
parser.add_argument('--format', choices=['csv', 'json', 'xml', 'sqlite'], default=config.get('DEFAULT', 'format'), help='The format to save the data in (default: csv)')
args = parser.parse_args()

# Set up robots.txt parser
parsed_url = urlparse(args.base_url)
robots_url = urljoin(args.base_url, '/robots.txt')
rp = RobotFileParser()
rp.set_url(robots_url)
rp.read()

# Define the function to scrape a page
def scrape_page(page_num):
    url = args.base_url + str(page_num)
    headers = {'User-Agent': 'Mozilla/5.0'}

    # Check if we're allowed to scrape the page
    if not rp.can_fetch('*', url):
        logging.warning(f'Not allowed to scrape page {page_num} according to robots.txt')
        return

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
    elif args.format == 'xml':
        root = ET.Element("root")
        for item in data:
            ET.SubElement(root, "item").text = item.text
        tree = ET.ElementTree(root)
        tree.write("data.xml")
    elif args.format == 'sqlite':
        conn = sqlite3.connect('data.sqlite')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS data
                     (text text)''')
        for item in data:
            c.execute("INSERT INTO data VALUES (?)", (item.text,))
        conn.commit()
        conn.close()


# Create the GUI
root = tk.Tk()

# Create the fields for the base URL, number of pages, tag, class name, and format
base_url_field = tk.Entry(root)
num_pages_field = tk.Entry(root)
tag_field = tk.Entry(root)
class_name_field = tk.Entry(root)
format_field = tk.Entry(root)

# Create the labels for the fields
base_url_label = tk.Label(root, text="Base URL")
num_pages_label = tk.Label(root, text="Number of pages")
tag_label = tk.Label(root, text="Tag")
class_name_label = tk.Label(root, text="Class name")
format_label = tk.Label(root, text="Format")

# Create the "Start" button
start_button = tk.Button(root, text="Start", command=start_scraping)

# Arrange the fields, labels, and button in a grid
base_url_label.grid(row=0, column=0)
base_url_field.grid(row=0, column=1)
num_pages_label.grid(row=1, column=0)
num_pages_field.grid(row=1, column=1)
tag_label.grid(row=2, column=0)
tag_field.grid(row=2, column=1)
class_name_label.grid(row=3, column=0)
class_name_field.grid(row=3, column=1)
format_label.grid(row=4, column=0)
format_field.grid(row=4, column=1)
start_button.grid(row=5, column=0, columnspan=2)

# Start the GUI
root.mainloop()

def start_scraping():
    # Read the values from the fields
    base_url = base_url_field.get()
    num_pages = int(num_pages_field.get())
    tag = tag_field.get()
    class_name = class_name_field.get()
    data_format = format_field.get()

    # Use a ThreadPoolExecutor to scrape multiple pages at the same time
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(scrape_page, base_url, num_pages, tag, class_name, data_format, page_num) for page_num in range(1, num_pages + 1)]
        for future in futures:
            try:
                # If the future raises an exception, this will re-raise that exception
                future.result()
            except Exception as err:
                logging.error(f'Error occurred during scraping: {err}')

