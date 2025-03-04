import threading
import queue
import urllib.robotparser, urllib.request, urllib.parse
from urllib.parse import ParseResult
from bs4 import BeautifulSoup  # type: ignore
from time import sleep
import re
import collections
import traceback

from ..db.db import store_page, update_keyword_page_frequencies

RED     = "\033[91m"
YELLOW  = "\033[93m"
GREEN   = "\033[92m"
RESET   = "\033[0m"

def check_robots_txt(url: str, user_agent: str):
    """Check if the URL is allowed by robots.txt"""
    parsed_url: ParseResult = urllib.parse.urlparse(url)
    robots_url = urllib.parse.urljoin(f"{parsed_url.scheme}://{parsed_url.netloc}", "/robots.txt")
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(robots_url)
    
    try:
        # Create a request with timeout for robots.txt
        headers = {'User-Agent': user_agent}
        req = urllib.request.Request(robots_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            # Parse the robots.txt content
            lines = response.read().decode('utf-8').splitlines()
            rp.parse(lines)
    except Exception as e:
        print(f"{RED}Could not read robots.txt at {robots_url}: {e}{RESET}")
        # If we can't read robots.txt within timeout, assume it's allowed
        return rp, True
    
    is_allowed = rp.can_fetch(user_agent, url)
    if not is_allowed:
        print(f"{RED}Blocked by robots.txt: {url}{RESET}")
    
    return rp, is_allowed

def fetch_html(url: str, user_agent: str):
    """Fetch HTML content from the URL"""
    try:
        headers = {'User-Agent': user_agent}
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req, timeout=10)
        content_type = response.headers.get('Content-Type', '')
        if 'text/html' not in content_type:
            return None
        return response.read()
    except Exception as e:
        print(f"{RED}Error fetching {url}: {e}{RESET}")
        return None

def extract_page_metadata(soup: BeautifulSoup):
    """Extract title and description from the page"""
    title = soup.title.string if soup.title else None
    description = None
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc:
        description = meta_desc.get('content')
    return title, description



def extract_text_content(soup: BeautifulSoup):
    """Extract and clean text content from the page"""
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.extract()
        
    # Get text
    text = soup.get_text()
    
    # Break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # Break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # Drop blank lines
    content = '\n'.join(chunk for chunk in chunks if chunk)
    return content

def extract_keywords(content: str):
    """Extract keywords and their frequencies from content"""
    
    # Tokenize and clean the text
    words = re.findall(r'\b[a-zA-Z]{3,}\b', content.lower())
    
    # Count word frequencies
    word_frequencies = collections.Counter(words)
    
    # Filter out common stop words
    stop_words = {'the', 'and', 'is', 'in', 'to', 'of', 'a', 'for', 'with', 'on', 'at', 'from', 'by'}
    for stop_word in stop_words:
        if stop_word in word_frequencies:
            del word_frequencies[stop_word]
    
    return dict(word_frequencies)

def extract_links(soup: BeautifulSoup, base_url: str):
    """Extract and normalize links from the page"""
    links = set()  # Already using a set for uniqueness
    
    for a in soup.find_all('a', href=True):
        link = a['href']
        link = urllib.parse.urljoin(base_url, link)
        parsed = urllib.parse.urlparse(link)

        # Normalize URL by removing query params and fragments
        clean_url = urllib.parse.urlunparse((
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            '', # Empty query
            ''  # Empty fragment
        )).rstrip('/')  # Remove trailing slash for consistency

        # Special handling for GitHub URLs
        if 'github.com' in parsed.netloc:
            path_parts = parsed.path.strip('/').split('/')
            if path_parts[0] == 'rhamzthev':
                if len(path_parts) == 1 or (len(path_parts) == 2 and path_parts[1]):
                    if any(keyword in parsed.netloc + parsed.path for keyword in ["rhamzthev"]):
                        links.add(clean_url)
            continue

        # Check if scheme is http/https and if names are in domain or path
        if parsed.scheme in ['http', 'https']:
            path_and_domain = parsed.netloc + parsed.path
            if any(keyword in path_and_domain for keyword in ["rhamzthev", "rhamsez"]):
                links.add(clean_url)
                
    return list(links)  # Convert to list at the end

