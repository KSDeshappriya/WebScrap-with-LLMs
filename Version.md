# Version 0.0.2

### **Key Enhancements in This Version**

1.  **Retrying Library**:

    *   The `retrying` library provides clean exponential backoff for failed requests to the GenAI API.
2.  **Output File Management**:
    
    *   Ensures the directory for `data.json` exists before saving.
3.  **Improved JSON Extraction**:
    
    *   Regex for JSON extraction handles potential edge cases more gracefully.
4.  **Error Logging**:
    
    *   All errors are logged with appropriate severity levels for debugging.
5.  **Flexible Configuration**:
    
    *   Uses `.env` files to manage sensitive credentials, with safeguards to check their presence.
6.  **Modular Design**:
    
    *   Each function has a single responsibility, making the code easier to test and extend.

---