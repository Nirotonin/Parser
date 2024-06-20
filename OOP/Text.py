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

def remove_extra_spaces(text):
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        cleaned_line = ' '.join(line.split())  # Remove extra spaces
        cleaned_lines.append(cleaned_line)
    return '\n'.join(cleaned_lines)

def remove_extra_paragraphs(text):
    lines = text.split('\n')
    cleaned_lines = []
    consecutive_newlines = 0
    for line in lines:
        if line.strip():  # If line is not empty
            cleaned_lines.append(line)
            consecutive_newlines = 0
        else:
            consecutive_newlines += 1
            if consecutive_newlines <= 2:
                cleaned_lines.append(line)
    return '\n'.join(cleaned_lines)

def main(url, save_directory):
    url = url
    folder_path = save_directory

    if not os.path.exists(folder_path):
        print(f"Путь {folder_path} не существует.")
        return

    text = get_text_from_url(url)
    cleaned_text = remove_extra_paragraphs(text)
    cleaned_text = remove_extra_spaces(cleaned_text)
    save_text_to_file(cleaned_text, folder_path)

if __name__ == "__main__":
    url = input("Введите URL: ")
    save_directory = input("Введите путь для сохранения: ")
    main(url, save_directory)
