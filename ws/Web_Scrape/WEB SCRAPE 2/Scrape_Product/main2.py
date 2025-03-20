# import os
# import pandas as pd
# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin
# from PIL import Image
# from io import BytesIO
#
# # Input Excel file
# input_file = "../Scrape_Link/siemens.xlsx"
# output_file = "siemens_product.xlsx"
#
# # Read input Excel file
# data = pd.read_excel(input_file)
#
# # Initialize output data list
# output_data = []
#
# # Create an Excel writer for simultaneous writing
# with pd.ExcelWriter(output_file, engine="openpyxl", mode="w") as writer:
#     # Write initial structure to the file
#     columns = [
#         "Brand",
#         "product",
#         "Category",
#         "URL",
#         "Product Title",
#         "Product Image",
#         "Sales Price",
#         "Regular Price",
#         "Datasheet",
#         "Technical Specification"
#     ]
#     pd.DataFrame(columns=columns).to_excel(writer, index=False)
#
#     # Process each URL
#     for index, row in data.iterrows():
#         model = os.path.basename(input_file).replace(".xlsx", "")
#         product = row.get("Category", "")  # Updated to get 'Category' from input
#         nested_category = row.get("Value", "")  # Updated to get 'Value' from input
#         url = row.get("URL", "")
#
#         print(f"Scraping URL {index + 1}/{len(data)}: {url}")
#
#         try:
#             # Load the page
#             response = requests.get(url)
#             response.raise_for_status()
#             soup = BeautifulSoup(response.content, "html.parser")
#
#             # Extract product title
#             title_tag = soup.find("h1", class_=lambda x: x and x.startswith("title product-detail-page-component_title"))
#             product_title = title_tag.text.strip() if title_tag else ""
#
#             # Extract sales and regular price
#             price_tags = soup.find_all("p", class_=lambda x: x and x.startswith("add-to-basket-cta-component_unit-price"))
#             sales_price = price_tags[0].text.strip() if len(price_tags) > 0 else ""
#             regular_price = price_tags[1].text.strip() if len(price_tags) > 1 else ""
#
#             # Extract product image URL
#             image_div = soup.find("div", class_=lambda x: x and "media-carousel-component_media" in x)
#             image_tag = image_div.find("img") if image_div else None
#             product_image_url = urljoin(url, image_tag["src"]) if image_tag and image_tag.get("src") else ""
#             print(f"Extracted Product Image URL: {product_image_url}")  # Debugging log
#
#             # Save the product image locally if the URL is valid
#             if product_image_url:
#                 try:
#                     image_response = requests.get(product_image_url)
#                     image_response.raise_for_status()
#                     image = Image.open(BytesIO(image_response.content))
#                     image_filename = f"product_image_{index + 1}.jpg"
#                     image.save(image_filename)
#                     product_image_url = image_filename  # Update column to store the local filename
#                 except Exception as e:
#                     print(f"Error saving product image: {e}")
#
#             # Extract datasheet link and ensure it is a PDF
#             datasheet_url = ""
#             datasheet_tag = soup.find("a", class_=lambda x: x and "button-component-module_button-component" in x)
#             if datasheet_tag:
#                 potential_link = urljoin(url, datasheet_tag["href"])
#                 if potential_link.endswith(".pdf"):
#                     datasheet_url = potential_link
#                 else:
#                     # Look for alternative PDF links in the page
#                     pdf_links = [
#                         urljoin(url, a_tag["href"])
#                         for a_tag in soup.find_all("a", href=True)
#                         if a_tag["href"].endswith(".pdf")
#                     ]
#                     if pdf_links:
#                         datasheet_url = pdf_links[0]  # Take the first valid PDF link
#
#             print(f"Extracted Datasheet URL: {datasheet_url}")  # Debugging log
#
#             # Extract technical specifications
#             specs = {}
#             spec_tags = soup.find_all("div", class_=lambda x: x and x.startswith("product-detail-page-component_spec__"))
#             for spec in spec_tags:
#                 label = spec.find("p", class_="snippet product-detail-page-component_label__3S-Gu")
#                 value = spec.find("p", class_="snippet product-detail-page-component_value__2ZiIc")
#                 if label and value:
#                     specs[label.text.strip()] = value.text.strip()
#
#             technical_specification = "; ".join(f"{k}: {v}" for k, v in specs.items())
#
#             # Append data to output list
#             row_data = [
#                 model,
#                 product,
#                 nested_category,
#                 url,
#                 product_title,
#                 product_image_url,  # Store the image URL or local file
#                 sales_price,
#                 regular_price,
#                 datasheet_url,  # Store the datasheet URL
#                 technical_specification
#             ]
#             output_data.append(row_data)
#
#             # Write the row to the Excel file
#             pd.DataFrame([row_data], columns=columns).to_excel(writer, index=False, header=False, startrow=len(output_data))
#
#             print(f"Extracted data for URL {index + 1}: {row_data}")
#             print(f"Data stored to Excel for URL {index + 1}")
#
#         except Exception as e:
#             print(f"Error processing URL {url}: {e}")
#
# print(f"Data extraction completed. Total URLs processed: {len(data)}. Output saved to {output_file}.")
#



