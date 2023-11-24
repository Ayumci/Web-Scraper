import requests
import csv
from bs4 import BeautifulSoup

url = input("Enter a URL from the website you want to scrape: ")
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
data = soup.find_all('p')
with open('data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for item in data:
        writer.writerow([item.text])