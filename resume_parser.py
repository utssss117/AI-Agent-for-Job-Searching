import fitz  # PyMuPDF
from utils import clean_text

def extract_text_from_pdf(pdf_path_or_bytes) -> str:
    """
    Extracts and cleans text from a PDF file.
    """
    try:
        if isinstance(pdf_path_or_bytes, str):
            doc = fitz.open(pdf_path_or_bytes)
        else:
            doc = fitz.open(stream=pdf_path_or_bytes, filetype="pdf")
            
        text = ""
        for page in doc:
            text += page.get_text()
        
        doc.close()
        return clean_text(text)
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""
