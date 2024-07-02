import requests
from bs4 import BeautifulSoup
import re

# Define the URL
url = "https://www.ndtv.com/india"

# Send a GET request to the URL
response = requests.get(url)
response.raise_for_status()  # Raise an exception for HTTP errors

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')


# Find all divs with the class 'article-image'
headings = soup.find_all('h2', class_='newsHdng')

# Extract the text of h3 inside each div
titles = [heading.find('a').text for heading in headings]

for title in titles:
    print(f"Title: {title}")