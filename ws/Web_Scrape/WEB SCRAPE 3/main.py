


import requests
from bs4 import BeautifulSoup
import openpyxl

# Function to extract links that start with /products and are inside a specific div
def extract_product_links(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Check if request was successful

        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the div with class 'theme-product-hover-properties'
        product_divs = soup.find_all('div', class_='theme-product-hover-properties')

        # Initialize a set to avoid duplicate links
        links = set()

        # Loop through each div and find the 'a' tags inside it
        for div in product_divs:
            for a_tag in div.find_all('a', href=True):
                link = a_tag['href']
                if link.startswith('/products'):  # Ensure the URL starts with '/products'
                    full_link = 'https://techgurustore.in' + link  # Prepend base URL
                    links.add(full_link)  # Add to set (automatically avoids duplicates)

        return list(links)  # Convert set back to list

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return []

# Function to save links with categories to an Excel file
def save_links_with_categories_to_excel(data, file_name='testing.xlsx'):
    # Create a new workbook and sheet
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Product Links"

    # Add headers to the first row
    sheet['A1'] = "Category"
    sheet['B1'] = "Product Links"

    # Add data rows
    row = 2  # Start writing data from the second row
    for category, links in data.items():
        for link in links:
            sheet[f'A{row}'] = category  # Write category
            sheet[f'B{row}'] = link  # Write product link
            row += 1

    # Save the Excel file
    workbook.save(file_name)
    print(f"Data saved to {file_name}")

# Main function to process multiple URLs with associated categories
def main():
    # Array of URLs
    urls = [
        'https://techgurustore.in/categories/laptop/1282329000020387495',
        'https://techgurustore.in/categories/desktop-pcs/1282329000020387497',
        'https://techgurustore.in/categories/media-storage/1282329000020387499',
        'https://techgurustore.in/categories/tower-rack-storage-server/1282329000020517024',
        'https://techgurustore.in/categories/desktop-server-parts/1282329000020517026',
        'https://techgurustore.in/categories/laptop-parts/1282329000021419131',
        'https://techgurustore.in/categories/computer-peripherals/1282329000020387513',
        'https://techgurustore.in/categories/accessories/1282329000020387509',
        'https://techgurustore.in/categories/cables-and-adapters/1282329000021871442',
        'https://techgurustore.in/categories/mobile-tablet-accessories/1282329000025237361',
        'https://techgurustore.in/categories/wireless-wired-products/1282329000020517004',
        'https://techgurustore.in/categories/security-system/1282329000020387527',
        'https://techgurustore.in/categories/networking-accessories/1282329000020387537',
        'https://techgurustore.in/categories/accounting/1282329000024912139',
        'https://techgurustore.in/categories/antivirus-and-security/1282329000020387553',
        'https://techgurustore.in/categories/business-apps/1282329000024505193',
        'https://techgurustore.in/categories/backup-and-recovery/1282329000020387555',
        'https://techgurustore.in/categories/education-software/1282329000024912145',
        'https://techgurustore.in/categories/engineers-architect/1282329000025033094',
        'https://techgurustore.in/categories/network-tools-software/1282329000024912143',
        'https://techgurustore.in/categories/operating-systems/1282329000020387551',
        'https://techgurustore.in/categories/remote-software/1282329000024912141'
    ]

    # Array of categories corresponding to the URLs
    categories = [
        'Laptop',
        'Desktop',
        'Media Storage',
        'Rack',
        'CPU Parts',
        'Laptop Parts',
        'Computer Peripherals',
        'desktop Accessories',
        'Cables & Adapters',
        'Mobile & Tablet Accessories',
        'Wireless & Wired Accessories',
        'Security System',
        'Network Accessories',
        'Accounting',
        'Antivirus & Security',
        'Business Apps',
        'Backup & Recovery',
        'Education Software',
        'Engineers & Architect',
        'Network Tools Software',
        'Operating System',
        'Remote Software'
     ]

    # Ensure the lengths of the arrays match
    if len(urls) != len(categories):
        print("Error: The number of URLs must match the number of categories.")
        return

    # Dictionary to hold categories and their associated links
    category_links = {}

    # Process each URL
    for url, category in zip(urls, categories):
        print(f"Processing category: {category}, URL: {url}")
        links = extract_product_links(url)
        category_links[category] = links

    # Save the extracted links with categories to an Excel file
    save_links_with_categories_to_excel(category_links)

# Run the script
if __name__ == "__main__":
    main()
