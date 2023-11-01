# summarise-ai

provide a base url to it
it will get all the links in it.
it will scrape the content from it and summarise the text.


docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/llama2

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python summ.py # after changing url in summ.py 

python recurse_links.py --base_url https://ollama.ai/blog --max_depth 2
