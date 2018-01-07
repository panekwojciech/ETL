from requests import get
from bs4 import BeautifulSoup
import pymysql

product_number = int(input("Podaj kod produktu: \n"))
# 44316403
conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='root', passwd='ETL.123', db='mysql')
cur = conn.cursor()
cur.execute("USE etl")


def delete(product_number):
	cur.execute("SELECT numer_produktu FROM info WHERE numer_produktu=\"%s\"", (product_number))
	if cur.rowcount is not 0:
		cur.execute("DELETE FROM opinie WHERE numer_produktu=\"%s\"", (product_number))
		cur.execute("DELETE FROM info WHERE numer_produktu=\"%s\"", (product_number))
		cur.connection.commit()
		print("Usunieto z bazy dancyh produkt numer: {}".format(product_number))
	else:
		print("Brak produktu o numerze {} w bazie danych!".format(product_number))

	cur.close()
	conn.close()

delete(product_number)

def select(product_number):
	cur.execute("SELECT opinia FROM opinie WHERE numer_produktu=\"%s\"", (product_number))
	print(cur.fetchall())

	cur.close()
	conn.close()


#select(product_number)