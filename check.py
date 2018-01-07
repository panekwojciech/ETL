from requests import get
from bs4 import BeautifulSoup
import pymysql
import pandas as pd

# 44316403
#Tablice przydatne do statystyk oraz do zapisu do pliku csv
numer_produktu_d = []
rodzaj_urzadzenia_d = []
marka_model_d = []
uzytkownik_d = []
opinia_d = []
ocena_d = []
zalety_d = []
wady_d = []
data_d = []
przydatna_d = []
nieprzydatna_d = []

#Numer produktu
product_number = int(input("Podaj kod produktu: \n"))
numer_produktu_d.append(product_number)

#Połączenie z bazą danych
conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='root', passwd='ETL.123', db='mysql',
					   charset='utf8mb4')
cur = conn.cursor()
cur.execute("USE etl")

#Funkcja zapisująca dane o produkcie do bazy danych
def store(rodzaj_urzadzenia, marka_model, ilosc_opinii, product_number):
	cur.execute("SELECT numer_produktu FROM info WHERE numer_produktu=\"%s\"", (product_number))
	if cur.rowcount == 0:
		cur.execute(
			"INSERT INTO info (rodzaj_urzadzenia, marka_model, ilosc_opinii, numer_produktu) VALUES (\"%s\", \"%s\", \"%s\",\"%s\")",
			(rodzaj_urzadzenia, marka_model, ilosc_opinii, product_number))
		cur.connection.commit()

#Funkcja wykonująca proces ETL
def getProduct(product_number):
	#Pobieramy URL z naszym produktem
	url = 'https://www.ceneo.pl/' + str(product_number)
	response = get(url)
	#Parsujemy przy uzyciu bibliotek BFS
	html_soup = BeautifulSoup(response.text, 'html.parser')
	#Pobieramy rodzaj urzadzenia oraz dodajemy do naszej tablicy
	rodzaj_urzadzenia = html_soup(itemprop="url")[2].text
	rodzaj_urzadzenia_d.append(rodzaj_urzadzenia)
	#Pobieramy marke/model oraz dodajemy do naszej tablicy
	marka_model = html_soup.find(itemprop="name").text
	marka_model_d.append(marka_model)
	#Inicjujemy zmienna ocena, która będzie nam potrzebna w następnym etapie
	ocena1 = ''
	try:
		ocena = html_soup(itemprop="ratingValue")[0].text.strip().split()
		ocena1 = ocena[0]
		ocena_d.append(ocena1)
	except IndexError:
		pass

	#Wyświetlamy na ekranie: Markę, Kategorię, Ocenę
	print("Marka/Model: {}".format(marka_model))
	print("Kategoria: {}".format(rodzaj_urzadzenia))
	print("Ocena: {}".format(ocena1))

	#Jeżeli produkt posiada opinię to wykonujemy następujący blok kodu:
	if html_soup.find(itemprop="reviewCount") is not None:
		ilosc_opinii = html_soup.find(itemprop="reviewCount").text
		ilosc_opinii = int(ilosc_opinii)

		#Pobieramy poszczególne dane z poszczególnej opinii
		for x in range(1, ilosc_opinii // 10 + 2):
			url = 'https://www.ceneo.pl/' + str(product_number) + '/opinie-' + str(x)
			response = get(url)
			html_soup = BeautifulSoup(response.text, 'html.parser')

			#Dla każdej opinii z osobna pobieramy dane
			for paragraph in html_soup.find_all("li", class_="review-box js_product-review"):
				nickname = paragraph.find("div", class_="reviewer-name-line").text
				uzytkownik_d.append(nickname)
				product_review = paragraph.find("p", class_="product-review-body").text
				opinia_d.append(product_review)
				score_count = paragraph.find("span", class_="review-score-count").text
				ocena_d.append(score_count)
				pros = ''
				cons = ''
				if paragraph.find("span", class_="pros"):
					pros = paragraph.findNext("ul").text
					zalety_d.append(pros)
				elif paragraph.find("span", class_="cons"):
					cons = paragraph.findNext("ul").text
					wady_d.append(wady_d)
				date = paragraph.find("span", class_="review-time").text
				data_d.append(date)
				vote_yes = paragraph.find("button", class_="vote-yes js_product-review-vote js_vote-yes").text
				przydatna_d.append(vote_yes)
				vote_no = paragraph.find("button", class_="vote-no js_product-review-vote js_vote-no").text
				nieprzydatna_d.append(vote_no)

				#Wyświetalmy wszystko na ekranie
				print("=================================")
				print("Użytkownik: {}".format(nickname))
				print("Opinia: {}".format(product_review))
				print("Ocena: {}".format(score_count))
				print("Zalety: {}".format(pros))
				print("Wady: {}".format(cons))
				print("Kiedy wystawiono opinie: {}".format(date))
				print("Ilosc lapek w gore: {}".format(vote_yes))
				print("Ilosc lapek w dol: {}".format(vote_no))

				#Potrzebne dane umieszczamy w bazie danych
				cur.execute(
					"INSERT IGNORE INTO opinie (numer_produktu, opinia, uzytkownik, ocena) VALUES (\"%s\",\"%s\",\"%s\",\"%s\")",
					(product_number, product_review, nickname, score_count))
				cur.connection.commit()

			#Sprawdzamy czy opinia posiada rekomendacje użytkownika
			if paragraph.find("div", class_="reviewer-recommendation"):
				if paragraph.find("em", class_="product-recommended"):
					# print("Polecam")
					product_recomm = paragraph.find("em", class_="product-recommended").get_text()
					print(product_recomm)
				elif paragraph.find("em", class_="product-not-recommended"):
					# print("Nie polecam")
					product_not_recomm = paragraph.find("em", class_="product-not-recommended")
					product_not_recomm_string = product_not_recomm.string
					print(product_not_recomm_string)
				else:
					print("Brak rekomendacji")

	#Jeżeli nie ma opinii - nie ma pracy ;)
	else:
		ilosc_opinii = 0
		print("Ilosc opinii: {}".format(ilosc_opinii))

	#Umieszczamy dane o produkcie w bazie danych
	store(rodzaj_urzadzenia, marka_model, ilosc_opinii, product_number)

	#Zamykamy połączenie z bazą danych
	cur.close()
	conn.close()

	#To wyrażenie regularne "wyrzuca" nam z tablicy 'uzytkownik_d' "smieci", tzn '\r\n'
	uzytkownik_d_r = [s.replace('\r\n', '') for s in uzytkownik_d]

	#Zapisujemy nasze dane z tablic do zmiennej 'd' przy użyciu 'Dictionary'
	d = dict({'Uzytkownik:': uzytkownik_d_r, 'Opinia:': opinia_d, 'Ocena:': ocena_d})

	test_df1 = pd.DataFrame({'Uzytkownik': uzytkownik_d_r})
	test_df2 = pd.DataFrame({'Opinia': opinia_d})
	test_df3 = pd.DataFrame({'Ocena': ocena_d})

	#Dzieki projektowi Pandas mozemy wyświetlic statystyki oraz zapisac do pliku CSV
	df = pd.DataFrame.from_dict(d, orient='index')
	print(df)
	print(test_df1.info(),'\n',test_df2.info(),'\n',test_df3.info())
	df.to_csv('trzecia.csv')

	#print(len(opinia_d), len(ocena_d))
	#print(test_df1.info(),'\n',test_df2.info(),'\n',test_df3.info())
	#print(test_df.info())

getProduct(product_number)
