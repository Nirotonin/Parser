import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup


def view_css_from_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверяем, есть ли ошибки в запросе
        soup = BeautifulSoup(response.text, 'html.parser')

        css_code = []

        for link in soup.find_all('link', rel='stylesheet'):
            try:
                css_url = urljoin(url, link['href'])
                css_response = requests.get(css_url)
                css_response.raise_for_status()  # Проверяем, есть ли ошибки при загрузке CSS
                css_content = css_response.text
                css_code.append(css_content)
            except requests.exceptions.RequestException as css_e:
                logging.error(f"Error extracting CSS from {css_url}: {css_e}")

        return css_code

    except requests.exceptions.RequestException as e:
        logging.error(f"Error accessing {url}: {e}")
        return []  # Возвращаем пустой список в случае ошибки

def view_js_from_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверяем, есть ли ошибки в запросе
        soup = BeautifulSoup(response.text, 'html.parser')

        js_code = []

        scripts = soup.find_all('script', src=True)
        for script in scripts:
            script_url = urljoin(url, script['src'])
            script_response = requests.get(script_url)
            js_code.append(script_response.text)

        return js_code

    except requests.exceptions.RequestException as e:
        logging.error(f"Error accessing {url}: {e}")
        return []  # Возвращаем пустой список в случае ошибки
