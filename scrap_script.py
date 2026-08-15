from bs4 import BeautifulSoup as bts # for scraping the data.
import requests as rq # to handle the requests to be sent.
import pandas as pd  # to clean and manipulate the data.
import numpy as np # for cleaning and manipulating the data.

# Function to extract the product title
def get_title(new_soup):
    try:
        title = new_soup.find("h1", class_=lambda x: x and "product" in x.lower()).text.strip()

    except AttributeError:
        title = ""	

    return title

# Function to extract the product price
def get_price(new_soup):
    try:
        price = new_soup.find("span", class_=lambda x: x and "price-item" in x.lower()).text.strip()

    except AttributeError:
        price = ""	

    return price

# Function to extract the review title
def get_review_title(new_soup):
    try:
        review_title = new_soup.find("b",class_=lambda x: x and "jdgm-rev__title" in x.lower()).text.strip()

    except AttributeError:
        review_title = ""	

    return review_title

# Function to extract the review body
def get_review_body(new_soup):
    try:
        review_body = new_soup.find("div",class_=lambda x: x and "jdgm-rev__body" in x.lower()).text.strip()

    except AttributeError:
        review_body = ""	

    return review_body


if __name__ == '__main__':

    # add your user agent 
    HEADERS = ({'UserAgent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Accept-Language' : 'en-US,en;q=0.5'})

    # The webpage URL
    URL = "https://www.regirlworld.com/collections/all"

    # HTTP Request
    webpage = rq.get(URL, headers=HEADERS)

    # Soup Object containing all data
    soup = bts(webpage.content, "html.parser")

    # Fetch links as List of Tag Objects
    links = soup.find_all("a", class_=lambda x: x and "product" in x.lower())

    # Store the links
    links_list = []

    # Loop for extracting links from Tag Objects
    for link in links:
            links_list.append(link.get('href'))

    d = {"title":[], "price":[], "review_title":[], "review_body":[] }
    
    # Loop for extracting product details from each link 
    for link in links_list:
        new_webpage = rq.get("https://www.regirlworld.com" + link, headers=HEADERS)

        new_soup = bts(new_webpage.content, "html.parser")

        # Function calls to display all necessary product information
        d['title'].append(get_title(new_soup))
        d['price'].append(get_price(new_soup))
        d['review_title'].append(get_review_title(new_soup))
        d['review_body'].append(get_review_body(new_soup))

    
    regirl_df = pd.DataFrame.from_dict(d)
    regirl_df['title'].replace('', np.nan, inplace=True)
    regirl_df = regirl_df.dropna(subset=['title'])
    regirl_df.to_csv("regirl_data.csv", header=True, index=False)

