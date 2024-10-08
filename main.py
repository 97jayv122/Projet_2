import requests

from bs4 import BeautifulSoup

url = "https://books.toscrape.com/catalogue/scott-pilgrims-precious-little-life-scott-pilgrim-1_987/index.html"

page = requests.get(url)

soup = BeautifulSoup(page.content, "html.parser")

print(soup.prettify())
