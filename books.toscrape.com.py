from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd

# Starting HTML session
s = HTMLSession()

# Defining a variable called books that will be used later on as a list of lists
books = []
# initiating a for loop to loop over the 50 pages we have 
for i in range(1, 51):
    url = f'https://books.toscrape.com/catalogue/page-{i}.html'
    r = s.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    ol = soup.find('ol', {'class': 'row'})
    articles = ol.find_all('article', {'class': 'product_pod'})

    for article in articles:
        img = article.find('img')
        title = img.attrs['alt']
        rate = article.find('p')
        rate = rate['class'][1]
        price_div = article.find('div', {'class': 'product_price'})
        price = price_div.find('p', {'class': 'price_color'})
        price = price.text
        price = float(price[2:])
        availability = price_div.find('p', {'class': 'instock availability'}).text.strip()
        books.append([title, price, rate, availability])

df = pd.DataFrame(books, columns=['Title', 'Price', 'Star Rating out of 5', 'Availability'])
df.to_csv('books.csv', index=False)