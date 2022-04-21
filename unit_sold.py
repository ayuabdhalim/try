import csv
import requests
from time import sleep
import mysql.connector
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome('D:/chromedriver')
driver.get('https://shopee.com.my/shocking_sale')
sleep(0.1)

# scroll the page
previous_height = 1500
step_scroll = 5
for i in range(1, step_scroll + 300):
    driver.execute_script('window.scrollTo(0, arguments[0]);', (previous_height / step_scroll) * i)
    sleep(0.2)

# get item link
url = []
progbar = []
card = driver.find_elements(By.XPATH, '//div[@class="flash-sale-item-card flash-sale-item-card--landing-page flash-sale-item-card--MY"]')
sleep(0.1)
for c in card:
    elink = c.find_element(By.XPATH, './/a[@class="flash-sale-item-card-link"]').get_attribute('href')
    eprogbar = c.find_element(By.XPATH, './/div[@class="flash-sale-item-card__lower-left"]/div[2]').get_attribute(
        'textContent')
    url.append(elink)
    progbar.append(eprogbar)
    print(elink)
    #print(eprogbar)

for i, prod_link in enumerate(url):

    if prod_link == 'https://shopee.com.my/web':
        pass

    else:
        unit_sold = progbar[i].replace('sold', '')
        print(unit_sold)

