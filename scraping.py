import time
from typing import List
from pathlib import Path

import chromedriver_binary
from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementClickInterceptedException
from tqdm import tqdm


def is_valid_artist_id(artist_id: str) -> bool:
    """Validate artist_id

    Parameters
    ----------
    artist_id: str
        CHEERZ artist ID

    Returns
    -------
    bool

    """
    try:
        int(artist_id)
    except ValueError:
        return False
    url = f'https://cheerz.cz/artist/{artist_id}/community'
    ua = (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
    )
    headers = {
        'user-Agent': ua,
    }
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        return False
    return True


def create_img_directory(directory_name: str) -> str:
    """ Create directory for images.

    Parameters
    ----------
    directory_name: str
        directory name

    Returns
    -------
    str
        Directory path as str.

    """
    dir_name = '_'.join(directory_name.split(' '))
    path = Path(f'img/{dir_name}')
    if not path.exists():
        path.mkdir(exist_ok=False)
    return str(path)


def init_driver() -> webdriver.Chrome:
    """ Initialize webdriver

    Returns
    -------
    webdriver.Chrome

    """
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    return driver


def get_pages(driver: webdriver.Chrome, url: str) -> List[str]:
    """

    Parameters
    ----------
    driver: webdriver.Chrome
        webdriver
    url: str
        URL for CHEERZ artist community page.

    Returns
    -------
    pages: List[str]
        List of page source of CHEERZ artist community page.

    """
    pages = []
    driver.get(url)
    print('Fetch page sources.')
    while True:
        try:
            next_page = driver.find_element_by_id('pageNext')
            html = driver.page_source
            pages.append(html)
            next_page.click()
        except ElementClickInterceptedException:
            driver.close()
            driver.quit()
            print(f'Accomplished. {len(pages)} sources has fetched.')
            return pages


def extract_img_urls(pages: List[str]) -> List[str]:
    """ Extract image urls from CHEERZ artist community page.

    Parameters
    ----------
    pages: List[str]
        List of page source of CHEERZ artist community page.

    Returns
    -------
    img_urls: List[str]
        List of image urls.

    """
    img_urls = []
    print('Extract image URLs.')
    for idx, page in enumerate(pages):
        soup = bs(page, 'html.parser')
        thumbnail = soup.find_all('dt', class_='thumb')
        for thumb in thumbnail:
            img_url = thumb.find('img')
            img_urls.append(img_url['src'])
    print(f'Accomplished. {len(img_urls)} URLs has extracted.')
    return img_urls


def count_exist_images(directory: str) -> int:
    """ Count exist images in save directory.

    Parameters
    ----------
    directory: str
        Directory path as str

    Returns
    -------
    int
        number of images already saved in directory.

    """
    path = Path(directory)
    return len(list(path.glob('*.jpeg')))


def save_imgs(img_urls: List[str], directory: str) -> None:
    """ Save images. Order for save is old to new.

    Parameters
    ----------
    img_urls: List[str]
        List of image urls.
    directory: str
        Directory path for save as str.

    Returns
    -------

    """
    img_urls.reverse()
    print('Save images.')

    urls = img_urls[::]
    start = 1

    exists_images = count_exist_images(directory)
    if exists_images:
        diff = len(img_urls) - exists_images
        print(f'Exist images: {exists_images}')
        print(f'New Images: {diff}')
        urls = img_urls[exists_images::]
        start = exists_images + 1

    for idx, img_url in enumerate(tqdm(urls), start=start):
        res = requests.get(img_url)
        filename = f'{directory}/{str(idx).zfill(4)}.jpeg'
        with open(filename, 'wb') as f:
            f.write(res.content)
        time.sleep(0.25)
    print('Accomplished.')


def main():
    id_is_valid = False
    artist_id = ''
    while not id_is_valid:
        artist_id = input('CHEERZ artist ID: ')
        id_is_valid = is_valid_artist_id(artist_id)
    directory_name = input('directory name (Optional. Default is artist id.): ')
    if not directory_name:
        directory_name = artist_id

    dir_name = create_img_directory(directory_name)
    driver = init_driver()
    url = f'https://cheerz.cz/artist/{artist_id}/community'
    pages = get_pages(driver, url)
    img_urls = extract_img_urls(pages)
    save_imgs(img_urls, directory=dir_name)


if __name__ == '__main__':
    main()