# <!--------------------------------------------------------------------------------------!>


# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# import time
#
#
# def get_data_after_page_load(url):
#     # Set up the Chrome WebDriver
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#     driver.get(url)
#
#     # Wait for the page to fully load (you can adjust the time as needed)
#     time.sleep(5)  # Adjust wait time depending on page load speed
#
#     # Example: Extract the datasheets or PDFs from the page
#     try:
#         # Use XPath or CSS selectors to find the elements containing the PDFs or datasheets
#         datasheets = driver.find_elements(By.XPATH,
#                                           "//a[contains(@href, 'pdf')]")  # This XPath searches for links to PDFs
#
#         # Extract links
#         pdf_links = [datasheet.get_attribute("href") for datasheet in datasheets]
#
#         # Check if there are at least 3 links and print the third one
#         if len(pdf_links) >= 3:
#             print("Found the 3rd PDF link:", pdf_links[2])  # Index 2 corresponds to the 3rd item (0-based index)
#         else:
#             print("Less than 3 PDF links found.")
#
#     except Exception as e:
#         print(f"Error occurred: {str(e)}")
#
#     finally:
#         # Close the browser after scraping
#         driver.quit()
#
#
# # Example Usage
# url = "https://in.rsdelivers.com/product/siemens/3va9113-0rl20/siemens-3va9-rcd-160a-3-pole-type-a/2103513?backToResults=1"
# get_data_after_page_load(url)

