import requests
import google.generativeai as genai
from langchain.prompts import PromptTemplate
import json
import re
import time

import os
from dotenv import load_dotenv
load_dotenv()

url = "https://chirpy.cotes.page/"

response = requests.get(url)
if response.status_code == 200:
    html_content = response.text
    print("Webpage HTML content fetched successfully!")
else:
    print(f"Failed to fetch webpage. Status code: {response.status_code}")
    exit()


genai.configure(api_key=os.getenv("Gemini_API_KEY"))

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash-exp"
)

html_prompt = """
You are a data extraction expert. I will provide you with raw HTML content of a webpage, 
and you need to extract specific information based on my instructions.

HTML Content:
{html}

Extraction Instructions:
{instructions}

Please extract the information in a structured JSON format.
"""

prompt = PromptTemplate(
    input_variables=["html", "instructions"],
    template=html_prompt,
)

instructions = """
Extract the following information:
1. Titles of all blog posts on the page.
2. Author names for each blog post.
3. Publication dates of each blog post.

Please provide the extracted information in a structured JSON format.
Expecting property name enclosed in double quotes and values in string format.
Example:
{
  "blog_posts": [
        {
            "title": "Blog Post 1",
            "author": "Author 1",
            "publication_date": "2022-01-01"
        },
        {
            "title": "Blog Post 2",
            "author": "Author 2",
            "publication_date": "2022-01-02"
        }
    ]
}
"""


def generate_output(input_data):
    #Retry logic with exponential backoff
    max_retries = 3
    retry_delay = 1
    for attempt in range(max_retries):
        try:
            return model.generate_content(contents=input_data).text
        except Exception as e:
            print(f"Error during generation (attempt {attempt + 1}/{max_retries}): {e}")
            if "429 Resource has been exhausted" in str(e) and attempt < max_retries -1:
                time.sleep(retry_delay)
                retry_delay *= 2 #Exponential Backoff
            else:
                raise  #Re-raise for other exceptions or max retries reached


def extract_blog_data(html_content):
    formatted_prompt = prompt.format(html=html_content, instructions=instructions)
    output = generate_output(formatted_prompt)
    return output

def extractJson(md_code):
    match = re.search(r'```json\s*({[\s\S]*?})\s*```', md_code)
    if match:
        try:
            return json.loads(match.group(1))
            # return match.group(1)
        except json.JSONDecodeError:
            return None
    return None

blog_data = extractJson(extract_blog_data(html_content))

print(blog_data)

# save output to data.json
if blog_data:
    with open('data.json', 'w') as f:
            json.dump(blog_data, f, indent=4)
else:
    print("No blog data to save.")

# Output:
# {
#     "blog_posts": [
#         {
#             "title": "How to Create a Personal Blog with GitHub Pages",
#             "author": "Cotes Chung",
#             "publication_date": "2023-12-15"
#         },
#         {
#             "title": "Understanding GPT",
#             "author": "John Doe",
#             "publication_date": "2023-12-14"
#         }
#    ]
# }