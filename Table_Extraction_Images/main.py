# import urllib.request
# from urllib.error import URLError, HTTPError
# import ssl
#
#
# def fetch_image_with_urllib(image_url, save_path):
#     # Disable SSL verification to avoid SSL certificate issues (Not recommended for production)
#     context = ssl._create_unverified_context()
#
#     try:
#         # Open the image URL and fetch the content
#         with urllib.request.urlopen(image_url, context=context) as response:
#             # Read the image content
#             img_data = response.read()
#
#             # Save the image to file
#             with open(save_path, 'wb') as f:
#                 f.write(img_data)
#             print(f"Image saved to {save_path}")
#
#     except HTTPError as e:
#         print(f"HTTP error: {e.code} - {e.reason}")
#     except URLError as e:
#         print(f"URL error: {e.reason}")
#     except Exception as e:
#         print(f"An error occurred: {e}")
#
#
# # Example usage
# image_url = "https://www.cyconozzles.com/wp-content/uploads/2022/03/venturi-nozzle-102.jpg"
# save_path = "air-fryer-nozzle-7.jpg"
#
# fetch_image_with_urllib(image_url, save_path)
# E:\PycharmProjects\Table_Extraction_Images\air-fryer-nozzle-7

import pytesseract
import cv2
import pandas as pd

# Setup the tesseract path if not set in environment variables
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Adjust this path accordingly

# Read an image and apply OCR
image_path = r'E:\PycharmProjects\Table_Extraction_Images\air-fryer-nozzle-7.jpg'
image = cv2.imread(image_path)
text = pytesseract.image_to_string(image)

# Split the text into rows
rows = text.strip().split("\n")

# Split each row into columns (assuming space-separated values)
table_data = [row.split() for row in rows]

# Convert to a pandas DataFrame
df = pd.DataFrame(table_data)

# Print the DataFrame
print("Data as DataFrame:")
print(df)

# Save as an HTML table
html_table = df.to_html(index=False, header=False)
output_html_path = r'E:\PycharmProjects\Table_Extraction_Images\TableData.html'
with open(output_html_path, 'w', encoding='utf-8') as f:
    f.write(html_table)

print(f"HTML table saved to {output_html_path}")
