import re
import csv
import urllib.request
import ssl
from bs4 import BeautifulSoup


# def __init__(self, product_number):
# 	self.product_number = str('')
# 	self.product_opinion = ''



def get_product_opinion(product_number):
	context = ssl._create_unverified_context()
	fp = urllib.request.urlopen('https://www.ceneo.pl/' + str(product_number) + '#tab=reviews', context=context).read()
	mystr = fp.decode("utf8")
	soup = BeautifulSoup(mystr, 'html.parser')

	for paragraph_nickname in soup.find_all("div", class_="reviewer-name-line"):
		nicknames = paragraph_nickname.string
		print(nicknames)
		for	paragraph_recommend in soup.find_all("em", class_="product-recommended"):
			recommend = paragraph_recommend.string
			print(recommend)
		for	paragraph_not_recommend in soup.find_all("em", class_="product-not-recommended"):
			not_recommend = paragraph_not_recommend.string
			print(not_recommend)



get_product_opinion(51499287)