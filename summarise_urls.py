import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import deque
import argparse
from langchain.llms import Ollama
from langchain.document_loaders import WebBaseLoader
from langchain.chains.summarize import load_summarize_chain

def scrape_links_iteration(start_url, max_depth):
    visited = set()
    to_visit = deque([(start_url, 0)])
    scraped_links = []

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

                links = soup.find_all('a')
                print(f'found {len(links)} in url: {current_url}')
                for link in links:
                    href = link.get('href')
                    if href:
                        absolute_url = urljoin(current_url, href)
                        if absolute_url.startswith(base_url):
                            scraped_links.append(absolute_url)
                            to_visit.append((absolute_url, depth + 1))
                            visited.add(absolute_url)

        except Exception as e:
            print(f"Error: {str(e)}")

    scraped_links = list(set(scraped_links))
    return scraped_links

def process_url(url):
    print(f"Processing URL: {url}")
    loader = WebBaseLoader(url)
    docs = loader.load()
    print(f"length: {len(docs[0].page_content)} for url: {url}")

    llm = Ollama(model="mistral-openorca")
    chain = load_summarize_chain(llm, chain_type="stuff")
    result = chain.run(docs)
    print(f"Length of result for {url}: {len(result)}")
    print(result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base_url", type=str, required=True, help="Base URL to start scraping from")
    parser.add_argument("--max_depth", type=int, required=True, help="Maximum depth for recursion")
    args = parser.parse_args()

    base_url = args.base_url
    max_depth = args.max_depth
    start_url = base_url

    unique_scraped_links = scrape_links_iteration(start_url, max_depth)
    print(f"found {len(unique_scraped_links} final from url:{base_url}")
    for link in unique_scraped_links:
        print('*'*100)
        process_url(link)
