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


	paragraph_nickname = soup.find("div", class_="reviewer-name-line")
	nicknames = paragraph_nickname.string
	print(nicknames)

	paragraph_recommend = soup.find("em", class_="product-recommended")
	recommend = paragraph_recommend.string
	print(recommend)



get_product_opinion(51499287)