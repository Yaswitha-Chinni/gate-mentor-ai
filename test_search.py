import sqlite3
from duckduckgo_search import DDGS

def get_first_result(query, site_filter=None):
    if site_filter:
        query = f"{query} site:{site_filter}"
    try:
        results = DDGS().text(query, max_results=1)
        if results:
            return results[0]['href']
    except Exception as e:
        print(f"Error fetching {query}: {e}")
    return None

print(get_first_result("GATE CSE Programming in C", "youtube.com"))
print(get_first_result("Programming in C GATE CSE", "geeksforgeeks.org"))
print(get_first_result("Programming in C GATE questions", "gateoverflow.in"))