#
#
# import os
# import pandas as pd
# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin
# from PIL import Image
# from io import BytesIO
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# import time
#
# # Function to get the third PDF link using Selenium
# def get_third_pdf_link(url):
#     # Set up the Chrome WebDriver
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#     driver.get(url)
#
#     # Wait for the page to fully load (you can adjust the time as needed)
#     time.sleep(5)  # Adjust wait time depending on page load speed
#
#     # Example: Extract the datasheets or PDFs from the page
#     try:
#         # Use XPath or CSS selectors to find the elements containing the PDFs or datasheets
#         datasheets = driver.find_elements(By.XPATH,
#                                           "//a[contains(@href, 'pdf')]")  # This XPath searches for links to PDFs
#
#         # Extract links
#         pdf_links = [datasheet.get_attribute("href") for datasheet in datasheets]
#
#         # Check if there are at least 3 links and return the third one
#         if len(pdf_links) >= 3:
#             return pdf_links[2]  # Return the third PDF link (index 2)
#         else:
#             return ""  # Return empty if less than 3 PDF links found
#
#     except Exception as e:
#         print(f"Error occurred: {str(e)}")
#         return ""
#
#     finally:
#         # Close the browser after scraping
#         driver.quit()
#
#
# # Input Excel file
# input_file = "../Scrape_Link/siemens.xlsx"
# output_file = "siemens_product.csv"
#
# # Read input Excel file
# data = pd.read_excel(input_file)
#
# # Define columns for the output
# columns = [
#     "Brand",
#     "product",
#     "Category",
#     "URL",
#     "Product Title",
#     "Product Image",
#     "Sales Price",
#     "Regular Price",
#     "Datasheet",
#     "Technical Specification"
# ]
#
# # Initialize the CSV file with headers (only once)
# if not os.path.exists(output_file):
#     pd.DataFrame(columns=columns).to_csv(output_file, index=False)
#
# # Process each URL
# for index, row in data.iterrows():
#     model = os.path.basename(input_file).replace(".xlsx", "")
#     product = row.get("Category", "")  # Updated to get 'Category' from input
#     nested_category = row.get("Value", "")  # Updated to get 'Value' from input
#     url = row.get("URL", "")
#
#     print(f"Scraping URL {index + 1}/{len(data)}: {url}")
#
#     try:
#         # Load the page
#         response = requests.get(url)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.content, "html.parser")
#
#         # Extract product title
#         title_tag = soup.find("h1", class_=lambda x: x and x.startswith("title product-detail-page-component_title"))
#         product_title = title_tag.text.strip() if title_tag else ""
#
#         # Extract sales and regular price
#         price_tags = soup.find_all("p", class_=lambda x: x and x.startswith("add-to-basket-cta-component_unit-price"))
#         sales_price = price_tags[0].text.strip() if len(price_tags) > 0 else ""
#         regular_price = price_tags[1].text.strip() if len(price_tags) > 1 else ""
#
#         # Extract product image URL
#         image_div = soup.find("div", class_=lambda x: x and "media-carousel-component_media" in x)
#         image_tag = image_div.find("img") if image_div else None
#         product_image_url = urljoin(url, image_tag["src"]) if image_tag and image_tag.get("src") else ""
#         print(f"Extracted Product Image URL: {product_image_url}")  # Debugging log
#
#         # Save the product image locally if the URL is valid
#         if product_image_url:
#             try:
#                 image_response = requests.get(product_image_url)
#                 image_response.raise_for_status()
#                 image = Image.open(BytesIO(image_response.content))
#                 image_filename = f"product_image_{index + 1}.jpg"
#                 image.save(image_filename)
#                 product_image_url = image_filename  # Update column to store the local filename
#             except Exception as e:
#                 print(f"Error saving product image: {e}")
#
#         # Extract the third PDF link using Selenium
#         datasheet_url = get_third_pdf_link(url)
#         print(f"Extracted Datasheet URL: {datasheet_url}")  # Debugging log
#
#         # Extract technical specifications
#         specs = {}
#         spec_tags = soup.find_all("div", class_=lambda x: x and x.startswith("product-detail-page-component_spec__"))
#         for spec in spec_tags:
#             label = spec.find("p", class_="snippet product-detail-page-component_label__3S-Gu")
#             value = spec.find("p", class_="snippet product-detail-page-component_value__2ZiIc")
#             if label and value:
#                 specs[label.text.strip()] = value.text.strip()
#
#         technical_specification = "; ".join(f"{k}: {v}" for k, v in specs.items())
#
#         # Append data to output list
#         row_data = [
#             model,
#             product,
#             nested_category,
#             url,
#             product_title,
#             product_image_url,  # Store the image URL or local file
#             sales_price,
#             regular_price,
#             datasheet_url,  # Store the third PDF datasheet URL
#             technical_specification
#         ]
#
#         # Write data to CSV immediately (append mode)
#         pd.DataFrame([row_data], columns=columns).to_csv(output_file, index=False, header=False, mode='a')
#
#         print(f"Extracted data for URL {index + 1}: {row_data}")
#         print(f"Data stored for URL {index + 1}")
#
#     except Exception as e:
#         print(f"Error processing URL {url}: {e}")
#
# print(f"Data extraction completed. Total URLs processed: {len(data)}. Output saved to {output_file}.")
#
#




