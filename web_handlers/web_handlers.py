#web_handlers.py

import requests
from bs4 import BeautifulSoup
from misc_handlers import log_error
import re
from urllib.parse import urlparse, urlunparse, urljoin
import logging


def extract_urls(text):
    """Extract all URLs from the given text."""
    return re.findall(r'https?://\S+', text)

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

def normalize_url(url, base_url=None, ignore_scheme=True):
    if base_url:
        url = urljoin(base_url, url)
    parsed_url = urlparse(url)
    scheme = 'https' if ignore_scheme else parsed_url.scheme
    netloc = parsed_url.netloc.replace('www.', '')  # Remove www.
    normalized_url = urlunparse(parsed_url._replace(scheme=scheme, netloc=netloc, query='', fragment=''))
    if normalized_url.endswith('/'):
        normalized_url = normalized_url[:-1]
    return normalized_url

def is_internal_url(base_url, url):
    base_domain = urlparse(base_url).netloc
    target_domain = urlparse(url).netloc
    return base_domain == target_domain

def get_http_status(url):
    try:
        response = requests.head(url, timeout=10)
        return response.status_code
    except requests.RequestException as e:
        return str(e)
    
def is_content_page(url):
    content_extensions = (
        '.php', '.pdf', '.html', '.htm', '.asp', '.aspx', '.jsp', '.jspx',
        '.cgi', '.pl', '.cfm', '.xml', '.json', '.md', '.txt'
    )
    media_extensions = (
        '.jpg', '.jpeg', '.gif', '.webp', '.png', '.bmp', '.svg', '.ico',
        '.tif', '.tiff', '.mp4', '.mkv', '.webm', '.mp3', '.wav', '.ogg',
        '.avi', '.mov', '.wmv', '.flv', '.swf', '.m4a', '.m4v', '.aac',
        '.3gp', '.3g2', '.midi', '.mid', '.wma', '.aac', '.ra', '.ram', 
        '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.odt', 
        '.ods', '.odp'
    )
    if any(url.lower().endswith(ext) for ext in content_extensions):
        return True
    if any(url.lower().endswith(ext) for ext in media_extensions):
        return False
    return True

