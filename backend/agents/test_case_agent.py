import google.generativeai as genai
import json
from typing import List, Dict
from backend.config import config

class TestCaseAgent:
    def __init__(self):
        if not config.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY not found in environment variables.")
        genai.configure(api_key=config.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def generate_test_cases(self, query: str, context_chunks: List[Dict]) -> Dict:
        """
        Generates test cases based on user query and retrieved context.
        """
        context_text = "\n\n".join([
            f"Source: {chunk.get('source', 'Unknown')}\nContent: {chunk.get('text', str(chunk))}"
            for chunk in context_chunks
        ])

        prompt = f"""
        You are an expert QA engineer.
        You ONLY use the provided context from product specs, UI/UX guidelines, APIs, and HTML structure.
        If something is not in the context, say "Not specified in documents" and DO NOT invent it.
        Generate comprehensive positive and negative test cases. Include boundary, validation, UI, and integration cases.

        Context:
        {context_text}

        User Request:
        {query}

        Output a list of test cases in JSON format with this schema:
        {{
            "test_cases": [
                {{
                    "test_id": "TC-001",
                    "feature": "Feature Name",
                    "scenario_type": "positive/negative/boundary/UI/validation/integration",
                    "preconditions": "Preconditions here",
                    "steps": ["Step 1", "Step 2"],
                    "input_data": {{ "key": "value" }},
                    "expected_result": "Expected result",
                    "grounded_in": ["source_document.md"]
                }}
            ]
        }}
        """

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.2,
                )
            )
            print(f"Raw response from Gemini: {response.text[:500]}...")  # Debug
            
            # Try to parse JSON from the response
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            result = json.loads(response_text.strip())
            print(f"Parsed {len(result.get('test_cases', []))} test cases")  # Debug
            return result
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            print(f"Response text: {response.text}")
            return {"test_cases": [], "error": f"Failed to parse JSON: {str(e)}"}
        except Exception as e:
            print(f"Error generating test cases: {e}")
            return {"test_cases": [], "error": str(e)}
