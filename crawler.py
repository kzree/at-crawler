import config
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://arvutitark.ee/est/Otsing?q="

def is_price_in_bounds(price, min, max):
    """
    Checks if the item price is in given min and max bounds

    @param price: Price that is checked
    @param min: Given minimum price
    @param max: Given maximum price, can be None type

    @returns boolean
    """
    if (price < min):
        return False
    if (max is not None and price > max):
        return False
    return True

def get_price(prices, min, max):
    """
    Checks both of the prices that are contained in the price container.
    The second price is always 0.00€ unless there is a sale.

    @param prices: Prices in the item card, first price is regular price, second price is on sale price 
    @param min: Given minimum price
    @param max: Given maximum price, can be None type

    @returns price: If the value is in given bounds returns price, else returns None
    """
    price = ""
    for pr in prices:
        pr_text = pr.text.strip()
        if pr_text != "0.00€":
            price = pr_text
    return price if is_price_in_bounds(int(price.split(".")[0].replace(" ", "")), min, max) else None

def get_item(card, conf):
    """
    Gets card element and checks if it has h2 in it, only product cards
    have a h2 element in it.

    @param card: The item card element
    @param conf: User input params config

    @returns tuple: returns tuple with the item name and price
    """
    title = card.find("h2")
    price = ""
    if title is not None:
        title = title.text.strip()
        prices = card.find_all("span", class_="price")
        price = get_price(prices, conf.min, conf.max)

    return (title, price)

def get_last_page(pagination):
    """
    Gets the last page number from the pagination element

    @param pagination: Pagination element

    @returns int: Last page number
    """
    pagination_items = pagination.find_all("li")
    return int(pagination_items[len(pagination_items) - 2].text)

def get_page_data(item_list, page, conf):
    """
    Gets all the cards on the page and extracts the data from the cards

    @param item_list: List where parsed items are added to
    @param page: Parsed page data
    @param conf: User input params config
    """
    cards = page.find_all("div", class_="card")

    for card in cards:
        item = get_item(card, conf)
        if item[0] is not None and item[1] is not None:
            item_list.append(item)

def get_parsed_page(url):
    """
    Gets the parsed data from given url

    @param url: Url to be parsed

    @returns page: Parsed page data
    """
    page = requests.get(url)
    return BeautifulSoup(page.content, "html.parser")

def print_list(items):
    """
    Prints out the parsed items

    @param items: Item list containing all the parsed items
    """
    for item in items:
        item_data = "{} - {}".format(item[1], item[0])
        print((item_data[:97] + '...') if len(item_data) > 100 else item_data)

def main():
    """Main function"""
    conf = config.get_application_arguments()

    url = BASE_URL + conf.name

    parsed_page = get_parsed_page(url) 
    last_page = get_last_page(parsed_page.find("ul", {'class': 'pagination'}))

    items = []
    get_page_data(items, parsed_page, conf)

    if last_page > 1:
        for i in range(2, last_page + 1):
            url = url + "&page={}".format(i)
            get_page_data(items, get_parsed_page(url), conf)

    print_list(items)

main()
