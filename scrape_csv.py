import csv
import mysql.connector

conn = mysql.connector.connect(host="localhost",
                               port="3306",
                               user="root",
                               password='1234',
                               database="shocking_sales_data")

cursor = conn.cursor()

query = "SELECT * FROM shocking_sales_raw"
cursor.execute(query)
with open("output.csv","w", encoding="utf-8", newline="") as outfile:
    writer = csv.writer(outfile, quoting=csv.QUOTE_NONNUMERIC)
    writer.writerow(col[0] for col in cursor.description)
    for row in cursor:
        writer.writerow(row)