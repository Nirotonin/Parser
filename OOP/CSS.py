import os
import requests
import logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin

logging.basicConfig(filename='error.log', level=logging.ERROR)

def extract_css_from_page(url, save_directory):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверяем, есть ли ошибки в запросе
        soup = BeautifulSoup(response.text, 'html.parser')

        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        css_files = []

        for link in soup.find_all('link', rel='stylesheet'):
            try:
                css_url = urljoin(url, link['href'])
                css_response = requests.get(css_url)
                css_response.raise_for_status()  # Проверяем, есть ли ошибки при загрузке CSS
                css_content = css_response.text
                file_name = os.path.join(save_directory, os.path.basename(link['href']))
                with open(file_name, 'w', encoding='utf-8') as file:
                    file.write(css_content)
                css_files.append(css_url)
            except requests.exceptions.RequestException as css_e:
                logging.error(f"Error extracting CSS from {css_url}: {css_e}")

        return css_files

    except requests.exceptions.RequestException as e:
        logging.error(f"Error accessing {url}: {e}")
        return []  # Возвращаем пустой список в случае ошибки

