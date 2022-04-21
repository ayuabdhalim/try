from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
from time import sleep
import lalalalala.connector

driver = webdriver.Chrome('D:/chromedriver')
driver.get('https://shopee.com.my/shocking_sale')
sleep(0.1)

# to scroll the page
previous_height = 1500
step_scroll = 5
for i in range(1, step_scroll + 300):
    driver.execute_script('window.scrollTo(0, arguments[0]);', (previous_height / step_scroll) * i)
    sleep(0.2)

# to get progress bar and url item listed
url = []
progbar = []
card = driver.find_elements(By.XPATH, '//div[@class="flash-sale-item-card flash-sale-item-card--landing-page flash-sale-item-card--MY"]')
for c in card:
    elink = c.find_element(By.XPATH, './/a[@class="flash-sale-item-card-link"]').get_attribute('href')
    eprogbar = c.find_element(By.XPATH, './/div[@class="flash-sale-item-card__lower-left"]/div[2]').get_attribute(
        'textContent')
    url.append(elink)
    progbar.append(eprogbar)
    print(elink)



for i, prod_link in enumerate(url):
    driver.get(prod_link)
    sleep(0.5)

    if prod_link == 'https://shopee.com.my/web':
        pass

    else:
        # to get category
        cate = WebDriverWait(driver, 10).until(ec.presence_of_all_elements_located(
            (By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/div/div[2]/div/div[1]/span[1]')))
        category = [c.get_attribute("textContent") for c in cate]

        for b in category:
            print(b)

        ps_id = prod_link.split('-i.')[1]
        item_id = ps_id.split('.')[1]
        item_name = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/div/div[2]/div/div[2]/div[3]/div/div[1]/span').get_attribute(
            "textContent")
        store_id = ps_id.split('.')[0]
        store_name = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/div/div[2]/div/div[3]/div[1]/div[1]/div/div[1]'))).get_attribute("textContent")
        #store_name = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/div/div[2]/div/div[3]/div[1]/div[1]/div/div[1]').get_attribute("textContent")
        price = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/div/div[2]/div/div[2]/div[3]/div/div[3]/div[2]/div/div/div/div[2]/div[1]').get_attribute("textContent")
        print(item_id)
        print(item_name)
        print(store_id)
        print(store_name)
        print(price)




