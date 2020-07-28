import argparse
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sys
import logging
import string
from scrape.get_reviews import get_all_reviews
from data_base.build_db import build_db
from scrape.restaurant_info import restaurant_info
from api.weather_api import weather_api

LINK = 'https://www.opentable.com/m/best-restaurants-in-america-for-2017/'


def write_csv(rest_names, rest_links, locations):
    """
    writes file reviews.csv and 100restaurants.csv (all reviews from all restaurants).
    :param rest_names: list of names of all restaurants
    :param rest_links: list of links of all restaurants
    :param locations: list of locations of all restaurants
    :return: None
    """
    scrap_file = os.path.join('.','data',"scrap_date.txt")
    if not os.path.exists(scrap_file):
        os.mkdir('data')
        old_date = '1900-01-01 00:00:00.000000'
        scrap_date = datetime.strptime(old_date.split('.')[0], "%Y-%m-%d %H:%M:%S")
    else:
        with open(scrap_file, 'r') as f:
            text_date = f.readline().split('.')[0]
            scrap_date = datetime.strptime(text_date, "%Y-%m-%d %H:%M:%S")

    try:
        with open(scrap_file, 'w') as f:
            f.write(str(datetime.now()))
    except FileNotFoundError:
        logging.error('File not found: ' + scrap_file)
        sys.exit()

    restaurant_info(rest_links, rest_names, locations)
    get_all_reviews(rest_links, rest_names, scrap_date)


def get_links_names_locations():
    """
    gets all links and restaurants names and their locations.
    :return: tuple: list: rest_links (restaurants links), restaurants (restaurant names), locations
    """
    r = requests.get(LINK)
    soup = BeautifulSoup(r.content, 'html.parser')
    restaurants = []
    rest_links = []
    locations = []

    # Collecting restaurants names and urls
    for rest in soup.find_all('div', class_='restaurant tablet--flex'):
        dirty_name = rest.find('h3').text
        name = ''.join([i if i in string.printable else '' for i in dirty_name])
        restaurants.append(name)
        rest_links.append('https://www.opentable.com/' + rest.find('a', class_='rest-profile-link').get('href'))
        try:
            locations.append(rest.find('h4').text.split('\n')[0].rstrip())
        except AttributeError:
            locations.append(None)

    return rest_links, restaurants, locations


def main():
    """
    Takes the arguments in the terminal and executes the function specified
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '-write', action='store_true', help='write csv')
    parser.add_argument('-db', '-database',  type=str, nargs = 2, metavar=('user', 'password'), help='build/update database')
    parser.add_argument('-api', '-weather_api', type=str, nargs=2, metavar=('user', 'password'),
                        help='build/update weather information table')
    args = parser.parse_args()

    if args.w:
        logging.info("writting csv")
        (rest_links, restaurants, locations) = get_links_names_locations()
        # write csv files
        write_csv(restaurants, rest_links, locations)

    if args.db:
        logging.info('building/updating database')
        build_db(args.db[0], args.db[1])
    if args.api:
        logging.info('building/updating weathers information table')
        weather_api(args.api[0], args.api[1])


if __name__ == '__main__':
    main()
