# summarise-ai

- provide a base url to it
- it will get all the links in it recursively
- it will scrape the content from all the urls and summarise the text for each.


docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/llama2

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


try:
- python summarise_urls.py --base_url https://ollama.ai/blog --max_depth 2 --data_folder ollama
- python summarise_urls.py --base_url https://yourstory.com/companies --max_depth 2 --data_folder yourstory
- python summarise_urls.py --base_url https://openai.com/blog --max_depth 2 --data_folder openai
