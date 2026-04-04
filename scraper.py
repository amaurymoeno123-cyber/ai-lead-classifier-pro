import requests
from bs4 import BeautifulSoup

def extract_info(url):
    """
    Extracts relevant text from a given URL.
    Prioritizes headers (h1, h2, h3) and paragraphs (p) to minimize noise.
    """
    try:
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=header, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()

        # Extract specific tags to avoid footer/nav noise
        tags = soup.find_all(['h1', 'h2', 'h3', 'p'])
        
        # Clean and join text
        lines = [tag.get_text(strip=True) for tag in tags if tag.get_text(strip=True)]
        text = "\n".join(lines)
        
        return text if text else "No relevant content found."

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None
