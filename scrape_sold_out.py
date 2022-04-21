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

# for sold out item
url2 = []
progbar2 = []
soldoutcard = driver.find_elements(By.XPATH, '//div[@class="flash-sale-item-card flash-sale-item-card--landing-page flash-sale-item-card--MY flash-sale-item-card--sold-out"]')
for sc in soldoutcard:
    selink = sc.find_element(By.XPATH, './/a[@class="flash-sale-item-card-link"]').get_attribute('href')
    seprogbar = sc.find_element_by_xpath('.//div[@class="flash-sale-item-card__lower-left"]/div[2]').get_attribute('textContent')
    url2.append(selink)
    progbar2.append(seprogbar)
    print(selink)

for i, prod_link2 in enumerate(url2):
    if prod_link2 == 'https://shopee.com.my/web':
        pass
    else:
        pro_id =  prod_link2.split('&promotionid')[0]
        productlink = pro_id.replace('/similar?from=flash_sale', '')
        print(productlink)
        print(pro_id)
        driver.get(productlink)
        sleep(10.0)

# get item_id and store_id from link
#        ps_id = productlink.split('-i.')[1]
#        item_id = ps_id.split('.')[1]
#        store_id = ps_id.split('.')[0]