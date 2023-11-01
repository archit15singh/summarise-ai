import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import deque

base_url = 'https://ollama.ai/blog'
max_depth = 2

def scrape_links_recursive(start_url, max_depth):
    visited = set()
    to_visit = deque([(start_url, 0])

    while to_visit:
        current_url, depth = to_visit.popleft()

        if depth > max_depth:
            continue

        if current_url in visited:
            continue

        try:
            response = requests.get(current_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                for link in soup.find_all('a'):
                    href = link.get('href')
                    if href:
                        absolute_url = urljoin(current_url, href)
                        if absolute_url.startswith(base_url):
                            print(absolute_url)
                            to_visit.append((absolute_url, depth + 1))
                            visited.add(absolute_url)

        except Exception as e:
            print(f"Error: {str(e)}")

start_url = base_url
scrape_links_recursive(start_url, max_depth)
