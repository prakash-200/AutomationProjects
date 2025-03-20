#
#
# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
# import re
#
#
# def scrape_links_to_excel(url):
#     base_url = "https://in.rsdelivers.com/"  # Base URL to concatenate
#
#     response = requests.get(url)
#     response.raise_for_status()
#
#     soup = BeautifulSoup(response.text, 'html.parser')
#
#     # Find all category divs
#     category_divs = soup.find_all('div', class_=re.compile(r'accordion-component-module_title__.*'))
#
#     all_data = []
#
#     for category_div in category_divs:
#         # Extract the category name
#         category_name = category_div.get_text(strip=True).split('(')[0].strip()
#
#         # Find the parent div to locate sub-category links
#         parent_div = category_div.find_parent('div', class_=re.compile(r'accordion-component-module_accordion__.*'))
#         if not parent_div:
#             continue
#
#         # Find sub-category link divs
#         link_divs = parent_div.find_all('div', class_=re.compile(r'categories-list-component_sub-category__.*'))
#
#         for link_div in link_divs:
#             # Find the <a> tag within the div
#             link = link_div.find('a')
#             if link:
#                 # Extract the value and URL from the <a> tag
#                 value = link.get_text(strip=True).split('(')[0].strip()
#                 href = link.get('href')
#
#                 if value and href:
#                     full_url = base_url + href.lstrip('/')  # Concatenate base URL with href
#                     all_data.append([category_name, value, full_url])
#
#     # Convert data to DataFrame
#     df = pd.DataFrame(all_data, columns=['Category', 'Value', 'URL'])
#
#     # Save to Excel
#     excel_file_name = f"scraped_categories.xlsx"
#     df.to_excel(excel_file_name, index=False)
#
#     print(f"Data saved to {excel_file_name}")
#
#
# # Example usage
# url = "https://in.rsdelivers.com/ourbrands/siemens"  # Replace with your target URL
# scrape_links_to_excel(url)


import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def scrape_links_to_excel(url):
    base_url = "https://in.rsdelivers.com/"  # Base URL to concatenate

    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all category divs
    category_divs = soup.find_all('div', class_=re.compile(r'accordion-component-module_title__.*'))

    all_data = []

    for category_div in category_divs:
        # Extract the category name
        category_name = category_div.get_text(strip=True).split('(')[0].strip()

        # Find the parent div to locate sub-category links
        parent_div = category_div.find_parent('div', class_=re.compile(r'accordion-component-module_accordion__.*'))
        if not parent_div:
            continue

        # Find sub-category link divs
        link_divs = parent_div.find_all('div', class_=re.compile(r'categories-list-component_sub-category__.*'))

        for link_div in link_divs:
            # Find the <a> tag within the div
            link = link_div.find('a')
            if link:
                # Extract the value and URL from the <a> tag
                value = link.get_text(strip=True).split('(')[0].strip()
                href = link.get('href')

                # Extract the number value inside parentheses (if any)
                page_number = None
                match = re.search(r'\((\d+)\)', link.get_text())
                if match:
                    page_number = match.group(1)

                if value and href:
                    full_url = base_url + href.lstrip('/')  # Concatenate base URL with href
                    # Append the data including the page number
                    all_data.append([category_name, value, page_number, full_url])

    # Convert data to DataFrame
    df = pd.DataFrame(all_data, columns=['Category', 'Value', 'Page', 'URL', ])

    # Save to Excel
    excel_file_name = f"scraped_categories.xlsx"
    df.to_excel(excel_file_name, index=False)

    print(f"Data saved to {excel_file_name}")

# Example usage
url = "https://in.rsdelivers.com/ourbrands/siemens"
scrape_links_to_excel(url)
