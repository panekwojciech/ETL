import csv
import urllib.request

url = 'http://winterolympicsmedals.com/medals.csv'
response = urllib.request.urlopen(url)
cr = csv.reader(response)

for row in cr:
	print(row)