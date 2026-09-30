import urllib.request
import urllib.parse
import re
import json
import time
from datetime import datetime

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def search_duckduckgo_html(query, max_results=15):
    """
    Searches DuckDuckGo HTML endpoint for business listings, snippets, and contact details.
    """
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query)
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5"
    }
    
    req = urllib.request.Request(url, headers=headers)
    records = []
    
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
            
            # Find result blocks
            # Look for result__body or individual snippet links
            links = re.findall(r'<a class="result__url"[^>]*href="([^"]+)"[^>]*>', html)
            snippets = re.findall(r'<a class="result__snippet"[^>]*>(.*?)</a>', html, re.DOTALL)
            titles = re.findall(r'<h2 class="result__title">.*?<a[^>]*>(.*?)</a>', html, re.DOTALL)
            
            min_len = min(len(links), len(snippets), len(titles))
            for i in range(min(min_len, max_results)):
                raw_url = links[i].strip()
                # Duckduckgo wraps urls in /l/?uddg=...
                match_url = re.search(r'uddg=([^&]+)', raw_url)
                if match_url:
                    actual_url = urllib.parse.unquote(match_url.group(1))
                else:
                    actual_url = raw_url
                
                clean_title = re.sub(r'<[^<]+?>', '', titles[i]).strip()
                clean_snippet = re.sub(r'<[^<]+?>', '', snippets[i]).strip()
                
                records.append({
                    "source_type": "web_directory",
                    "source_id": f"web_{hash(actual_url) & 0xffffffff:x}",
                    "source_url": actual_url,
                    "title": clean_title,
                    "snippet": clean_snippet,
                    "query_used": query,
                    "raw_payload": json.dumps({
                        "title": clean_title,
                        "snippet": clean_snippet,
                        "url": actual_url,
                        "query": query
                    }, ensure_ascii=False),
                    "extracted_at": datetime.utcnow().isoformat()
                })
    except Exception as e:
        print(f"Error querying DDG for '{query}': {e}")
        
    return records

if __name__ == "__main__":
    print("Testing Web Harvester for 'agrovet Tegeta Dar es Salaam'...")
    results = search_duckduckgo_html("agrovet Tegeta Dar es Salaam")
    print(f"Found {len(results)} results:")
    for r in results[:5]:
        print("- Title:", r["title"][:50], "| URL:", r["source_url"][:60])
        print("  Snippet:", r["snippet"][:100])