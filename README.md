# python-tools
Python functions to handle folders and other common stuff


#website_urls.py
#example usage: 

# another_script.py

from website_urls import get_website_urls

domain = "https://mysitefaster.com"
crawl_depth = 5

internal_links, external_links, sitemap_links = get_website_urls(domain, crawl_depth)

print(f"Internal Links:\n{internal_links}")
print(f"External Links:\n{external_links}")
print(f"Sitemap Links:\n{sitemap_links}")