#
# import os
# import pandas as pd
# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin
# from PIL import Image
# from io import BytesIO
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# import time
#
# # Function to extract meta tags (keywords and description) from the page
# def extract_meta_tags(url):
#     response = requests.get(url)
#
#     if response.status_code != 200:
#         print("Failed to retrieve the page")
#         return '', ''
#
#     soup = BeautifulSoup(response.content, 'html.parser')
#
#     description = soup.find('meta', attrs={'name': 'description'})
#     keywords = soup.find('meta', attrs={'name': 'keywords'})
#
#     meta_description = description['content'] if description else 'No description found'
#     meta_keywords = keywords['content'] if keywords else 'No keywords found'
#
#     return meta_description, meta_keywords
#
#
# # Function to get the third PDF link using Selenium
# def get_third_pdf_link(url):
#     # Set up the Chrome WebDriver
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#     driver.get(url)
#
#     # Wait for the page to fully load (you can adjust the time as needed)
#     time.sleep(5)  # Adjust wait time depending on page load speed
#
#     # Example: Extract the datasheets or PDFs from the page
#     try:
#         # Use XPath or CSS selectors to find the elements containing the PDFs or datasheets
#         datasheets = driver.find_elements(By.XPATH,
#                                           "//a[contains(@href, 'pdf')]")  # This XPath searches for links to PDFs
#
#         # Extract links
#         pdf_links = [datasheet.get_attribute("href") for datasheet in datasheets]
#
#         # Check if there are at least 3 links and return the third one
#         if len(pdf_links) >= 3:
#             return pdf_links[2]  # Return the third PDF link (index 2)
#         else:
#             return ""  # Return empty if less than 3 PDF links found
#
#     except Exception as e:
#         print(f"Error occurred: {str(e)}")
#         return ""
#
#     finally:
#         # Close the browser after scraping
#         driver.quit()
#
#
# # Input Excel file
# input_file = "../Scrape_Link/siemens.xlsx"
# output_file = "siemens_product.csv"
#
# # Read input Excel file
# data = pd.read_excel(input_file)
#
# # Define columns for the output
# columns = [
#     "Brand",
#     "product",
#     "Category",
#     "URL",
#     "Product Title",
#     "Product Image",
#     "Sales Price",
#     "Regular Price",
#     "Datasheet",
#     "Technical Specification",
#     "Meta Description",  # New column for meta description
#     "Meta Keywords"  # New column for meta keywords
# ]
#
# # Check if output file exists and initialize CSV with headers if necessary
# if not os.path.exists(output_file):
#     print(f"Creating a new CSV file: {output_file}")
#     pd.DataFrame(columns=columns).to_csv(output_file, index=False)  # Initialize with headers
#
# # Process each URL
# for index, row in data.iterrows():
#     model = os.path.basename(input_file).replace(".xlsx", "")
#     product = row.get("Category", "")  # Updated to get 'Category' from input
#     nested_category = row.get("Value", "")  # Updated to get 'Value' from input
#     url = row.get("URL", "")
#
#     print(f"Scraping URL {index + 1}/{len(data)}: {url}")
#
#     try:
#         # Load the page
#         response = requests.get(url)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.content, "html.parser")
#
#         # Extract product title
#         title_tag = soup.find("h1", class_=lambda x: x and x.startswith("title product-detail-page-component_title"))
#         product_title = title_tag.text.strip() if title_tag else ""
#
#         # Extract sales and regular price
#         price_tags = soup.find_all("p", class_=lambda x: x and x.startswith("add-to-basket-cta-component_unit-price"))
#         sales_price = price_tags[0].text.strip() if len(price_tags) > 0 else ""
#         regular_price = price_tags[1].text.strip() if len(price_tags) > 1 else ""
#
#         # Extract product image URL
#         image_div = soup.find("div", class_=lambda x: x and "media-carousel-component_media" in x)
#         image_tag = image_div.find("img") if image_div else None
#         product_image_url = urljoin(url, image_tag["src"]) if image_tag and image_tag.get("src") else ""
#         print(f"Extracted Product Image URL: {product_image_url}")  # Debugging log
#
#         # Save the product image locally if the URL is valid
#         if product_image_url:
#             try:
#                 image_response = requests.get(product_image_url)
#                 image_response.raise_for_status()
#                 image = Image.open(BytesIO(image_response.content))
#                 image_filename = f"product_image_{index + 1}.jpg"
#                 image.save(image_filename)
#                 product_image_url = image_filename  # Update column to store the local filename
#             except Exception as e:
#                 print(f"Error saving product image: {e}")
#
#         # Extract the third PDF link using Selenium
#         datasheet_url = get_third_pdf_link(url)
#         print(f"Extracted Datasheet URL: {datasheet_url}")  # Debugging log
#
#         # Extract technical specifications
#         specs = {}
#         spec_tags = soup.find_all("div", class_=lambda x: x and x.startswith("product-detail-page-component_spec__"))
#         for spec in spec_tags:
#             label = spec.find("p", class_="snippet product-detail-page-component_label__3S-Gu")
#             value = spec.find("p", class_="snippet product-detail-page-component_value__2ZiIc")
#             if label and value:
#                 specs[label.text.strip()] = value.text.strip()
#
#         technical_specification = "; ".join(f"{k}: {v}" for k, v in specs.items())
#
#         # Extract meta description and keywords
#         meta_description, meta_keywords = extract_meta_tags(url)
#
#         # Print meta description and keywords to console
#         print(f"Meta Description: {meta_description}")
#         print(f"Meta Keywords: {meta_keywords}")
#
#         # Prepare data row
#         row_data = [
#             model,
#             product,
#             nested_category,
#             url,
#             product_title,
#             product_image_url,  # Store the image URL or local file
#             sales_price,
#             regular_price,
#             datasheet_url,  # Store the third PDF datasheet URL
#             technical_specification,
#             meta_description,  # Store meta description
#             meta_keywords  # Store meta keywords
#         ]
#
#         # Debugging: Print row data before storing
#         print(f"Row Data to store: {row_data}")
#
#         # Write data to CSV immediately (append mode)
#         try:
#             df = pd.DataFrame([row_data], columns=columns)
#             # Append the data to the CSV file with the correct 'lineterminator'
#             df.to_csv(output_file, index=False, header=False, mode='a', lineterminator='\n')
#             print(f"Data stored for URL {index + 1}")
#         except Exception as e:
#             print(f"Error writing data to CSV: {e}")
#
#     except Exception as e:
#         print(f"Error processing URL {url}: {e}")
#
# print(f"Data extraction completed. Total URLs processed: {len(data)}. Output saved to {output_file}.")
















