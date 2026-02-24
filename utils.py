import re

def clean_text(text: str) -> str:
    """
    Cleans extracted text for LLM processing.
    - Removes extra whitespaces
    - Normalizes characters
    - Removes non-printable characters
    """
    if not text:
        return ""
    
    # Remove non-printable characters
    text = "".join(char for char in text if char.isprintable() or char in "\n\t")
    
    # Replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text)
    
    # Remove extra newlines
    text = re.sub(r'\n+', '\n', text)
    
    return text.strip()
