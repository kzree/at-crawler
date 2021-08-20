import requests
from bs4 import BeautifulSoup

def get_price(prices):
    """
    Checks both of the prices that are contained in the price container.
    The second price is always 0.00€ unless there is a sale.
    """
    price = ""
    for pr in prices:
        pr_text = pr.text.strip()
        if pr_text != "0.00€":
            price = pr_text
    return price

def get_item(card):
    """
    Gets card element and checks if it has h2 in it, only product cards
    have a h2 element in it.
    """
    title = card.find("h2")
    price = ""
    if title is not None:
        title = title.text.strip()
        prices = card.find_all("span", class_="price")
        price = get_price(prices)

    return (title, price)

def print_list(items):
    for item in items:
        print("{} - {}".format(item[1], item[0]))

URL = "https://arvutitark.ee/est/Otsing?q=3080&page=3"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
cards = soup.find_all("div", class_="card")

items = [] 

for card in cards:
    item = get_item(card)
    if item[0] is not None:
        items.append(item)

print_list(items)
