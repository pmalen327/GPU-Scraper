#NewEgg search_term Scraper

from bs4 import BeautifulSoup
import requests
import re

#use the number associated with search_term/gpu - i.e. "3080" or "2060"

#input MUST be a numerical value
search_term = input("What are you looking for? ")


url = f"https://www.newegg.com/p/pl?d={search_term}&N=4131"

page = requests.get(url).text
doc = BeautifulSoup(page, "html.parser")

page_text = doc.find(class_="list-tool-pagination-text").strong

#counting how many pages of items we have and sending it to an int
pages = int(str(page_text).split("/")[-2].split(">")[-1][:-1])

items_found = {}

for page in range(1, pages+1):
    url = f"https://www.newegg.com/p/pl?d={search_term}&N=4131&page={page}"
    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser") 
    div = doc.find(class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")

    items = div.find_all(text=re.compile(search_term))

    for item in items:
        parent = item.parent
        link = None
        if parent.name !="a":
            continue
        
        #stripping the numerical value of the price
        link = parent['href']
        next_parent = item.find_parent(class_="item-container")

        #try-except because some tags had a type of "NoneType" which were not recognized
        try:
            price = next_parent.find(class_="price-current").find("strong").string
            items_found[item] = {"price": int(price.replace(",", "")), "link": link}
        except:
            pass

print(items_found)

#changing the dict to a list and sorting the items
sorted_items = sorted(items_found.items(), key=lambda x: x[1]['price'])

for item in sorted_items:
    print(item[0])
    print(f"${item[1]['price']}")
    print(item[1]['link'])
    print("------------------------")



