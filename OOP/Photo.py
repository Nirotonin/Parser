import os
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import time
import base64
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
from io import BytesIO
import json

def create_folder_if_not_exists(folder_path):
    images_folder_path = os.path.join(folder_path, "images")
    if not os.path.exists(images_folder_path):
        os.makedirs(images_folder_path)

def download_image(url, folder_path, error_images):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            create_folder_if_not_exists(folder_path)  # Создаем папку, если она не существует
            # Сохраняем изображение с помощью PIL
            img = Image.open(BytesIO(response.content))
            img.save(os.path.join(folder_path, os.path.basename(urlparse(url).path)))
    except Exception as e:
        print(f"Error downloading image {url}: {e}")
        error_images.append({"name": os.path.basename(urlparse(url).path), "link": url, "error": str(e)})

def download_data_uri_image(data_uri, folder_path, error_images):
    try:
        # Извлекаем тип и данные изображения из URI
        header, image_data = data_uri.split(",", 1)
        mime_type = header.split(";")[0].split(":")[1]

        # Определяем расширение файла на основе MIME-типа
        if mime_type == "image/jpeg":
            extension = ".jpg"
        elif mime_type == "image/png":
            extension = ".png"
        elif mime_type == "image/gif":
            extension = ".gif"
        elif mime_type == "image/svg+xml":
            extension = ".svg"
        else:
            # Если тип изображения не распознан, пропускаем его
            print(f"Skipping unknown image type: {mime_type}")
            return

        # Декодируем данные изображения из base64
        image_data = base64.b64decode(image_data)

        create_folder_if_not_exists(folder_path)  # Создаем папку, если она не существует
        # Сохраняем изображение в файл с помощью PIL
        img = Image.open(BytesIO(image_data))
        img.save(os.path.join(folder_path, f"image_{len(os.listdir(folder_path))}{extension}"))
    except Exception as e:
        print(f"Error downloading data URI image: {e}")
        error_images.append({"name": f"image_{len(os.listdir(folder_path))}{extension}", "link": data_uri, "error": str(e)})

def fetch_images_from_url(url, folder_path):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options) # Используйте путь к вашему драйверу Chrome
    driver.get(url)
    time.sleep(2)  # Подождем немного, чтобы страница загрузилась полностью

    # Получаем html-код страницы
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Ищем теги <img> для изображений
    img_tags = soup.find_all('img')

    error_images = []

    # Проверяем, существует ли папка "изображения"
    create_folder_if_not_exists(folder_path)

    # Скачиваем изображения
    for img_tag in img_tags:
        img_url = img_tag.get('src')
        if img_url:
            # Проверяем, является ли изображение URL-адресом или data URI
            if img_url.startswith('data:image'):
                download_data_uri_image(img_url, os.path.join(folder_path, "images"), error_images)  # Обновленный путь
            else:
                # Преобразуем относительный URL в абсолютный
                img_url = urljoin(url, img_url)
                download_image(img_url, os.path.join(folder_path, "images"), error_images)  # Обновленный путь

    driver.quit()

    # Сохраняем файл JSON с ошибками загрузки изображений
    if error_images:
        with open(os.path.join(folder_path, "images", "error_images.json"), "w") as json_file:  # Обновленный путь
            json.dump(error_images, json_file, indent=4)
