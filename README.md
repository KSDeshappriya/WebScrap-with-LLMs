# Web Scraping Project with AI Data Extraction

## Overview

This project demonstrates how to scrape a webpage and extract specific information using AI-powered data extraction techniques. The script fetches HTML content from a specified URL, processes it with a generative AI model, and extracts structured data in JSON format. The extracted data includes blog post titles, author names, and publication dates.

## Features

- Fetches HTML content from a specified URL.
- Utilizes an AI model for data extraction based on user-defined instructions.
- Outputs extracted data in a structured JSON format.
- Implements retry logic with exponential backoff for handling API rate limits.
- Saves the extracted data to a JSON file.

## Requirements

- Python 3.x
- `requests` library
- `google.generativeai` library
- `langchain` library
- `json` and `re` modules (part of the Python standard library)
- `python-dotenv`: To manage environment variables via `.env` files.
- `retrying`: To add retry logic with exponential backoff.
- `logging`: (Part of the Python standard library, no need to install separately.)

## Installation

1. Clone the repository or download the script.
2. Install the required libraries using pip:

   ```bash
   pip install requests google-generativeai langchain python-dotenv retrying
   ```

3. Ensure you have a valid API key for the Google Generative AI service.

## Usage

1. Open the script in your preferred Python environment.
2. Modify the `url` variable to point to the webpage you want to scrape.
3. Set your API key in the `.env` file as `GEMINI_API_KEY=your_api_key`.
4. Run the script:

   ```bash
   python WebScrap-GeminiAI.py
   ```

5. The extracted blog data will be saved in a file named `data.json` in the same directory.

## Code Explanation

- **Fetching HTML Content**: The script uses the `requests` library to fetch the HTML content of the specified URL.
  
- **AI Configuration**: The script configures the Google Generative AI model for data extraction.

- **Prompt Template**: A prompt template is defined to instruct the AI model on how to extract the required information from the HTML content.

- **Data Extraction**: The `extract_blog_data` function formats the prompt with the HTML content and extraction instructions, then calls the AI model to generate the output.

- **JSON Extraction**: The `extractJson` function uses regular expressions to extract the JSON data from the AI model's output.

- **Saving Data**: The extracted data is saved to a `data.json` file if available.

## Example Output

The output JSON file (`data.json`) will contain the extracted blog data in the following format:

```json
{
    "blog_posts": [
        {
            "title": "How to Create a Personal Blog with GitHub Pages",
            "author": "Cotes Chung",
            "publication_date": "2023-12-15"
        },
        {
            "title": "Understanding GPT",
            "author": "John Doe",
            "publication_date": "2023-12-14"
        }
    ]
}
```

## Version Information

You can see these from [Version.md](Version.md)

## Contributing

Contributions are welcome! If you have suggestions for improvements or additional features, feel free to submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgments

- Thanks to the developers of the `requests`, `google.generativeai`, `python-dotenv`, and `langchain` libraries for their contributions to the Python ecosystem.
- Special thanks to the creators of the webpage being scraped for providing valuable content.