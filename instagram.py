import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from parser import Parser, get_influencer


def ig_login(driver, uname, ig_password):
    driver.get('https://instagram.com/accounts/login/')

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
    )

    driver.get_screenshot_as_file("screenshot.png")

    username=driver.find_element_by_css_selector("input[name='username']")
    password=driver.find_element_by_css_selector("input[name='password']")
    username.clear()
    password.clear()
    username.send_keys(uname)
    password.send_keys(ig_password)
    login = driver.find_element_by_css_selector("button[type='submit']").click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Not Now')]"))
    )

    notnow = driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()

    time.sleep(5)


def ig_scraper(driver, handle):
    driver.get(f'https://instagram.com/{handle}/')

    time.sleep(5)

    parser = Parser()
    parser.feed(driver.page_source)
    data = parser.Data

    try:
        influencer = get_influencer(data)
        return influencer, 'ok'
    except:
        if 'Page Not Found' in driver.title:
            try:
                if driver.find_element_by_css_selector('.error-container'):
                    return None, 'login'
            except:
                driver.get_screenshot_as_png()
        return None, 'not found'