# import os
# import pandas as pd
# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin
# from PIL import Image
# from io import BytesIO
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# import time
#
# # Function to extract meta tags (keywords and description) from the page
# def extract_meta_tags(url):
#     response = requests.get(url)
#
#     if response.status_code != 200:
#         print("Failed to retrieve the page")
#         return '', ''
#
#     soup = BeautifulSoup(response.content, 'html.parser')
#
#     description = soup.find('meta', attrs={'name': 'description'})
#     keywords = soup.find('meta', attrs={'name': 'keywords'})
#
#     meta_description = description['content'] if description else 'No description found'
#     meta_keywords = keywords['content'] if keywords else 'No keywords found'
#
#     return meta_description, meta_keywords
#
#
# # Function to get the third PDF link using Selenium
# def get_third_pdf_link(url):
#     # Set up the Chrome WebDriver
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#     driver.get(url)
#
#     # Wait for the page to fully load (you can adjust the time as needed)
#     time.sleep(5)  # Adjust wait time depending on page load speed
#
#     # Example: Extract the datasheets or PDFs from the page
#     try:
#         # Use XPath or CSS selectors to find the elements containing the PDFs or datasheets
#         datasheets = driver.find_elements(By.XPATH,
#                                           "//a[contains(@href, 'pdf')]")  # This XPath searches for links to PDFs
#
#         # Extract links
#         pdf_links = [datasheet.get_attribute("href") for datasheet in datasheets]
#
#         # Check if there are at least 3 links and return the third one
#         if len(pdf_links) >= 3:
#             return pdf_links[2]  # Return the third PDF link (index 2)
#         else:
#             return ""  # Return empty if less than 3 PDF links found
#
#     except Exception as e:
#         print(f"Error occurred: {str(e)}")
#         return ""
#
#     finally:
#         # Close the browser after scraping
#         driver.quit()
#
#
# # Input Excel file
# input_file = "../Scrape_Link/siemens.xlsx"
# output_file = "siemens_product.csv"
#
# # Read input Excel file
# data = pd.read_excel(input_file)
#
# # Define columns for the output
# columns = [
#     "Brand",
#     "product",
#     "Category",
#     "URL",
#     "Product Title",
#     "Product Image",
#     "Sales Price",
#     "Regular Price",
#     "Datasheet",
#     "Technical Specification",
#     "Meta Description",  # New column for meta description
#     "Meta Keywords"  # New column for meta keywords
# ]
#
# # Check if output file exists and initialize CSV with headers if necessary
# if not os.path.exists(output_file):
#     print(f"Creating a new CSV file: {output_file}")
#     pd.DataFrame(columns=columns).to_csv(output_file, index=False)  # Initialize with headers
#
# # Process each URL
# for index, row in data.iterrows():
#     model = os.path.basename(input_file).replace(".xlsx", "")
#     product = row.get("Category", "")  # Updated to get 'Category' from input
#     nested_category = row.get("Value", "")  # Updated to get 'Value' from input
#     url = row.get("URL", "")
#
#     print(f"Scraping URL {index + 1}/{len(data)}: {url}")
#
#     try:
#         # Load the page
#         response = requests.get(url)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.content, "html.parser")
#
#         # Extract product title
#         title_tag = soup.find("h1", class_=lambda x: x and x.startswith("title product-detail-page-component_title"))
#         product_title = title_tag.text.strip() if title_tag else ""
#
#         # Extract sales and regular price
#         price_tags = soup.find_all("p", class_=lambda x: x and x.startswith("add-to-basket-cta-component_unit-price"))
#         sales_price = price_tags[0].text.strip() if len(price_tags) > 0 else ""
#         regular_price = price_tags[1].text.strip() if len(price_tags) > 1 else ""
#
#         # Extract product image URLs using Selenium
#         driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#         driver.get(url)
#         time.sleep(5)
#
#         images = driver.find_elements(By.TAG_NAME, 'img')
#         product_image_url = ""
#
#         for img in images:
#             img_url = img.get_attribute('src')
#             if img_url and "res.cloudinary.com" in img_url:
#                 product_image_url = f'<img src="{img_url}" height="300" width="300">'
#                 break
#
#         driver.quit()
#
#         # Extract the third PDF link using Selenium
#         datasheet_url = get_third_pdf_link(url)
#         print(f"Extracted Datasheet URL: {datasheet_url}")
#
#         # Extract technical specifications
#         specs = {}
#         spec_tags = soup.find_all("div", class_=lambda x: x and x.startswith("product-detail-page-component_spec__"))
#         for spec in spec_tags:
#             label = spec.find("p", class_="snippet product-detail-page-component_label__3S-Gu")
#             value = spec.find("p", class_="snippet product-detail-page-component_value__2ZiIc")
#             if label and value:
#                 specs[label.text.strip()] = value.text.strip()
#
#         technical_specification = "; ".join(f"{k}: {v}" for k, v in specs.items())
#
#         # Extract meta description and keywords
#         meta_description, meta_keywords = extract_meta_tags(url)
#
#         # Prepare data row
#         row_data = [
#             model,
#             product,
#             nested_category,
#             url,
#             product_title,
#             product_image_url,  # Store the image URL as an <img> tag
#             sales_price,
#             regular_price,
#             datasheet_url,  # Store the third PDF datasheet URL
#             technical_specification,
#             meta_description,  # Store meta description
#             meta_keywords  # Store meta keywords
#         ]
#
#         # Debugging: Print row data before storing
#         print(f"Row Data to store: {row_data}")
#
#         # Write data to CSV immediately (append mode)
#         try:
#             df = pd.DataFrame([row_data], columns=columns)
#             # Append the data to the CSV file with the correct 'lineterminator'
#             df.to_csv(output_file, index=False, header=False, mode='a', lineterminator='\n')
#             print(f"Data stored for URL {index + 1}")
#         except Exception as e:
#             print(f"Error writing data to CSV: {e}")
#
#     except Exception as e:
#         print(f"Error processing URL {url}: {e}")
#
# print(f"Data extraction completed. Total URLs processed: {len(data)}. Output saved to {output_file}.")

