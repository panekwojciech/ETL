from requests import get
from bs4 import BeautifulSoup
from extract import html_soup, product_number


# def transform(html_soup):


rodzaj_urzadzenia = html_soup(itemprop="url")[2].text
marka_model = html_soup.find(itemprop="name").text
ocena = html_soup(itemprop="ratingValue")[0].text.strip().split()
ocena1 = ocena[0]

print(marka_model)
print(rodzaj_urzadzenia)
print(ocena1)

if html_soup.find(itemprop="reviewCount") is not None:
	ilosc_opinii = html_soup.find(itemprop="reviewCount").text
	ilosc_opinii = int(ilosc_opinii)

	for x in range(1, ilosc_opinii // 10 + 2):
		url = 'https://www.ceneo.pl/' + str(product_number) + '/opinie-' + str(x)
		response = get(url)
		html_soup = BeautifulSoup(response.text, 'html.parser')

		for paragraph in html_soup.find_all("li", class_="review-box js_product-review"):
			nickname = paragraph.find("div", class_="reviewer-name-line").text
			product_review = paragraph.find("p", class_="product-review-body").text
			score_count = paragraph.find("span", class_="review-score-count").text
			pros = ''
			cons = ''
			if paragraph.find("span", class_="pros"):
				pros = paragraph.findNext("ul").text
			elif paragraph.find("span", class_="cons"):
				cons = paragraph.findNext("ul").text
			date = paragraph.find("span", class_="review-time").text
			vote_yes = paragraph.find("button", class_="vote-yes js_product-review-vote js_vote-yes").text
			vote_no = paragraph.find("button", class_="vote-no js_product-review-vote js_vote-no").text

			print("============")
			print("Użytkownik: {}".format(nickname))
			print("Opinia: {}".format(product_review))
			print("Ocena: {}".format(score_count))
			print("Zalety: {}".format(pros))
			print("Wady: {}".format(cons))
			print("Kiedy wystawiono opinie: {}".format(date))
			print("Ilosc lapek w gore: {}".format(vote_yes))
			print("Ilosc lapek w dol: {}".format(vote_no))

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

else:
	ilosc_opinii = 0

# transform(html_soup)