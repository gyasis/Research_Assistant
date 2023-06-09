# scripts/web_scraper.py
import requests
from bs4 import BeautifulSoup

def scrape_webpage_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Remove any script or style elements
    for script in soup(['script', 'style']):
        script.extract()

    # Get the text from the page
    page_text = soup.get_text()

    # Remove any leading or trailing whitespace
    page_text = page_text.strip()

    return page_text
