import urllib.request
from bs4 import BeautifulSoup
import re

url = urllib.request.urlopen("https://www.royalchallengers.com/rcb-cricket-news")

soup = BeautifulSoup(url, "html.parser")

rows = soup.find_all('div', {'class':'views-row'})

for row in rows:
	print(row.text)

images = soup.find_all('img', {'src':re.compile('.svg')})
for image in images: 
    print(image['src']+'\n')
