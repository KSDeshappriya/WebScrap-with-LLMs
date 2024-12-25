# version 0.0.2
# Date: 2024-12-25
# Description: This script demonstrates how to use the Gemini AI model to extract data from a webpage.
# More information: Version.md

import requests
import google.generativeai as genai
from langchain.prompts import PromptTemplate
import json
import re
import time
import logging
import os
from typing import Optional, Dict, Any
from retrying import retry
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Ensure required environment variables are set
GEMINI_API_KEY = os.getenv("Gemini_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Gemini_API_KEY environment variable is not set.")

# Configure GenAI
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(model_name="gemini-2.0-flash-exp")

# Prompt template for data extraction
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

def fetch_webpage(url: str) -> str:
    """Fetches HTML content from a given URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        logging.info("Webpage HTML content fetched successfully!")
        return response.text
    except requests.RequestException as e:
        logging.error(f"Failed to fetch webpage: {e}")
        raise

@retry(stop_max_attempt_number=3, wait_exponential_multiplier=1000)
def generate_output(input_data: str) -> str:
    """Generates content using GenAI with retry logic."""
    try:
        return model.generate_content(contents=input_data).text
    except Exception as e:
        logging.warning(f"Error during content generation: {e}")
        raise

def extract_blog_data(html_content: str) -> str:
    """Generates a structured response by passing HTML content to the language model."""
    formatted_prompt = prompt.format(html=html_content, instructions=instructions)
    return generate_output(formatted_prompt)

def extract_json(md_code: str) -> Optional[Dict[str, Any]]:
    """Extracts and parses JSON from markdown-style code."""
    match = re.search(r'```json\s*({[\s\S]*?})\s*```', md_code)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse JSON: {e}")
            return None
    logging.error("No JSON code block found in the response.")
    return None

def save_to_file(data: Dict[str, Any], file_path: str) -> None:
    """Saves the extracted data to a JSON file."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
    logging.info(f"Data saved to {file_path}")

def main():
    # URL of the webpage to scrape
    url = "https://chirpy.cotes.page/"

    try:
        # Fetch webpage HTML content
        html_content = fetch_webpage(url)

        # Extract blog data using GenAI
        extracted_md = extract_blog_data(html_content)

        # Parse JSON from the extracted markdown
        blog_data = extract_json(extracted_md)

        # Save the data if valid
        if blog_data:
            save_to_file(blog_data, "output/data.json")
        else:
            logging.warning("No blog data to save.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

# Example Output:
# {
#   "blog_posts": [
#     {
#       "title": "How to Create a Personal Blog with GitHub Pages",
#       "author": "Cotes Chung",
#       "publication_date": "2023-12-15"
#     },
#     {
#       "title": "Understanding GPT",
#       "author": "John Doe",
#       "publication_date": "2023-12-14"
#     }
#   ]
# }