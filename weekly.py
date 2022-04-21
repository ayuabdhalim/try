import mysql.connector

conn = mysql.connector.connect(host="localhost",
                               port="3306",
                               user="root",
                               password='1234',
                               database="shocking_sales_data")

cursor = conn.cursor()
"""
SELECT
  EXTRACT(

SELECT
  EXTRACT(year FROM transaction_date) AS year,
  SUM(money) AS money_earned
FROM data
GROUP BY EXTRACT(year FROM transaction_date);
"""