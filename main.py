import argparse
import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
from restaurant_info import restaurant_info
from get_reviews import get_all_reviews
from build_db import build_db

LINK = 'https://www.opentable.com/m/best-restaurants-in-america-for-2017/'


def write_csv(rest_names, rest_links):
    """
    writes file reviews.csv and 100restaurants.csv (all reviews from all restaurants).
    :param rest_names: list of names of all restaurants
    :param rest_links: list of links of all restaurants
    :return: None
    """
    if not os.path.exists("scrap_date.txt"):
        old_date = '1900-01-01 00:00:00.000000'
        scrap_date = datetime.strptime(old_date.split('.')[0], "%Y-%m-%d %H:%M:%S")
    else:
        with open('scrap_date.txt', 'r') as f:
            text_date = f.readline().split('.')[0]
            scrap_date = datetime.strptime(text_date, "%Y-%m-%d %H:%M:%S")

    with open('scrap_date.txt', 'w') as f:
        f.write(str(datetime.now()))

    # restaurant_info(rest_links, rest_names)
    get_all_reviews(rest_links, rest_names, scrap_date)


def get_links_and_names():
    """
    gets all links and restaurants names
    :return: tuple: list: rest_links (restaurants links), restaurants (restaurant names)
    """
    r = requests.get(LINK)
    soup = BeautifulSoup(r.content, 'html.parser')
    restaurants = []
    rest_links = []

    # Collecting restaurants names and urls
    for rest in soup.find_all('div', class_='restaurant tablet--flex'):
        restaurants.append(rest.find('h3').text)
        rest_links.append('https://www.opentable.com/' + rest.find('a', class_='rest-profile-link').get('href'))

    return rest_links, restaurants


def main():
    """
    Takes the arguments in the terminal and executes the function specified
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '-write', action='store_true')
    parser.add_argument('-db', '-database', action='store_true')
    args = parser.parse_args()

    if args.w:
        print("writting csv")
        (rest_links, restaurants) = get_links_and_names()
        # write csv files
        write_csv(restaurants, rest_links)

    if args.db:
        # print('database')
        build_db()


if __name__ == '__main__':
    main()
