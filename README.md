#Web Scraper
This Python script is a web scraper that fetches data from a user-specified website and stores it in a CSV file.

How it works
The script prompts the user to enter the base URL of the website they want to scrape and the number of pages to scrape. It then loops through each page, sends a GET request to the page, and handles any HTTP or other errors that might occur during the request.

The script uses BeautifulSoup to parse the HTML response from each page and finds all 'p' tags. The text of each 'p' tag is then written to a CSV file named 'data.csv'.

Dependencies
This script requires the following Python libraries:

requests
csv
BeautifulSoup
Usage
To run the script, simply execute the main.py file in your Python environment. When prompted, enter the base URL of the website you want to scrape (e.g., 'https://example.com/page') and the number of pages to scrape.

Please note that the structure of the website being scraped can affect the results. If the website does not use 'p' tags to store the data you want to scrape, you will need to modify the script to look for the correct tags.
