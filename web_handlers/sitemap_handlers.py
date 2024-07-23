
#sitemap_handlers

import requests
from urllib.parse import urlparse
from xml.etree import ElementTree as ET

def check_robots_txt(url):
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    robots_url = f"{base_url}/robots.txt"
    
    try:
        response = requests.get(robots_url, timeout=10)
        if response.status_code == 200:
            print(f"robots.txt found at {robots_url}")
            return response.text
        else:
            print(f"robots.txt not found at {robots_url}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error accessing {robots_url}: {e}")
        return None

def check_sitemap_in_robots(robots_txt_content):
    lines = robots_txt_content.splitlines()
    sitemaps = [line.split(':', 1)[1].strip() for line in lines if line.lower().startswith('sitemap:')]
    if sitemaps:
        for sitemap in sitemaps:
            print(sitemap)
        return sitemaps
    else:
        print("No sitemap found in robots.txt.")
        return []