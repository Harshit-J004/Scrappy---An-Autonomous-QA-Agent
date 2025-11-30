import google.generativeai as genai
import json
from typing import Dict, List
from backend.config import config

class ScriptAgent:
    def __init__(self):
        if not config.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY not found in environment variables.")
        genai.configure(api_key=config.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def generate_script(self, test_case: Dict, html_content: str, elements_schema: Dict, context_chunks: List[Dict]) -> str:
        """
        Generates a Selenium Python script for a specific test case.
        """
        
        # Summarize HTML to avoid token limits if necessary, but for now passing full HTML 
        # as it's a single page checkout.
        
        context_text = "\n\n".join([
            f"Source: {chunk.get('source', 'Unknown')}\nContent: {chunk.get('text', str(chunk))}"
            for chunk in context_chunks
        ])

        prompt = f"""
        You are an expert Selenium (Python) automation engineer.
        Use ONLY the HTML and documentation provided.
        Use real IDs, names, or CSS selectors that exist in the HTML.
        If an element is not present in the HTML, do not use it.
        Use explicit waits (WebDriverWait) instead of hard sleeps whenever possible.
        The script must be runnable as-is.
        
        Test Case:
        {json.dumps(test_case, indent=2)}

        Available Elements Schema:
        {json.dumps(elements_schema, indent=2)}

        Relevant Documentation Context:
        {context_text}

        HTML Content:
        {html_content}

        Generate a complete Python Selenium script that:
        - Opens the checkout page at a placeholder URL (e.g., "file:///path/to/checkout.html").
        - Implements the test steps exactly.
        - Uses correct locators from the available elements list.
        - Asserts the expected_result at the end using assertions.
        - Wrap everything in a main() and add if __name__ == "__main__".
        - Do not use markdown formatting (```python), just return the code.
        """

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.1,
                )
            )
            # Clean up markdown code blocks if present
            code = response.text
            if code.startswith("```python"):
                code = code[9:]
            if code.startswith("```"):
                code = code[3:]
            if code.endswith("```"):
                code = code[:-3]
            return code.strip()
        except Exception as e:
            print(f"Error generating script: {e}")
            return f"# Error generating script: {str(e)}"
