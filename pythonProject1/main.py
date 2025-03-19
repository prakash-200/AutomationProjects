import requests
import json

def fetch_all_products(base_url):
    all_products = []
    page = 1

    while True:
        url = f"{base_url}?page={page}"
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code != 200:
            print(f"Error: Unable to fetch data from {url} (Status Code: {response.status_code})")
            break

        try:
            data = response.json()  # Parse JSON response
        except json.JSONDecodeError:
            print(f"Error: Failed to decode JSON from {url}")
            break

        # Check if 'products' key exists and is not empty
        if 'products' not in data or not data['products']:
            print(f"No more products found on page {page}. Stopping.")
            break

        # Add products to the combined list
        all_products.extend(data['products'])
        print(f"Fetched {len(data['products'])} products from page {page}")

        # Increment page number
        page += 1

    return all_products

# Example usage
base_url = "https://buildpro.store/collections/showers/products.json"
all_products = fetch_all_products(base_url)

# Save all products to a single JSON file
output_file = "all_products.json"
with open(output_file, "w") as file:
    json.dump(all_products, file, indent=2)

print(f"Total products fetched: {len(all_products)}. Data saved to {output_file}")
