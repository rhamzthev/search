import os
import psycopg
from psycopg import Cursor, Connection
from psycopg.abc import Query, Params
from psycopg_pool import ConnectionPool
from typing import Dict, Generator, Iterable, List, Optional, Tuple, Any
from dotenv import load_dotenv
from contextlib import contextmanager
import re
import math

load_dotenv()

# Global connection pool
_pool = None

def get_pool() -> ConnectionPool:
    """Get or create the connection pool."""
    global _pool
    if _pool is None:
        _pool = ConnectionPool(
            conninfo=f"host={os.getenv('DB_HOST')} "
                    f"port={os.getenv('DB_PORT')} "
                    f"dbname={os.getenv('DB_NAME')} "
                    f"user={os.getenv('DB_USER')} "
                    f"password={os.getenv('DB_PASSWORD')}",
            min_size=5,
            max_size=20,
            max_idle=300  # 5 minutes max idle time
        )
    return _pool

@contextmanager
def _get_connection():
    """Get a connection from the pool."""
    pool = get_pool()
    conn = pool.getconn()
    try:
        # Deal with prepared statements
        conn.execute("DEALLOCATE ALL")
        yield conn
        conn.commit()
    finally:
        # Cleanup prepared statements before returning connection to pool
        conn.execute("DEALLOCATE ALL")
        pool.putconn(conn)

def store_page(url: str, title: Optional[str], description: Optional[str], content: str) -> int:
    """
    Store a page in the database and return its ID.
    If the page already exists, update it.
    """
    # Check if page exists
    with _get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM pages WHERE url = %s", (url,))
            result = cur.fetchone()
            
            if result:
                # Update existing page
                cur.execute("""
                    UPDATE pages 
                    SET title = %s, description = %s, content = %s, last_crawled = CURRENT_TIMESTAMP
                    WHERE url = %s
                    RETURNING id
                """, (title, description, content, url))

                conn.commit()
                return cur.fetchone()[0]
            else:
                # Insert new page
                cur.execute("""
                    INSERT INTO pages (url, title, description, content)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                """, (url, title, description, content))
                id = cur.fetchone()[0]

                conn.commit()
                return id

def _store_keywords(cur: Cursor, words: List[str]) -> Dict[str, int]:
    """
    Store keywords in the database and return a dictionary mapping words to their IDs.
    """

    # Prepare the words for bulk insert
    words_list = [(word,) for word in words]
    
    # Try to insert all words at once
    cur.executemany("""
        INSERT INTO keywords (word)
        VALUES (%s)
        ON CONFLICT (word) DO NOTHING
    """, words_list)
    
    # Get all word IDs in one query
    cur.execute("""
        SELECT word, id FROM keywords 
        WHERE word = ANY(%s)
    """, (list(words),))
    
    # Create word to ID mapping
    word_ids = dict(cur.fetchall())
    
    return word_ids

def update_keyword_page_frequencies(page_id: int, word_frequencies: Dict[str, int]):
    """
    Update the keyword-page frequencies for a given page.
    """
    with _get_connection() as conn:
        with conn.cursor() as cur:
            # # Handle keywords and frequencies in a single transaction

            word_ids = _store_keywords(cur, word_frequencies.keys())
            
            # Delete existing frequencies
            cur.execute("DELETE FROM keyword_pages WHERE page_id = %s", (page_id,))
            
            # Insert new frequencies
            freq_data = [(word_ids[word], page_id, freq) for word, freq in word_frequencies.items()]
            cur.executemany("""
                INSERT INTO keyword_pages (keyword_id, page_id, frequency)
                VALUES (%s, %s, %s)
            """, freq_data)

            conn.commit()

def search_pages(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Search pages using TF-IDF ranking based on the query.
    
    Args:
        query: The search query string
        limit: Maximum number of results to return
        
    Returns:
        List of page dictionaries with ranking scores
    """
    # Tokenize the query into words
    query_words = [word.lower() for word in re.findall(r'\b[a-zA-Z]{3,}\b', query)]
    
    if not query_words:
        return []
    
    with _get_connection() as conn:
        with conn.cursor() as cur:
            # Get total number of documents
            cur.execute("SELECT COUNT(*) FROM pages")
            total_docs = cur.fetchone()[0]
            
            # Get matching pages and calculate TF-IDF
            results = []
            
            # For each query word, get matching documents and their frequencies
            for word in query_words:
                cur.execute("""
                    SELECT p.id, p.url, p.title, p.description, kp.frequency, 
                           (SELECT COUNT(*) FROM keyword_pages WHERE keyword_id = k.id) as doc_frequency
                    FROM pages p
                    JOIN keyword_pages kp ON p.id = kp.page_id
                    JOIN keywords k ON kp.keyword_id = k.id
                    WHERE k.word = %s
                """, (word,))
                
                rows = cur.fetchall()
                
                for row in rows:
                    page_id, url, title, description, term_freq, doc_freq = row
                    
                    # Calculate TF-IDF
                    tf = term_freq  # Term frequency
                    idf = math.log(total_docs / (doc_freq or 1))  # Inverse document frequency
                    score = tf * idf
                    
                    # Check if page is already in results
                    page_exists = False
                    for result in results:
                        if result['id'] == page_id:
                            result['score'] += score
                            page_exists = True
                            break
                    
                    if not page_exists:
                        results.append({
                            'id': page_id,
                            'url': url,
                            'title': title or url,
                            'description': description or '',
                            'score': score
                        })
            
            # Sort results by score in descending order
            results.sort(key=lambda x: x['score'], reverse=True)
            
            # Return top results
            return results[:limit]