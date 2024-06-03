import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse
import time

visited = set()


def get_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text(separator='\n')
    return text, soup


def save_text_to_file(text, folder_path, filename):
    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)
    print(f"Текст сохранен в {file_path}")


def crawl_site(base_url, folder_path):
    to_visit = [base_url]

    while to_visit:
        current_url = to_visit.pop(0)
        if current_url in visited:
            continue

        visited.add(current_url)
        try:
            text, soup = get_text_from_url(current_url)
            parsed_url = urlparse(current_url)
            filename = f"{parsed_url.netloc}{parsed_url.path}".replace("/", "_") + ".txt"
            save_text_to_file(text, folder_path, filename)

            for link in soup.find_all('a', href=True):
                absolute_link = urljoin(current_url, link['href'])
                if urlparse(absolute_link).netloc == urlparse(base_url).netloc:
                    to_visit.append(absolute_link)

            time.sleep(1)  # добавляем задержку, чтобы не нагружать сервер

        except Exception as e:
            print(f"Ошибка при обработке {current_url}: {e}")


def main(url, save_directory):
    base_url = url
    folder_path = save_directory

    if not os.path.exists(folder_path):
        print(f"Путь {folder_path} не существует.")
        return

    crawl_site(base_url, folder_path)


if __name__ == "__main__":
    main()