def process_page(url: str, user_agent: str ="mycrawler"):
    """
    Process the page at 'url':
    1. Check robots.txt rules
    2. Fetch the page content
    3. Index the page in the database
    4. Extract and return hyperlinks
    """
    # Check robots.txt
    rp, is_allowed = check_robots_txt(url, user_agent)
    if not is_allowed:
        return []
    
    # Fetch HTML
    html = fetch_html(url, user_agent)
    if not html:
        return []
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Index the page
    try:
        # Extract metadata and content
        title, description = extract_page_metadata(soup)
        content = extract_text_content(soup)
        
        # Store the page in the database
        page_id = store_page(url, title, description, content)
        
        # Extract and store keywords
        word_frequencies = extract_keywords(content)
        update_keyword_page_frequencies(page_id, word_frequencies)
        
        print(f"{GREEN}Indexed: {url}{RESET}")
        
    except Exception as e:
        print(f"{RED}Error indexing {url}: {e}{RESET}")
    
    # Extract links
    links = extract_links(soup, url)

    # Respect Crawl-delay in robots.txt
    crawl_delay = rp.crawl_delay(user_agent)
    if crawl_delay:
        print(f"{YELLOW}Crawl-delay: {crawl_delay} seconds{RESET}")
        sleep(crawl_delay)

    return links

def crawl(start_urls: list[str], n_workers: int = 4, max_pages: int = 100, user_agent: str = "mycrawler"):
    """
    Perform a BFS-style web crawl starting from a list of 'start_urls',
    using 'n_workers' threads and stopping after 'max_pages' unique pages have been crawled.
    """
    # Use sets for both visited and result to ensure uniqueness
    visited = set()
    result_set = set()  # New set to track unique results
    q = queue.Queue()
    
    # Normalize and add starting URLs
    for url in start_urls:
        parsed = urllib.parse.urlparse(url)
        normalized_url = urllib.parse.urlunparse((
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            parsed.query,
            ''
        )).rstrip('/')
        
        if normalized_url not in visited:
            visited.add(normalized_url)
            q.put(normalized_url)
    
    visited_lock = threading.Lock()
    result = []  # Keep ordered list for final result
    
    def worker():
        nonlocal visited, result, result_set
        while True:
            try:
                url = q.get(timeout=1)
            except queue.Empty:
                return
            
            # Only process if not already in result_set
            if url not in result_set:
                print(f"{GREEN}Crawling: {url}{RESET}")
                result.append(url)
                result_set.add(url)
                links = process_page(url, user_agent)

                # Process new links
                for link in links:
                    parsed = urllib.parse.urlparse(link)
                    normalized_link = urllib.parse.urlunparse((
                        parsed.scheme,
                        parsed.netloc,
                        parsed.path,
                        parsed.params,
                        '',
                        ''
                    )).rstrip('/')
                    
                    with visited_lock:
                        if normalized_link not in visited and len(visited) < max_pages:
                            visited.add(normalized_link)
                            q.put(normalized_link)
                            
            q.task_done()
            sleep(5)  # Politeness delay
    
    threads = []
    for _ in range(n_workers):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)
    
    q.join()
    for t in threads:
        t.join()
    
    return result

def main():
    start_urls = ["https://www.rhamzthev.com", "https://rhed.rhamzthev.com", "https://github.com/rhamzthev", "https://github.com/rhamzthev/?tab=repositories"]
    crawled_urls = crawl(start_urls, n_workers=3, max_pages=1000, user_agent="RhamBot")
    print("\nCrawled URLs:")
    for url in crawled_urls:
        print(url)

# Example usage:
if __name__ == '__main__': 
    # print(check_robots_txt("https://linkedin.com", "RhamBot"))
    main()
