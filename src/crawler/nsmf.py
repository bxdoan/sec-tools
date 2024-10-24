import os
import re

import requests
from bs4 import BeautifulSoup
import unidecode
from pipenv.patched.safety.constants import YELLOW

ROOT_REPO = os.path.dirname(os.path.abspath(__file__))
# DES_FOLDER = f'{ROOT_REPO}/../../data/crawler/nhasachmienphi'
DES_FOLDER = f'D:/books/nsmp'

GREEN = '\033[32m'
YELLOW = '\033[33m'
RED = '\033[31m'
END_COLOR = '\033[0m'

def get_html(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.text
    except requests.exceptions.RequestException as e:
        print(e)
        return None


def find_href_in_class(html, class_name):
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup.find_all(class_=class_name):
        if tag.name == 'a' and 'href' in tag.attrs:
            return tag['href']


def find_text_in_class(html, class_name):
    soup = BeautifulSoup(html, 'html.parser')
    texts = []
    for tag in soup.find_all(class_=class_name):
        texts.append(tag.get_text(strip=True))
    return texts


def find_h1_text(html):
    soup = BeautifulSoup(html, 'html.parser')
    h1_tag = soup.find('h1')
    if h1_tag:
        return h1_tag.get_text(strip=True)
    return None


def download_file(url, file_name, des_path):
    # if exist file then skip
    if os.path.exists(f'{des_path}/{file_name}'):
        print(f'{YELLOW}{file_name} is exist{END_COLOR}')
        return

    try:
        r = requests.get(url, stream=True)
        with open(f'{des_path}/{file_name}', 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
    except requests.exceptions.RequestException as e:
        print(f'{RED}Error download file:{END_COLOR}\n {e}, skip {file_name}')


def download_files(html, file_name, des_path):
    file_exts = ['epub', 'ebook', 'mobi', 'pdf']
    for fes in file_exts:
        link = find_href_in_class(html, f'button {fes}')
        if link:
            print(f'Downloading {fes.upper()} file: {link}')
            download_file(link, f'{file_name}.{fes}', des_path)


def get_author(html):
    texts = find_text_in_class(html, 'mg-t-10')
    for t in texts:
        if 'Tác giả' in t:
            return t.split(':')[1].strip()


def get_category(html):
    texts = find_text_in_class(html, 'mg-tb-10')
    for t in texts:
        if 'Thể loại' in t:
            return t.split(':')[1].strip()


def get_image_book(html, name_folder, full_path_folder):
    soup = BeautifulSoup(html, 'html.parser')
    img_tags = soup.find_all('img')
    if img_tags[2]:
        # download image
        img_url = img_tags[2]['src']
        ext_file = img_url.split('.')[-1]
        download_file(img_url, f'{name_folder}.{ext_file}', full_path_folder)
        return img_tags[2]['src']
    return None


def write_content_to_file(content, file_path):
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)


def sanitize_name(name):
    # Replace any non-alphanumeric character with an underscore
    name = unidecode.unidecode(name.replace(' ', '-').lower())
    sanitized_name = re.sub(r'[^a-zA-Z0-9]', '-', name)
    # Remove duplicate underscores
    sanitized_name = re.sub(r'-+', '-', sanitized_name)
    # Remove leading and trailing underscores
    sanitized_name = sanitized_name.strip('_')
    sanitized_name = sanitized_name.replace('_', '-')
    return sanitized_name


def rename_items(root_folder):
    for root, dirs, files in os.walk(root_folder, topdown=False):
        for name in files:
            sanitized_name = sanitize_name(name)
            if name != sanitized_name:
                os.rename(os.path.join(root, name), os.path.join(root, sanitized_name))
        for name in dirs:
            sanitized_name = sanitize_name(name)
            if name != sanitized_name:
                os.rename(os.path.join(root, name), os.path.join(root, sanitized_name))


def process(url_book=None):
    if not url_book:
        return None
    html = get_html(url_book)
    if html:
        name = find_h1_text(html)
        print(f"Name: {name}")
        # replace space with underscore and lower case and english character
        name_folder = sanitize_name(name)

        # create folder
        full_path_folder = f'{DES_FOLDER}/{name_folder}'
        # if folder exist and have content.txt then skip
        if os.path.exists(full_path_folder) and os.path.exists(f'{full_path_folder}/content.txt'):
            print(f'{YELLOW}Folder {name_folder} is exist{END_COLOR}')
            return

        os.makedirs(full_path_folder, exist_ok=True)

        # download files to folder
        download_files(html, name_folder, full_path_folder)

        # get content
        author = get_author(html)
        category_name = get_category(html)
        img_book = get_image_book(html, name_folder, full_path_folder)
        descriptions = find_text_in_class(html, 'content_p content_p_al')
        content = f'{name_folder}|{name}|{author}|{category_name}|{descriptions}'
        write_content_to_file(content, f'{full_path_folder}/content.txt')

        print(f"name_folder: {name_folder}\nauthor: {author}\ncategory: {category_name}\n"
              f"description: {' '.join(descriptions)}\nimg_book: {img_book}")
    else:
        print('Error get html')


def write_link_to_file(links, file_path):
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))

    with open(file_path, 'w', encoding='utf-8') as f:
        for link in links:
            f.write(f'{link}\n')

def find_href_category_link():
    url = 'https://nhasachmienphi.com'
    html = get_html(url)
    hrefs = []
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        for tag in soup.find_all('div', class_='item_folder'):
            for a_tag in tag.find_all('a', href=True):
                print(f'Category url: {a_tag["href"]}')
                hrefs.append(a_tag['href'])
    return hrefs

def find_book_link(url_category, hrefs=None):
    html = get_html(url_category)
    if not hrefs:
        hrefs = []

    if html:
        soup = BeautifulSoup(html, 'html.parser')
        for tag in soup.find_all('a', class_='title_sach'):
            hrefs.append(tag['href'])

        href_next_page = None
        for tag in soup.find_all('a', class_='nextpostslink'):
            href_next_page = tag['href']

        href_last_page = None
        for tag in soup.find_all('a', class_='last'):
            href_last_page = tag['href']

        if href_next_page and href_next_page != href_last_page:
            return find_book_link(href_next_page, hrefs)
    return hrefs

def process_category(url_category):
    href_books = find_book_link(url_category)
    print(f'href_books: {len(href_books)}')
    for i, href in enumerate(href_books):
        print(f"{GREEN}==== File {i+1}/{len(href_books)}: {href} ===={END_COLOR}")
        process(href)

def main():
    # href_categories = find_href_category_link()
    # print(f'href_categories: {len(href_categories)}')
    # write_link_to_file(href_categories, f'{DES_FOLDER}/categories.txt')

    read_link_categories = open(f'{DES_FOLDER}/categories.txt', 'r').readlines()
    for x, link in enumerate(read_link_categories):
        link = link.strip()
        print(f"{GREEN}==== Category {x+1}/{len(read_link_categories)}: {link} ===={END_COLOR}")
        href_books = find_book_link(link)
        print(f'href_books: {len(href_books)}')
        for i, href in enumerate(href_books):
            print(f"{GREEN}==== Category {x+1}/{len(read_link_categories)} | Book {i + 1}/{len(href_books)}: {href} ===={END_COLOR}")
            process(href)

if __name__ == '__main__':
    main()
    # process_category("https://nhasachmienphi.com/category/am-thuc-nau-an")
    # rename_items(DES_FOLDER)