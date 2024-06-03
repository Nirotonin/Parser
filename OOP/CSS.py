import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def extract_css_from_page(url, save_directory):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    css_files = []

    for link in soup.find_all('link', rel='stylesheet'):
        css_url = urljoin(url, link['href'])
        css_files.append(css_url)
        css_content = requests.get(css_url).text
        file_name = os.path.join(save_directory, os.path.basename(link['href']))
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(css_content)

    return css_files

# Пример использования
# url = url
# save_directory = save_directory
# css_files = extract_css_from_page(url, save_directory)
# print(f"CSS файлы сохранены: {css_files}")