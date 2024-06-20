import os
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import time
import base64
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
from io import BytesIO
import json

def download_image(url, folder_path, error_images):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            img.save(os.path.join(folder_path, os.path.basename(urlparse(url).path)))
    except Exception as e:
        print(f"Error downloading image {url}: {e}")
        error_images.append({"name": os.path.basename(urlparse(url).path), "link": url, "error": str(e)})

def download_data_uri_image(data_uri, folder_path, error_images):
    global extension
    try:
        header, image_data = data_uri.split(",", 1)
        mime_type = header.split(";")[0].split(":")[1]

        if mime_type == "image/jpeg":
            extension = ".jpg"
        elif mime_type == "image/png":
            extension = ".png"
        elif mime_type == "image/gif":
            extension = ".gif"
        elif mime_type == "image/svg+xml":
            extension = ".svg"
        else:
            print(f"Skipping unknown image type: {mime_type}")
            return

        image_data = base64.b64decode(image_data)
        img = Image.open(BytesIO(image_data))
        img.save(os.path.join(folder_path, f"image_{len(os.listdir(folder_path))}{extension}"))
    except Exception as e:
        print(f"Error downloading data URI image: {e}")
        error_images.append({"name": f"image_{len(os.listdir(folder_path))}{extension}", "link": data_uri, "error": str(e)})

def fetch_images_from_url(url, folder_path, visited_urls, error_images, driver):
    if url in visited_urls:
        return

    visited_urls.add(url)
    driver.get(url)
    time.sleep(2)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    img_tags = soup.find_all('img')

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    site_images_folder = os.path.join(folder_path, "images_from_site")
    if not os.path.exists(site_images_folder):
        os.makedirs(site_images_folder)

    for img_tag in img_tags:
        img_url = img_tag.get('src')
        if img_url:
            if img_url.startswith('data:image'):
                download_data_uri_image(img_url, site_images_folder, error_images)
            else:
                img_url = urljoin(url, img_url)
                download_image(img_url, site_images_folder, error_images)

    link_tags = soup.find_all('a', href=True)
    for link_tag in link_tags:
        link_url = urljoin(url, link_tag['href'])
        if urlparse(link_url).netloc == urlparse(url).netloc:
            fetch_images_from_url(link_url, folder_path, visited_urls, error_images, driver)

def main(url, save_directory):
    url = url
    folder_path = save_directory

    visited_urls = set()
    error_images = []

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    try:
        fetch_images_from_url(url, folder_path, visited_urls, error_images, driver)
    finally:
        driver.quit()

    if error_images:
        with open(os.path.join(folder_path, "error_images.json"), "w") as json_file:
            json.dump(error_images, json_file, indent=4)

if __name__ == "__main__":
    main()
