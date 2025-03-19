
import pandas as pd
from bs4 import BeautifulSoup


# Function to extract product details from HTML
def extract_product_details(html_file):
    with open(html_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # List to store extracted product data
    products = []

    # Find all h1 tags, which represent product titles
    h1_tags = soup.find_all('h1')

    for h1 in h1_tags:
        product_data = {}

        # Extract product title from the h1 tag
        product_data['Product Title'] = h1.get_text(strip=True)

        # Find the next table after the current h1 tag
        table = h1.find_next('table')

        if table:  # If a table is found after the h1 tag
            material_value = ""  # To store material value
            description_value = ""  # To store description value
            application_value = ""  # To store application value

            rows = table.find_all('tr')

            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 2:
                    key = cols[0].get_text(strip=True).lower()
                    value = ", ".join([col.get_text(strip=True) for col in cols[1:]])

                    if key == "material":
                        material_value = value
                    elif key == "description":
                        description_value = value
                    elif key == "application":
                        application_value = value

            # Store the extracted fields in the product data
            product_data['Material'] = material_value
            product_data['Description'] = description_value
            product_data['Application'] = application_value

        # Append the extracted product data to the list
        products.append(product_data)

    return products


# Function to write extracted details to Excel
def write_to_excel(data, output_file):
    df = pd.DataFrame(data)
    df.to_excel(output_file, index=False)


# Example usage
html_file = 'SynergyHTML.html'  # Path to your HTML file
output_file = 'products.xlsx'  # Path to the output Excel file

product_data = extract_product_details(html_file)
write_to_excel(product_data, output_file)

print(f"Product details have been extracted and saved to {output_file}")



# import pandas as pd
# from bs4 import BeautifulSoup
# from openpyxl import Workbook
# from openpyxl.worksheet.hyperlink import Hyperlink
#
#
# # Function to extract product details from HTML
# def extract_product_details(html_file):
#     with open(html_file, 'r', encoding='utf-8') as file:
#         soup = BeautifulSoup(file, 'html.parser')
#
#     # List to store extracted product data
#     products = []
#
#     # Find all h1 tags, which represent product titles
#     h1_tags = soup.find_all('h1')
#
#     for h1 in h1_tags:
#         product_data = {}
#
#         # Extract product title from the h1 tag
#         product_data['Product Title'] = h1.get_text(strip=True)
#
#         # Find the next table after the current h1 tag
#         table = h1.find_next('table')
#
#         if table:  # If a table is found after the h1 tag
#             material_value = ""  # To store material value
#             description_value = ""  # To store description value
#             application_value = ""  # To store application value
#             images = []  # To store image paths
#
#             rows = table.find_all('tr')
#
#             for row in rows:
#                 cols = row.find_all('td')
#
#                 # Check for text-based fields
#                 if len(cols) >= 2:
#                     key = cols[0].get_text(strip=True).lower()
#                     value = ", ".join([col.get_text(strip=True) for col in cols[1:]])
#
#                     if key == "material":
#                         material_value = value
#                     elif key == "description":
#                         description_value = value
#                     elif key == "application":
#                         application_value = value
#
#                 # Check for images in the row
#                 img_tags = row.find_all('img')
#                 for img in img_tags:
#                     img_src = img.get('src')
#                     if img_src:  # Ensure the `src` attribute exists
#                         images.append(img_src)
#
#             # Store the extracted fields in the product data
#             product_data['Material'] = material_value
#             product_data['Description'] = description_value
#             product_data['Application'] = application_value
#
#             # Add each image path as a hyperlink
#             for idx, img_path in enumerate(images):
#                 product_data[f'Image {idx + 1}'] = f'=HYPERLINK("{img_path}", "{img_path}")'
#
#         # Append the extracted product data to the list
#         products.append(product_data)
#
#     return products
#
#
# # Function to write extracted details to Excel with hyperlinks
# def write_to_excel(data, output_file):
#     # Create a workbook and active sheet
#     wb = Workbook()
#     ws = wb.active
#
#     # Write column headers
#     headers = list(data[0].keys()) if data else []  # Convert dict_keys to list
#     ws.append(headers)
#
#     # Write data rows
#     for product in data:
#         row = [product.get(col, '') for col in headers]
#         ws.append(row)
#
#     # Save the workbook to a file
#     wb.save(output_file)
#
#
# # Example usage
# html_file = 'SynergyHTML.html'  # Path to your HTML file
# output_file = 'product_details_with_links.xlsx'  # Path to the output Excel file
#
# product_data = extract_product_details(html_file)
# write_to_excel(product_data, output_file)
#
# print(f"Product details have been extracted and saved to {output_file}")
