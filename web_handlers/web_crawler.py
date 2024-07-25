# web_crawler.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from misc_handlers import log_error

def parse_html(url):
    """
    Parse an HTML page to extract links.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return [link['href'] for link in soup.find_all('a', href=True)]
    except requests.RequestException as e:
        log_error(f"Failed to fetch {url}: {e}")
        return []

def parse_sitemap(url):
    """
    Parse an XML sitemap to extract links.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'xml')
        return [loc.text for loc in soup.find_all('loc')]
    except requests.RequestException as e:
        log_error(f"Failed to fetch {url}: {e}")
        return []

def crawl_website(root_url, crawl_depth=5, is_sitemap=False):
    """
    Recursively crawl a website starting from the root URL up to the specified depth.
    Collects internal links and external links, their status, and the URLs where they are found.
    
    Parameters:
    root_url (str): The root URL to start crawling from.
    crawl_depth (int): The depth to which the crawler should go. Default is 5.
    is_sitemap (bool): Indicates whether the root URL is a sitemap.
    
    Returns:
    tuple: Three lists of dictionaries containing the internal, external, and sitemap links, their status, and the URLs where they are found.
    """
    from web_handlers import normalize_url, get_http_status, is_internal_url, is_content_page

    internal_links_data = {}
    external_links_data = {}
    sitemap_links_data = []

    visited_urls = set()

    def crawl(url, current_depth):
        if current_depth > crawl_depth or url in visited_urls:
            return
        visited_urls.add(url)

        if is_sitemap:
            links = parse_sitemap(url)
        else:
            links = parse_html(url)

        for link in links:
            link_url = normalize_url(link, base_url=url, ignore_scheme=False)
            if is_internal_url(root_url, link_url) and is_content_page(link_url):
                status = get_http_status(link_url)
                if link_url not in internal_links_data:
                    internal_links_data[link_url] = {
                        'link': link_url,
                        'status': status,
                        'found_at': []
                    }
                internal_links_data[link_url]['found_at'].append(url)
                if not is_sitemap:
                    crawl(link_url, current_depth + 1)
            elif not is_internal_url(root_url, link_url) and not is_sitemap:
                status = get_http_status(link_url)
                if link_url not in external_links_data:
                    external_links_data[link_url] = {
                        'link': link_url,
                        'status': status,
                        'found_at': []
                    }
                external_links_data[link_url]['found_at'].append(url)

        if is_sitemap:
            for link in links:
                if link.endswith('.xml'):
                    crawl(link, current_depth + 1)
                else:
                    status = get_http_status(link)
                    sitemap_links_data.append({
                        'link': link,
                        'status': status,
                        'found_at': [url]
                    })

    crawl(root_url, 0)
    return list(internal_links_data.values()), list(external_links_data.values()), sitemap_links_data
