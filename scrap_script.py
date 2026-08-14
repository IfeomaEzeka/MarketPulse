from bs4 import BeautifulSoup as bts # for scraping the data 
import requests as rq # to handle the requests to be sent
import pandas as pd  # to clean and manipulate the data

URL = "https://www.regirlworld.com/collections/all"
#Headers 
Header = ({'UserAgent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Accept-Language' : 'en-US,en;q=0.5'})

webpage = rq.get(URL,headers= Header)

#print(webpage)

#print(type(webpage.content))

soup = bts(webpage.content, "html.parser")
#print(soup)

links = soup.find_all("a", class_=lambda x: x and "product" in x.lower())
#print(links)

product =links[0].get("href")
product_link = "https://www.regirlworld.com" + product
#print(product)
#print(product_link)

new_webpage = rq.get(product_link, headers= Header)
print(new_webpage)

new_soup = bts(new_webpage.content, "html.parser")
#print(new_soup)

result = new_soup.find("h1", class_=lambda x: x and "product" in x.lower()).text.strip()
print(result)

price = new_soup.find("span", class_=lambda x: x and "price-item" in x.lower()).text.strip()
print(price)
review = new_soup.find("b",class_=lambda x: x and "jdgm-rev__title" in x.lower()).text.strip()
review_body = new_soup.find("div",class_=lambda x: x and "jdgm-rev__body" in x.lower()).text.strip()

print(review)
print(review_body)

