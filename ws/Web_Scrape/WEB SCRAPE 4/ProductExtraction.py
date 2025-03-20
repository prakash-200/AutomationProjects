import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to extract product details from a URL
def extract_product_data(url):
    logging.info(f"Extracting data from {url}")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch {url}. Error: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    # Locate the product containers
    containers = soup.find_all('a', class_='col-span-2 p-3 border border-gray-200 bg-gray-50 rounded-xl mb-[24px] hover:border-blue-lubi cursor-pointer hover:bg-blue-lubi hover:bg-opacity-5 transition-all')

    all_product_data = []

    for tag in containers:
        product_data = {
            'Product Image': '',
            'Product Title': '',
            'Flow Range': '',
            'Head Range': '',
            'Rating': '',
            'Rated Speed': ''
        }

        # Extract product image
        img_tag = tag.find('img', {'data-src': True})
        if img_tag:
            product_data['Product Image'] = img_tag['data-src']

        # Extract product title
        title_tag = tag.find('div', class_='text-[20px] leading-[30px] font-semibold text-black clear-left mb-3')
        if title_tag:
            product_data['Product Title'] = title_tag.get_text(strip=True)

        # Extract specifications
        specs_div = tag.find('div', class_='flex-grow flex-shrink-0 order-5 w-full lg:w-auto lg:order-4')
        if specs_div:
            specs = specs_div.find_all('li')
            for spec in specs:
                text = spec.get_text(strip=True).lower()
                if 'flow range' in text:
                    product_data['Flow Range'] = text.split(':')[-1].strip()
                elif 'head range' in text:
                    product_data['Head Range'] = text.split(':')[-1].strip()
                elif 'rating' in text:
                    product_data['Rating'] = text.split(':')[-1].strip()
                elif 'rated speed' in text:
                    product_data['Rated Speed'] = text.split(':')[-1].strip()

        all_product_data.append(product_data)

    return all_product_data

# Function to process URLs and write extracted data to Excel row by row
def process_urls_from_excel(input_file, output_file='extracted_product_data.xlsx'):
    df = pd.read_excel(input_file)
    column_names = list(df.columns) + ['Product Image', 'Product Title', 'Flow Range', 'Head Range', 'Rating', 'Rated Speed']

    # Create the output file with headers if it doesn't exist
    if not os.path.exists(output_file):
        pd.DataFrame(columns=column_names).to_excel(output_file, index=False)

    for _, row in df.iterrows():
        url = row['Link']  # Adjust column name to match your input file
        logging.info(f"Processing URL: {url}")

        product_data_list = extract_product_data(url)
        if product_data_list:
            for product_data in product_data_list:
                row_data = row.tolist() + list(product_data.values())
                new_row = pd.DataFrame([row_data], columns=column_names)

                # Append the new row to the existing file
                with pd.ExcelWriter(output_file, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                    new_row.to_excel(writer, index=False, header=False, startrow=writer.sheets['Sheet1'].max_row)

                logging.info(f"Data for {url} added to {output_file}")
        else:
            logging.warning(f"No products found at {url}")

# Input Excel file containing URLs
input_excel_file = './extracted_data - Copy.xlsx'

# Run the function
process_urls_from_excel(input_excel_file)
