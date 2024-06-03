import requests
from bs4 import BeautifulSoup
import os

def get_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text(separator='\n')
    return text

def save_text_to_file(text, folder_path):
    file_path = os.path.join(folder_path, 'page_text.txt')
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)
    print(f"Текст сохранен в {file_path}")

def main(url, save_directory):
    url = url
    folder_path = save_directory

    if not os.path.exists(folder_path):
        print(f"Путь {folder_path} не существует.")
        return

    text = get_text_from_url(url)
    save_text_to_file(text, folder_path)

if __name__ == "__main__":
    main()
