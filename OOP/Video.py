from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import time
import os

def download_videos(url, download_folder):
    # Настройка Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Запуск в фоновом режиме
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    # Открываем веб-страницу
    driver.get(url)

    # Задержка для загрузки контента
    time.sleep(5)

    # Извлечение HTML-кода страницы
    page_source = driver.page_source

    # Закрываем драйвер
    driver.quit()

    # Анализируем страницу с помощью BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Поиск всех тегов <video> и источников видео
    video_sources = []
    video_tags = soup.find_all('video')
    for video_tag in video_tags:
        source_tag = video_tag.find('source')
        if source_tag and 'src' in source_tag.attrs:
            video_sources.append(source_tag['src'])

    # Проверка найденных видео URL
    if not video_sources:
        print("Источники видео не найдены.")
        return

    # Создаем папку для сохранения видео, если ее нет
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Скачивание видео
    for i, video_url in enumerate(video_sources):
        try:
            video_content = requests.get(video_url).content
            video_path = os.path.join(download_folder, f'video_{i}.mp4')
            with open(video_path, 'wb') as video_file:
                video_file.write(video_content)
            print(f'Video {i} downloaded from {video_url}')
        except Exception as e:
            print(f'Failed to download video {i} from {video_url}: {e}')

    print('Успешная загрузка.')

# Пример использования функции
# download_folder = input("Путь ")  # Укажите путь к папке для сохранения видео
# download_videos('https://ru.freepik.com/free-video/cute-little-daughter-embracing-her-happy-mother-from-back-park_171476', download_folder)
