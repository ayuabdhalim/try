import csv
import requests
from time import sleep
import mysql.connector
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome('D:/chromedriver')
driver.get('https://shopee.com.my/shocking_sale')
sleep(0.1)

# scroll the page
previous_height = 1500
step_scroll = 5
for i in range(1, step_scroll + 300):
    driver.execute_script('window.scrollTo(0, arguments[0]);', (previous_height / step_scroll) * i)
    sleep(0.2)

# get sold out item link
url2 = []
soldoutcard = driver.find_elements(By.XPATH, '//div[@class="flash-sale-item-card flash-sale-item-card--landing-page flash-sale-item-card--MY flash-sale-item-card--sold-out"]')
sleep(0.1)
for sc in soldoutcard:
    selink = sc.find_element(By.XPATH, './/a[@class="flash-sale-item-card-link"]').get_attribute('href')
    url2.append(selink)
    print(selink)

# connect to mysql

conn = mysql.connector.connect(host="localhost",
                               port="3306",
                               user="root",
                               password='1234',
                               database="shocking_sales_db")

cursor = conn.cursor()

for i, prod_link2 in enumerate(url2):

    if prod_link2 == 'https://shopee.com.my/web':
        pass

    else:
        try:

            # get item_id and store_id from link
            pro_id = prod_link2.split('&promotionid')[0]
            productlink = pro_id.replace('/similar?from=flash_sale', '')
            ps_id = productlink.split('-i.')[1]
            item_id_l = ps_id.split('.')[1]
            shop_id_l = ps_id.split('.')[0]

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'}

            # request url and get data
            url = f'https://shopee.com.my/api/v4/item/get?itemid={item_id_l}&shopid={shop_id_l}'
            r = requests.get(url, headers=headers)
            sleep(1.0)
            json_r = r.json()
            data = json_r['data']

            url2 = f'https://shopee.com.my/api/v4/product/get_shop_info?shopid={shop_id_l}'
            r2 = requests.get(url2, headers=headers)
            sleep(1.0)
            json_r2 = r2.json()
            data2 = json_r2['data']

            # get models
            models = data['models']

            for i in range(len(models)):

                # get item_id
                item_id = data['itemid']

                # get model_id
                model_id = models[i]['modelid']

                # get shop_id
                shop_id = data['shopid']

                # get_price
                prices = models[i]['price']
                price = prices / 100000

                # get current_stock
                current_stock = models[i]['current_promotion_reserved_stock']

                # get allocated_stock
                price_stocks = models[i]['price_stocks']
                a_stocks = price_stocks[0]['allocated_stock']
                allocated_stock = 0 if a_stocks is None else a_stocks

                # get_unit_sold
                unit_sold = allocated_stock - current_stock

                # get item_name
                item_name = data['name']

                # get store_name
                store_name = data2['account']['username']

                # get category
                category = data['fe_categories'][0]['display_name']

                # get link
                link = productlink

                # get time create_at
                created_at = datetime.now().astimezone().replace(microsecond=0).isoformat()
                """
                print(created_at)
                print(item_id)
                print(model_id)
                print(shop_id)
                print(price)
                print(unit_sold)
                print(current_stock)
                print(allocated_stock)
                print(item_name)
                print(store_name)
                print(category)
                print(link)
                """
                # insert data
                query = "INSERT INTO shocking_sales_raw (created_at, item_id, model_id, shop_id, price, unit_sold, current_stock, allocated_stock, item_name, store_name, category, link)" \
                        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

                dbdata = (created_at, item_id, model_id, shop_id, price, unit_sold, current_stock, allocated_stock, item_name, store_name, category, link)

                cursor.execute(query,dbdata)
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
