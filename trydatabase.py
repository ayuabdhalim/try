import mysql.connector

conn = mysql.connector.connect(host="localhost",
                               port="3306",
                               user="root",
                               password='1234',
                               database="shocking_sales_data")

cursor = conn.cursor()

cursor.execute("DESCRIBE shocking_sales_raw")

for x in cursor:
    print(x)