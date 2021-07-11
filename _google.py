import re
import time

from urllib.parse import urlparse, urlencode

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup


def google_scraper(driver, name):
    youtube_link = None
    twitter_link = None

    search_q = urlencode({'q': f'{name} twitter profile'})
    driver.get(f'https://google.com/search?{search_q}')

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "search"))
    )

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    for res in soup.select('#search h3'):
        try:
            link = res.find_parent('a')['href']
            twitter = re.search(r'^https:\/\/twitter\.com\/\w+', link)
            if not twitter_link and twitter and len(urlparse(link).path.split('/')) == 2:
                twitter_link = link
            if twitter_link:
                break
        except:
            pass

    search_q = urlencode({'q': f'{name} youtube channel'})
    driver.get(f'https://google.com/search?{search_q}')

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "search"))
    )

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    for res in soup.select('#search h3'):
        try:
            link = res.find_parent('a')['href']
            youtube = re.search(r'https\:\/\/www\.youtube\.com\/channel\/\w+', link)
            if not youtube_link and youtube and len(urlparse(link).path.split('/')) == 3:
                youtube_link = link
            if youtube_link:
                break
        except:
            pass

    time.sleep(2)

    return {'youtube_link': youtube_link, 'twitter_link': twitter_link}
