import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

# URL of the webpage
url = "https://en.wikipedia.org/wiki/1964_Brinks_Hotel_bombing"

# Fetch the HTML content
response = requests.get(url)
html_content = response.text

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Extract the entire text content
page_text = soup.get_text()

# Use regular expressions to find the relevant data
# Assuming the data is in the format "Key: Value"
data_pattern = r'([A-Za-z ]+): ([A-Za-z0-9 ,.-]+)'
matches = re.findall(data_pattern, page_text)

# Convert the matches into a DataFrame
data_list = [{'Key': match[0].strip(), 'Value': match[1].strip()} for match in matches]
final_data = pd.DataFrame(data_list)

# View the final data
# print(final_data)

# save As json
final_data.to_json('data.json', orient='records')

# print(page_text)