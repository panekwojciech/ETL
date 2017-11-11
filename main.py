import re
import csv
import urllib.request
import ssl
from bs4 import BeautifulSoup


def get_product_opinion(product_number):
	context = ssl._create_unverified_context()
	fp = urllib.request.urlopen('https://www.ceneo.pl/' + str(product_number) + '#tab=reviews', context=context).read()
	mystr = fp.decode("utf8")
	soup = BeautifulSoup(mystr, 'html.parser')

	reviewer_name = soup.find_all("div", class_="reviewer-name-line")
	product_recommended = soup.find("em", class_="product-recommended")
	product_recommended_string = product_recommended.string
	product_not_recommended = soup.find("em", class_="product-not-recommended")
	product_not_recommended_string = product_not_recommended.string

	for paragraph_nickname in reviewer_name:
		if product_recommended_string == 'Polecam':
			nicknames = paragraph_nickname.string
			print(nicknames)
			print('Polecamm')
		elif product_not_recommended_string == 'Nie polecam':
			nicknames = paragraph_nickname.string
			print(nicknames)
			print('Nie polecam')


get_product_opinion(51499287)