import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Function to extract meta tags (keywords and description) from the page
def extract_meta_tags(url):
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to retrieve the page")
        return '', ''

    soup = BeautifulSoup(response.content, 'html.parser')

    description = soup.find('meta', attrs={'name': 'description'})
    keywords = soup.find('meta', attrs={'name': 'keywords'})

    meta_description = description['content'] if description else 'No description found'
    meta_keywords = keywords['content'] if keywords else 'No keywords found'

    return meta_description, meta_keywords


# Function to get the third PDF link using Selenium
def get_third_pdf_link(url):
    # Set up the Chrome WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)

    # Wait for the page to fully load (you can adjust the time as needed)
    time.sleep(5)  # Adjust wait time depending on page load speed

    # Example: Extract the datasheets or PDFs from the page
    try:
        # Use XPath or CSS selectors to find the elements containing the PDFs or datasheets
        datasheets = driver.find_elements(By.XPATH,
                                          "//a[contains(@href, 'pdf')]")  # This XPath searches for links to PDFs

        # Extract links
        pdf_links = [datasheet.get_attribute("href") for datasheet in datasheets]

        # Check if there are at least 3 links and return the third one
        if len(pdf_links) >= 3:
            return pdf_links[2]  # Return the third PDF link (index 2)
        else:
            return ""  # Return empty if less than 3 PDF links found

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return ""

    finally:
        # Close the browser after scraping
        driver.quit()


