import requests
import google.generativeai as genai
from langchain.prompts import PromptTemplate
import json
import re
import logging
import os
from typing import Optional, Dict, Any
from retrying import retry
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class LLMWebScraper:
    def __init__(self, api_key_env: str, model_name: str = "gemini-2.0-flash-exp"):
        """Initialize the scraper with API key and model."""
        self.api_key = os.getenv(api_key_env)
        if not self.api_key:
            raise ValueError(f"{api_key_env} environment variable is not set.")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name=model_name)
        
        self.prompt_template = PromptTemplate(
            input_variables=["html", "instructions"],
            template="""
You are a data extraction expert. I will provide you with raw HTML content of a webpage, 
and you need to extract specific information based on my instructions.

HTML Content:
{html}

Extraction Instructions:
{instructions}

Please extract the information in a structured JSON format.
"""
        )

    def __fetch_webpage(self, url: str) -> str:
        """Fetch HTML content from a given URL."""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            logging.info("Webpage HTML content fetched successfully!")
            return response.text
        except requests.RequestException as e:
            logging.error(f"Failed to fetch webpage: {e}")
            raise

    @retry(stop_max_attempt_number=3, wait_exponential_multiplier=1000)
    def __generate_output(self, input_data: str) -> str:
        """Generate content using GenAI with retry logic."""
        try:
            return self.model.generate_content(contents=input_data).text
        except Exception as e:
            logging.warning(f"Error during content generation: {e}")
            raise

    def __extract_data(self, html_content: str, instructions: str) -> str:
        """Generate a structured response by passing HTML content and instructions to the language model."""
        formatted_prompt = self.prompt_template.format(html=html_content, instructions=instructions)
        return self.__generate_output(formatted_prompt)

    def __extract_json(self, md_code: str) -> Optional[Dict[str, Any]]:
        """Extract and parse JSON from markdown-style code."""
        match = re.search(r'```json\s*({[\s\S]*?})\s*```', md_code)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError as e:
                logging.error(f"Failed to parse JSON: {e}")
                return None
        logging.error("No JSON code block found in the response.")
        return None

    def toJSON(self, url: str, instructions: str) -> Optional[Dict[str, Any]]:
        """Extract data from a given URL using provided instructions."""
        try:
            html_content = self.__fetch_webpage(url)
            extracted_md = self.__extract_data(html_content, instructions)
            return self.__extract_json(extracted_md)
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return None
        
    def toFile(self, data: Dict[str, Any], file_path: str) -> None:
        """Save the extracted data to a JSON file."""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        logging.info(f"Data saved to {file_path}")

# Example usage
if __name__ == "__main__":
    # Initialize the scraper
    scraper = LLMWebScraper(api_key_env="Gemini_API_KEY")

    # Define instructions
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

    # URL of the webpage to scrape
    url = "https://chirpy.cotes.page/"

    try:
        # Parse JSON from the extracted Data From given URL
        blog_data = scraper.toJSON(url, instructions)

        # Save the data if valid
        if blog_data:
            scraper.toFile(blog_data, "output/data.json")
        else:
            logging.warning("No blog data to save.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
