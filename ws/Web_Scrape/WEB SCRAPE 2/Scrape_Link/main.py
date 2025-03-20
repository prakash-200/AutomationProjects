
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Function to scrape product links from a page
def scrape_product_links(page_url):
    # Set up Selenium WebDriver
    options = Options()
    options.add_argument("--headless")  # Run in headless mode (no browser window)
    options.add_argument("--disable-gpu")  # Disable GPU acceleration (optional)
    options.add_argument("--no-sandbox")  # For Linux, disable sandbox (optional)

    # Specify path to ChromeDriver if it's not in your PATH
    driver = webdriver.Chrome(options=options)  # Ensure ChromeDriver is in your PATH

    # Load the page and wait for it to load completely
    print(f"Loading page: {page_url}")
    driver.get(page_url)
    print("Waiting for the page to fully load...")
    time.sleep(1.5)  # Wait for at least 3 seconds for the page to load

    # Scrape the product links
    print(f"Scraping page: {page_url}")
    product_links = []

    try:
        # Find all product links with class "snippet"
        product_elements = driver.find_elements(By.CSS_SELECTOR, 'a.snippet')  # Using the "snippet" class

        # Extract the links from the href attribute
        for element in product_elements:
            link = element.get_attribute("href")
            if link:
                product_links.append(link)

    except Exception as e:
        print(f"Error scraping links: {e}")
    finally:
        # Close the WebDriver
        driver.quit()

    return product_links

# Function to save data to Excel
def save_to_excel(data, filename):
    # Save the extracted data to Excel
    df = pd.DataFrame(data, columns=['Category', 'Value', 'URL'])
    try:
        df.to_excel(filename, index=False)
        print(f"Data saved to {filename}")
    except PermissionError as e:
        print(f"Permission error: {e}")
        print(f"Please ensure the file is not open or try saving with a different name.")

# Function to scrape links with pagination and save them in a single dataset
def scrape_links_with_pagination(base_url, category, value, all_data, output_file):
    page_number = 0  # Start from the provided URL without any `po` parameter
    modified_url = f"{base_url}#ps=60;"  # First iteration with #ps=60;

    while True:
        if page_number > 0:
            modified_url = f"{base_url}#ps=60;po={page_number};"

        print(f"Scraping URL: {modified_url}")
        product_links = scrape_product_links(modified_url)

        # If no links are found, stop the process
        if not product_links:
            print(f"No product links found for URL: {modified_url}. Stopping process.")
            break

        # Add the links to the dataset
        for link in product_links:
            all_data.append([category, value, link])

        # Save data incrementally
        save_to_excel(all_data, output_file)

        print(f"Scraped {len(product_links)} links from URL: {modified_url}.")
        print("<!----------------------------------------------------------------------------------------------------!>")

        # Increment page number by 60 for the next iteration
        page_number += 60

        # Wait a few seconds for the page to fully load before moving to the next page
        print("Waiting for the page to fully load...")
        time.sleep(3)  # Wait for 3 seconds for the page to load

# Main function to control the flow
def main():
    # Read URLs and categories from an Excel file
    input_file = "./scraped_categories.xlsx"  # Input Excel file containing URLs, categories, and values
    output_file = "siemens.xlsx"  # Output Excel file for all data

    try:
        input_data = pd.read_excel(input_file)
    except FileNotFoundError as e:
        print(f"Input file not found: {e}")
        return

    if 'URL' not in input_data.columns or 'Category' not in input_data.columns or 'Value' not in input_data.columns or 'Page' not in input_data.columns:
        print("Input Excel must contain 'URL', 'Category', 'Value', and 'Page' columns.")
        return

    all_data = []  # To store all scraped data

    # Process each URL, category, and value
    for idx, row in input_data.iterrows():
        url = row['URL']
        category = row['Category']
        value = row['Value']
        page_value = row['Page']

        if page_value == 1:
            # If 'Page' column value is 1, store the URL directly without scraping
            all_data.append([category, value, url])
            print(f"Page value is 1, storing URL directly: {url}")
        else:
            print(f"Scraping category: {category}, value: {value}, URL: {url}")
            scrape_links_with_pagination(url, category, value, all_data, output_file)

    # Save the final data
    save_to_excel(all_data, output_file)

if __name__ == "__main__":
    main()