# Input Excel file
input_file = "../Scrape_Link/siemens.xlsx"
output_file = "siemens_product.csv"

# Read input Excel file
data = pd.read_excel(input_file)

# Define columns for the output
columns = [
    "Brand",
    "Product",
    "Category",
    "URL",
    "Product Title",
    "Product Image",
    "Sales Price",
    "Regular Price",
    "Datasheet",
    "Technical Specification",
    "Meta Description",  # New column for meta description
    "Meta Keywords"  # New column for meta keywords
]

# Check if output file exists and initialize CSV with headers if necessary
if not os.path.exists(output_file):
    print(f"Creating a new CSV file: {output_file}")
    pd.DataFrame(columns=columns).to_csv(output_file, index=False)  # Initialize with headers

# Process each URL
for index, row in data.iterrows():
    model = os.path.basename(input_file).replace(".xlsx", "")
    product = row.get("Category", "")  # Updated to get 'Category' from input
    nested_category = row.get("Value", "")  # Updated to get 'Value' from input
    url = row.get("URL", "")

    print(f"Scraping URL {index + 1}/{len(data)}: {url}")

    try:
        # Load the page
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract product title
        title_tag = soup.find("h1", class_=lambda x: x and x.startswith("title product-detail-page-component_title"))
        product_title = title_tag.text.strip() if title_tag else ""

        # Extract sales and regular price
        price_tags = soup.find_all("p", class_=lambda x: x and x.startswith("add-to-basket-cta-component_unit-price"))
        sales_price = price_tags[0].text.strip() if len(price_tags) > 0 else ""
        regular_price = price_tags[1].text.strip() if len(price_tags) > 1 else ""

        # Extract product image URLs using Selenium
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(url)
        time.sleep(5)

        images = driver.find_elements(By.TAG_NAME, 'img')
        product_image_url = ""

        for img in images:
            img_url = img.get_attribute('src')
            if img_url and "res.cloudinary.com" in img_url:
                product_image_url = f'<img src="{img_url}" height="300" width="300">'
                break

        driver.quit()

        # Extract the third PDF link using Selenium
        datasheet_url = get_third_pdf_link(url)
        print(f"Extracted Datasheet URL: {datasheet_url}")

        # Extract technical specifications
        specs = {}
        spec_tags = soup.find_all("div", class_=lambda x: x and x.startswith("product-detail-page-component_spec__"))
        for spec in spec_tags:
            label = spec.find("p", class_="snippet product-detail-page-component_label__3S-Gu")
            value = spec.find("p", class_="snippet product-detail-page-component_value__2ZiIc")
            if label and value:
                specs[label.text.strip()] = value.text.strip()

        # Convert technical specifications to an HTML table
        technical_specification = "<table>"
        for k, v in specs.items():
            technical_specification += f"<tr><td>{k}</td><td>{v}</td></tr>"
        technical_specification += "</table>"

        # Extract meta description and keywords
        meta_description, meta_keywords = extract_meta_tags(url)

        # Prepare data row
        row_data = [
            model,
            product,
            nested_category,
            url,
            product_title,
            product_image_url,  # Store the image URL as an <img> tag
            sales_price,
            regular_price,
            datasheet_url,  # Store the third PDF datasheet URL
            technical_specification,  # Store technical specification as an HTML table
            meta_description,  # Store meta description
            meta_keywords  # Store meta keywords
        ]

        # Debugging: Print row data before storing
        print(f"Row Data to store: {row_data}")

        # Write data to CSV immediately (append mode)
        try:
            df = pd.DataFrame([row_data], columns=columns)
            # Append the data to the CSV file with the correct 'lineterminator'
            df.to_csv(output_file, index=False, header=False, mode='a', lineterminator='\n')
            print(f"Data stored for URL {index + 1}")
        except Exception as e:
            print(f"Error writing data to CSV: {e}")

    except Exception as e:
        print(f"Error processing URL {url}: {e}")

print(f"Data extraction completed. Total URLs processed: {len(data)}. Output saved to {output_file}.")
