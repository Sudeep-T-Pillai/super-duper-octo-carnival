from urllib.parse import urlparse

def extract_page_id(input_string: str) -> str:
    """
    Extracts the LinkedIn Page ID from a URL or returns the ID if provided directly.
    Example: 
    - "https://www.linkedin.com/company/deepsolv/" -> "deepsolv"
    - "deepsolv" -> "deepsolv"
    """
    clean_input = input_string.strip().rstrip('/')
    
    if "linkedin.com" in clean_input:
        parsed = urlparse(clean_input)
        path_parts = parsed.path.split('/')
        valid_parts = [p for p in path_parts if p]
        
        if valid_parts:
            return valid_parts[-1] 
            
    return clean_input