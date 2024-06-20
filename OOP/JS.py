import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote

def sanitize_filename(filename):
    # Функция для замены недопустимых символов
    return quote(filename, safe='')

def get_js_from_page(url, save_path):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Создаем папку, если она не существует
    os.makedirs(save_path, exist_ok=True)

    scripts = soup.find_all('script', src=True)
    for script in scripts:
        script_url = urljoin(url, script['src'])
        script_response = requests.get(script_url)
        sanitized_filename = sanitize_filename(os.path.basename(script['src']))
        script_filename = os.path.join(save_path, sanitized_filename)
        with open(script_filename, 'w', encoding='utf-8') as f:
            f.write(script_response.text)

    print(f"JavaScript файлы сохранены в {save_path}")
