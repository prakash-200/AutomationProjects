import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Function to extract links and sub-category from a URL
def extract_data(url):
    logging.info(f"Extracting data from {url}")

    # Send a GET request to the URL
    response = requests.get(url)

    if response.status_code == 200:
        logging.info(f"Successfully fetched the page: {url}")

        # Parse the page content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the sub-category name from the specific div
        sub_category_tag = soup.find('div',
                                     class_='text-[20px] leading-[30px] font-semibold text-black clear-left mb-3')
        sub_category = sub_category_tag.text.strip() if sub_category_tag else 'Not Available'
        logging.info(f"Sub-category found: {sub_category}")

        # Extract all anchor tag links within a specific container class
        links = []
        container = soup.find('div', class_='container')  # Change this to your desired container class

        if container:
            anchor_tags = container.find_all('a', href=True)  # Find all anchor tags with href inside the container
            for link in anchor_tags:
                # Extract the sub-category from the div inside the <a> tag
                sub_category_in_link_tag = link.find('div',
                                                     class_='text-[20px] leading-[30px] font-semibold text-black clear-left mb-3')
                sub_category_from_link = sub_category_in_link_tag.text.strip() if sub_category_in_link_tag else 'Not Available'

                # Prepend the base URL to the relative links
                full_link = f"https://www.lubipumps.com{link['href']}"
                links.append([sub_category_from_link, full_link])

        logging.info(f"Found {len(links)} links in the container.")
        return links
    else:
        logging.error(f"Error: Failed to fetch {url}, Status Code: {response.status_code}")
        return []


# Function to save data into Excel
def save_to_excel(urls, output_file='extracted_data.xlsx'):
    all_data = []
    logging.info(f"Starting to process {len(urls)} URLs...")

    for url in urls:
        logging.info(f"Processing URL: {url}")
        category = url.split('/')[-2]  # Extract category from URL (the second to last part of the URL path)
        links = extract_data(url)

        if links:
            # Append data for each link
            for sub_category_from_link, link in links:
                all_data.append([category, sub_category_from_link, link])

    # Create a DataFrame
    df = pd.DataFrame(all_data, columns=['Category', 'Sub-Category', 'Link'])

    # Save to Excel
    df.to_excel(output_file, index=False)

    logging.info(f"Data saved to {output_file}")


# List of URLs to process
urls = [
    'https://www.lubipumps.com/product-category/borewell-submersible-pumps/',
    'https://www.lubipumps.com/product-category/centrifugal-monoblock-pumps/',
    'https://www.lubipumps.com/product-category/coolant-pumps/',
    'https://www.lubipumps.com/product-category/drainage-sewage-pumps/',
    'https://www.lubipumps.com/product-category/end-suction-pumps/',
    'https://www.lubipumps.com/product-category/fire-fighting-pump-sets/',
    'https://www.lubipumps.com/product-category/horizontal-split-case-pump/',
    'https://www.lubipumps.com/product-category/induction-motor/',
    'https://www.lubipumps.com/product-category/multistage-centrifugal-pumps/',
    'https://www.lubipumps.com/product-category/openwell-submersible-pumps/',
    'https://www.lubipumps.com/product-category/pressure-booster-systems/',
    'https://www.lubipumps.com/product-category/pump-controllers/',
    'https://www.lubipumps.com/product-category/self-priming-monoblock-pumps/',
    'https://www.lubipumps.com/product-category/self-priming-centrifugal-pumps/',
    'https://www.lubipumps.com/product-category/submerged-centrifugal-pumps/',
    'https://www.lubipumps.com/product-category/vertical-inline-pumps/',
    'https://www.lubipumps.com/product-category/vertical-multistage-pumps/',
    'https://www.lubipumps.com/product-category/swimming-pool-pump/',
    'https://www.lubipumps.com/product-category/hvac-systems/',
    'https://www.lubipumps.com/product-category/hpn-systems/',
]

# Run the function to save extracted data into Excel
save_to_excel(urls)
