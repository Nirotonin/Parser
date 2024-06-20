from selenium import webdriver
from selenium.webdriver.common.by import By
import os


def extract_links_from_site(url, save_folder):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    visited = set()
    to_visit = set([url])
    all_links = set()

    while to_visit:
        current_url = to_visit.pop()
        visited.add(current_url)

        driver.get(current_url)
        elements = driver.find_elements(By.TAG_NAME, 'a')
        links = [elem.get_attribute('href') for elem in elements if elem.get_attribute('href')]

        for link in links:
            if link.startswith(url):
                if link not in visited and link not in to_visit:
                    to_visit.add(link)
            all_links.add(link)

    driver.quit()

    save_path = os.path.join(save_folder, 'links_from_all_site.json')
    with open(save_path, 'w') as file:
        file.write('const links = ' + str(list(all_links)) + ';\n')

    print(f'Ссылки (глобально) сохранены в {save_path}')

