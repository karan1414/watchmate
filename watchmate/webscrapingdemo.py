# First step in writing scraping script using beautiful soup is to install the package using 
# pip install beautifulsoup4
# pip install requests

import csv

import requests
from bs4 import BeautifulSoup

# we save the link to scrape in a variable
base_url = "https://books.toscrape.com/"
home_url = "https://books.toscrape.com/index.html"

csv_file = open('book_records.csv', 'w')

csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Sr. No.', 'Book Title', 'Book Price', 'Book Availability'])

first_resp = requests.get(home_url).text

# if first_resp.status_code != 200:
# if not first_resp:

soup = BeautifulSoup(first_resp, 'html.parser')

# if not soup:
#     print("Soup not found for base webpage")
# print(soup.find('ol', attrs={"class": "row"}))
# print(s)
ol_soup = soup.find('ol', attrs={"class": "row"})

li_soup = ol_soup.find_all('article', attrs={"class": "product_pod"})
count = 0
for li in li_soup:
    count += 1
    pictures_link_suffix = li.find('img')['src'] if li.find('img') and li.find('img')['src'] else None
    pictures_link = base_url + pictures_link_suffix
    
    # book heading
    heading = li.find('h3') if li.find('h3') else None
    book_title = heading.find('a')['title'] if heading else None

    # product price
    book_price = li.find('p', attrs={"class": "price_color"}).text.strip() if li.find('p', attrs={"class": "price_color"}) and li.find('p', attrs={"class": "price_color"}).text else ""

    # book availability
    book_availability = True if li.find('p', attrs={"class": "instock availability"}) and li.find('p', attrs={"class": "instock availability"}).text and li.find('p', attrs={"class": "instock availability"}).text.strip() == "In stock" else False

    csv_writer.writerow([count, book_title, book_price, book_availability])

    print("----------------------------------")
    print("picture link ===>", pictures_link)
    print("book title ===>", book_title)
    print("book price ===>", book_price)
    print("book availability ===>", book_availability)
    # print(li)
    print("----------------------------------")


# Web Scraping roles and job opportunity