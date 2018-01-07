from requests import get
from bs4 import BeautifulSoup
import pymysql
from transform import rodzaj_urzadzenia, marka_model, ilosc_opinii, product_number

# 44316403
conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='root', passwd='ETL.123', db='mysql')
cur = conn.cursor()
cur.execute("USE etl")

def store(rodzaj_urzadzenia, marka_model, ilosc_opinii, product_number):
	cur.execute("SELECT numer_produktu FROM info WHERE numer_produktu=\"%s\"", (product_number))
	if cur.rowcount == 0:
		cur.execute(
			"INSERT INTO info (rodzaj_urzadzenia, marka_model, ilosc_opinii, numer_produktu) VALUES (\"%s\", \"%s\", \"%s\",\"%s\")",
			(rodzaj_urzadzenia, marka_model, ilosc_opinii, product_number))
		cur.connection.commit()

store(rodzaj_urzadzenia, marka_model, ilosc_opinii, product_number)

cur.close()
conn.close()
