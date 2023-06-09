# scripts/website_downloader.py
import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from scripts.web_scraper import scrape_webpage_text

def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_website_links(url):
    urls = set()
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            continue
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid(href):
            continue
        if href in internal_urls:
            continue
        if domain_name not in href:
            continue
        urls.add(href)
        internal_urls.add(href)
    return urls

def download_website(url, delay=3):
    print(f"Crawling: {url}")
    links = get_all_website_links(url)
    for link in links:
        if link not in internal_urls:
            time.sleep(delay) 
            page_text = scrape_webpage_text(link)
            page_path = os.path.join('downloaded_pages', link.replace("http://", "").replace("https://", "") + '.txt')
            os.makedirs(os.path.dirname(page_path), exist_ok=True)
            with open(page_path, 'w') as f:
                f.write(page_text)
            download_website(link)
