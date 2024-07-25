# website_pages.py

from web_handlers.web_crawler import crawl_website
from web_handlers.sitemap_handlers import check_robots_txt, check_sitemap_in_robots

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python main.py <domain> [<crawl_depth>]")
        sys.exit(1)

    domain = sys.argv[1]
    crawl_depth = int(sys.argv[2]) if len(sys.argv) == 3 else 5

    if not domain.startswith("http://") and not domain.startswith("https://"):
        domain = "https://" + domain

    root_url = domain

    # Check for robots.txt and store its content if exists
    robots_txt_content = check_robots_txt(root_url)
    sitemap_urls = check_sitemap_in_robots(robots_txt_content) if robots_txt_content else []

    # Crawl sitemap URLs if found
    if sitemap_urls:
        for sitemap_url in sitemap_urls:
            internal_links, external_links, sitemap_links = crawl_website(sitemap_url, crawl_depth, is_sitemap=True)
            print(f"Sitemap Links from {sitemap_url}:\n{sitemap_links}")

    # Always crawl the root URL
    internal_links, external_links, sitemap_links = crawl_website(root_url, crawl_depth, is_sitemap=False)
    print(f"Internal Links:\n{internal_links}")
    print(f"External Links:\n{external_links}")
    print(f"Sitemap Links:\n{sitemap_links}")
