import requests
from bs4 import BeautifulSoup
from general_handlers import log_error



def scrape_webpage(url):
    """Scrape the text content of a webpage."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text()
    except requests.RequestException as e:
        log_error(f"Failed to fetch {url}: {e}")
        return ""

def encode_urls(text):
    """Encode URLs in the text by replacing 'https://' with 'https_//'."""
    return text.replace('https://', 'https_//')
