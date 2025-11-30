import json
import fitz  # pymupdf
from bs4 import BeautifulSoup

class DocumentParser:
    @staticmethod
    def parse_text(file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def parse_pdf(file_path: str) -> str:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    @staticmethod
    def parse_json(file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # Convert JSON to a more readable text format for embedding
        return json.dumps(data, indent=2)

    @staticmethod
    def parse_html_structure(html_content: str) -> dict:
        """Parses HTML to extract interactive elements for the agent."""
        soup = BeautifulSoup(html_content, 'html.parser')
        elements = []
        
        # Find inputs, buttons, selects
        for tag in soup.find_all(['input', 'button', 'select', 'textarea']):
            el_info = {
                'tag': tag.name,
                'id': tag.get('id'),
                'name': tag.get('name'),
                'type': tag.get('type'),
                'placeholder': tag.get('placeholder'),
                'text': tag.get_text(strip=True) if tag.name == 'button' else None
            }
            # Filter out elements without identifiers if possible, or keep them if they are important
            if el_info['id'] or el_info['name'] or el_info['text']:
                elements.append(el_info)
                
        return {"elements": elements}

    @staticmethod
    def parse_html_text(html_content: str) -> str:
        """Extracts visible text from HTML for RAG context."""
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup.get_text(separator='\n', strip=True)
