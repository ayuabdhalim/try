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

# connect to mysql

conn = mysql.connector.connect(host="localhost",
                               port="3306",
                               user="root",
                               password='1234',
                               database="shocking_sales_data")

cursor = conn.cursor()


# get item details

for i, prod_link in enumerate(url):
    driver.get(prod_link)
    sleep(1.0)

    if prod_link == 'https://shopee.com.my/web':
        pass

    else:
        try:
            # get category
            cate = WebDriverWait(driver, 20).until(ec.presence_of_all_elements_located(
                (By.CLASS_NAME, '_2572CL')))
            categor = [c.get_attribute("textContent") for c in cate]
            category = categor[1]

            # get item_id and store_id from link
            ps_id = prod_link.split('-i.')[1]
            item_id = ps_id.split('.')[1]
            store_id = ps_id.split('.')[0]

            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'}

            # request url and get data
            url = f'https://shopee.com.my/api/v4/item/get?itemid={item_id}&shopid={store_id}'
            r = requests.get(url, headers=headers)
            sleep(0.1)
            json_r = r.json()
            data = json_r['data']

            url2 = f'https://shopee.com.my/api/v4/product/get_shop_info?shopid={store_id}'
            r2 = requests.get(url2, headers=headers)
            sleep(0.1)
            json_r2 = r2.json()
            data2 = json_r2['data']

            # get item_name
            item_name = data['name']
            #get store_name
            store_name = data2['account']['username']

            # get unit_sold
            unit_sold = progbar[i].replace('sold', '')

            # get stock
            stock = data['stock']

            # get price
            #price = data['price']
            price = driver.find_element(By.CLASS_NAME, "_2v0Hgx").get_attribute("textContent")

            # get date_iso
            created_at = datetime.now().astimezone().replace(microsecond=0).isoformat()

            # get model_id
            model_id = f'{item_id}{store_id}{unit_sold}{price[2:]}'

            # insert data
            sql = "INSERT INTO shocking_sales_raw (created_at, item_id, model_id, category, item_name, store_id, store_name,"\
                    "unit_sold, stock, price, link) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

            dbdata = (created_at, item_id, model_id, category, item_name, store_id, store_name, unit_sold, stock, price[2:], prod_link)

            cursor.execute(sql, dbdata)
            conn.commit()

        except requests.exceptions.ConnectionError:
            print("connection refused")

# export to csv

query = "SELECT * FROM shocking_sales_raw"
cursor.execute(query)
with open("output.csv","w", encoding="utf-8", newline="") as outfile:
    writer = csv.writer(outfile, quoting=csv.QUOTE_NONNUMERIC)
    writer.writerow(col[0] for col in cursor.description)
    for row in cursor:
        writer.writerow(row)
conn.close()