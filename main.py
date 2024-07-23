# main.py

import requests
from urllib.parse import urlparse
from web_handlers import normalize_url, get_http_status, is_internal_url, is_content_page, log_error, parse_html, parse_sitemap, crawl_website, check_robots_txt, check_sitemap_in_robots
