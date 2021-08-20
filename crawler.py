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

def get_last_page(pagination):
    """Gets the last page number from the pagination element"""
    pagination_items = pagination.find_all("li")
    return int(pagination_items[len(pagination_items) - 2].text)

def get_page_data(item_list, page):
    """Gets all the cards on the page and extracts the data from the cards"""
    cards = page.find_all("div", class_="card")

    for card in cards:
        item = get_item(card)
        if item[0] is not None:
            item_list.append(item)

def get_parsed_page(url):
    page = requests.get(url)
    return BeautifulSoup(page.content, "html.parser")

def print_list(items):
    for item in items:
        item_data = "{} - {}".format(item[1], item[0])
        print((item_data[:97] + '...') if len(item_data) > 100 else item_data)

def main():
    """Main function"""
    base_url = "https://arvutitark.ee/est/Otsing?q=3080"

    parsed_page = get_parsed_page(base_url) 
    last_page = get_last_page(parsed_page.find("ul", {'class': 'pagination'}))

    items = []
    get_page_data(items, parsed_page)

    if last_page > 1:
        for i in range(2, last_page + 1):
            url = base_url + "&page={}".format(i)
            get_page_data(items, get_parsed_page(url))

    print_list(items)

main()
