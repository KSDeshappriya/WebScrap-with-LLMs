## Details about Version

### v 0.0.1
This script is now modular and reusable, with the functionality encapsulated in the LLMWebScraper class. It allows for easy adaptation to different scraping tasks by specifying new instructions and URLs.

##### How to Use the Script

1.  **Set the API key as an environment variable:** You can add the API key to your `.env` file or export it in your shell session. For example:
    
    *   Create a `.env` file in the same directory as your script with the following content:
        
        `Gemini_API_KEY=AIzaSyBru4lgqGpms81Jcx7pD4VKNSqqyQj_Dxw` 
        
    *   Or, export it directly in your terminal:
        
        `export Gemini_API_KEY=AIzaSyBru4lgqGpms81Jcx7pD4VKNSqqyQj_Dxw` 
        
2.  **Pass the correct environment variable name:** Update the code where you're initializing the `LLMWebScraper` instance to use the variable name `Gemini_API_KEY`:
    
    `scraper = LLMWebScraper(api_key_env="Gemini_API_KEY")` 
    
    This tells the script to fetch the actual API key from the `Gemini_API_KEY` environment variable.
    

##### Summary of Version 0.0.1:

*   Modularized the web scraping functionality into the `LLMWebScraper` class.
*   Added instructions on how to set the API key as an environment variable.
*   Set the API key in the environment (e.g., `.env` file or `export` command).
*   Pass the name of the environment variable (`Gemini_API_KEY`) to the `LLMWebScraper`.

---