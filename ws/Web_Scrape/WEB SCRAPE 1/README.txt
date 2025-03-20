
<!------------------------ WEB SCRAPE USING PYTHON ----------------------------!>

PROJECT STRUCTURE:
------------------
Web_Scrape ==> Parent Folder
   Description_Automation ==> Child Folder 1, For description automation
      Main.py ==> Python code to generate description
      Output.xlsx ==> Sample excel file format
   Products Extract ==> Child Folder 2, For product extraction
      Product_Extract => To extract products from json data
	  ProductsData ==> It was a sheet, used to store products
   URL_to_JSON ==> Child Folder 3, For JSON data extraction
      product_data ==> nested folder, used to store json files
	  JSON_Extract ==> Python code used to extract json data


HOW TO RUN:
-----------
1) JSON_Extract:
      PATH: Inside URL_to_JSON folder
      Here is the python code to extract products as JSON data by passing URL's
	  At line no.55, there was an array named urls. Pass url's in the array.
	  Note: add products.json at end of the url, you are passing.
	  Then run the code.

2) JSON file:
      PATH: Inside product_data folder located within URL_to_JSON folder
      After above step, json file stored under product_data folder.
	  Check it's stored or not!

3) RUN Product_Extract code:
      PATH: Inside Product Extract folder
      Finally run python code, it will store data into sheet.
	  Note: In this code, implemented code for fetch products and technical specification. So, if you want to scrape products only means terminate the process of scrape_technical_specifications function in the code!

4) Generate Description:
   PATH: Inside	Description_Automation folder
   Store an excel in the Description_Automation folder, which mandatorily contains tile column and empty description column.
   In Main.py python code, at line no.83 locate the excel file then run the code.


<!--------------------------------------------------- End! -----------------------------------------------!>