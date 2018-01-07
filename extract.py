from requests import get
from bs4 import BeautifulSoup

product_number = int(input("Podaj kod produktu: \n"))
url = 'https://www.ceneo.pl/' + str(product_number)
response = get(url)
html_soup = BeautifulSoup(response.text, 'html.parser')