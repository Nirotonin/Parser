import requests
from bs4 import BeautifulSoup
import os
import json

def extract_links_from_page(url, save_folder):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = [a.get('href') for a in soup.find_all('a', href=True)]

    save_path = os.path.join(save_folder, 'Links_url.json')
    with open(save_path, 'w', encoding='utf-8') as file:
        json.dump(links, file, ensure_ascii=False, indent=4)

    print(f'Ссылки сохранены в {save_path}')

# Пример использования, который можно удалить
# url = "http://example.com"
# save_folder = "/path/to/save"
# extract_links_from_page(url, save_folder)
