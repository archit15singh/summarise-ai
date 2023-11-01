import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from langchain.llms import Ollama
from langchain.document_loaders import WebBaseLoader
from langchain.chains.summarize import load_summarize_chain
import time
import concurrent.futures
from tqdm import tqdm

base_url = 'https://ollama.ai/blog'

def scrape_links(url):
    scraped_links = []
    try:
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            for link in soup.find_all('a'):
                href = link.get('href')
                if href:
                    absolute_url = urljoin(url, href)

                    if absolute_url.startswith(base_url):
                        scraped_links.append(absolute_url)
    except Exception as e:
        print(f"Error while scraping links from {url}: {str(e)}")

    return scraped_links

def process_url(url):
    print(f"Processing URL: {url}")
    loader = WebBaseLoader(url)
    docs = loader.load()
    print(f"Loaded {len(docs)} documents from {url}")

    llm = Ollama(model="mistral-openorca")
    chain = load_summarize_chain(llm, chain_type="stuff")
    result = chain.run(docs)
    print(f"Length of result for {url}: {len(result)}")
    print(result)

start_url = base_url
s = time.time()
all_scraped_links = set()

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    futures = {executor.submit(scrape_links, url): url for url in scrape_links(start_url)}

    for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Scraping Links"):
        url = futures[future]
        scraped_links = future.result()
        all_scraped_links.update(scraped_links)

print(f"Total unique scraped links: {len(all_scraped_links)}")

for url in tqdm(all_scraped_links, desc="Processing URLs"):
    process_url(url)

e = time.time()
print(f"Total scraped links: {len(all_scraped_links)}, Time taken: {e-s}")
