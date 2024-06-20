import requests
import os

def fetch_html_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # проверка успешности запроса
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к URL: {e}")
        return None

def save_html_to_file(html, directory, filename):
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, filename)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(html)

