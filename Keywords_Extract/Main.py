#
# import requests
# from bs4 import BeautifulSoup
#
# def extract_seo_keywords(url):
#     try:
#         # Add a User-Agent header to mimic a browser request
#         headers = {
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
#         }
#
#         # Fetch the page content
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()  # Raise an error for bad responses
#
#         # Parse the HTML content
#         soup = BeautifulSoup(response.text, 'html.parser')
#
#         # Extract meta keywords
#         meta_keywords = ''
#         meta_tag = soup.find('meta', attrs={'name': 'keywords'})
#         if meta_tag and 'content' in meta_tag.attrs:
#             meta_keywords = meta_tag['content']
#
#         # Display results
#         print("SEO Keywords (Meta):", meta_keywords)
#
#         return {
#             "meta_keywords": meta_keywords
#         }
#
#     except Exception as e:
#         print("Error:", e)
#         return None
#
# # Example Usage
# if __name__ == "__main__":
#     url = input("Enter the URL: ")
#     print("Fetching SEO keywords...")
#     seo_data = extract_seo_keywords(url)
#     if seo_data:
#         print("\nExtraction Complete!")

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time


def extract_seo_keywords(url):
    try:
        # Add a User-Agent header to mimic a browser request
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        # Fetch the page content
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract meta keywords
        meta_keywords = ''
        meta_tag = soup.find('meta', attrs={'name': 'keywords'})
        if meta_tag and 'content' in meta_tag.attrs:
            meta_keywords = meta_tag['content']

        # Display results
        print("SEO Keywords (Meta):", meta_keywords)

        return {
            "meta_keywords": meta_keywords
        }

    except Exception as e:
        print("Error:", e)
        return None


def get_all_page_urls(main_url):
    try:
        # Add a User-Agent header to mimic a browser request
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        # Initialize sets for URLs
        visited_urls = set()
        urls_to_visit = set([main_url])

        # Parse the domain to avoid external links
        base_domain = urlparse(main_url).netloc

        print("\nCrawling for all URLs. This may take some time...")

        while urls_to_visit:
            current_url = urls_to_visit.pop()
            if current_url in visited_urls:
                continue

            try:
                response = requests.get(current_url, headers=headers, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')

                # Mark the current URL as visited
                visited_urls.add(current_url)
                print(f"Visited: {current_url}")

                # Find and parse all links on the current page
                for link in soup.find_all('a', href=True):
                    full_url = urljoin(current_url, link['href'])
                    if urlparse(full_url).netloc == base_domain and full_url not in visited_urls:
                        urls_to_visit.add(full_url)

                # Sleep to avoid overloading the server
                time.sleep(0.5)
            except Exception as e:
                print(f"Error visiting {current_url}: {e}")

        print("\nAll Page URLs Crawled:")
        for url in visited_urls:
            print(url)
        print(f"\nTotal URLs Found: {len(visited_urls)}")
        return visited_urls

    except Exception as e:
        print("Error fetching URLs:", e)
        return None


# Example Usage
if __name__ == "__main__":
    main_url = input("Enter the main page URL: ")
    print("\nFetching all page URLs...")
    all_urls = get_all_page_urls(main_url)
    if all_urls:
        print(f"\nTotal URLs Found: {len(all_urls)}")
