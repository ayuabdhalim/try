import mysql.connector

conn = mysql.connector.connect(host="localhost",
                               port="3306",
                               user="root",
                               password='1234',
                               database="shocking_sales_data")

cursor = conn.cursor()

sql = "SELECT * FROM shocking_sales_raw" \
      "WHERE date_iso BETWEEN DATE_SUB(NOW(),INTERVAL 1 WEEK) and NOW()"

cursor.execute(sql)

data = cursor.fetchall()

for i in data:
    print(i)


"""
sql = "SELECT model_id, DATE(date_iso) FROM shocking_sales_raw"

data = cursor.fetchall()

for i in data:
    print(i)
    
sql = "SELECT model_id,date_iso FROM shocking_sales_raw" \
      "WHERE date_iso = CONVERT(nvarchar(10),GETDATE(),101);"
sql = "SELECT model_id,date_iso FROM shocking_sales_raw" \
      "WHERE date_iso BETWEEN DATEADD(d,-7," \
      "CONVERT(nvarchar(10),GETDATE(),101))" \
      "AND CONVERT(nvarchar(10),GETDATE(),101)"

Group Data by Week
SELECT
  DATEPART(week, RegistrationDate) AS Week,
  COUNT(CustomerID) AS Registrations
FROM Customers
WHERE '20180101' <= RegistrationDate
  AND RegistrationDate < '20190101'
GROUP BY DATEPART(week, RegistrationDate)
ORDER BY DATEPART(week, RegistrationDate);
***************************************************************************
Product Name|First Week|Second Week|Third Week
Select
ProductName,
WeekNumber,
sum(sale)
from
(
    SELECT
    ProductName,
    DATEDIFF(week, '2011-05-30', date) AS WeekNumber,
    sale
    FROM table
)
GROUP BY
ProductName,
WeekNumber
"""