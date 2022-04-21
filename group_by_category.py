import mysql.connector

conn = mysql.connector.connect(host="localhost",
                               port="3306",
                               user="root",
                               password='1234',
                               database="shocking_sales_data")

cursor = conn.cursor()

query = "SELECT COUNT (model_id), category" \
        "FROM shocking_sales_raw" \
        "GROUP BY category"
cursor.execute(query)

"""
lists number of customers in each country
SELECT COUNT(CustomerID), Country
FROM Customers
GROUP BY Country;
list number of customers in each country,sorted high to low
SELECT COUNT(CustomerID), Country
FROM Customers
GROUP BY Country
ORDER BY COUNT(CustomerID) DESC;
"""