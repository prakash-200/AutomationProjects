
import requests
import json
import os

def fetch_all_products(base_url):
    all_products = []
    page = 1

    while True:
        url = f"{base_url}?page={page}"
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Error: Unable to fetch data from {url} (Status Code: {response.status_code})")
            break

        try:
            data = response.json()  # Parse JSON response
        except json.JSONDecodeError:
            print(f"Error: Failed to decode JSON from {url}")
            break

        if 'products' not in data or not data['products']:
            print(f"No more products found on page {page}. Stopping.")
            break

        # Add products to the combined list
        all_products.extend(data['products'])
        print(f"Fetched {len(data['products'])} products from page {page} of {base_url}")

        page += 1

    return all_products

def fetch_and_store_data(urls, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for url in urls:
        # Extract a unique name for the file from the URL
        file_name = url.split('/')[-2] + ".json"
        output_file = os.path.join(output_dir, file_name)

        print(f"Processing URL: {url}")
        products = fetch_all_products(url)

        # Save the fetched products to a JSON file
        with open(output_file, "w") as file:
            json.dump(products, file, indent=2)

        print(f"Data from {url} saved to {output_file}. Total products fetched: {len(products)}")


urls = [
    "https://buildpro.store/collections/plumbing/products.json",
    "https://buildpro.store/collections/fittings/products.json",
    "https://buildpro.store/collections/plumbing-accessories/products.json"
]
output_directory = "product_data"

fetch_and_store_data(urls, output_directory)
