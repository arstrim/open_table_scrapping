import argparse
import csv
import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
from restaurant_class import Restaurant
from restaurant_info import restaurant_info
from get_reviews import get_all_reviews
from build_db import build_db


LINK = 'https://www.opentable.com/m/best-restaurants-in-america-for-2017/'

def write_csv(name, links):
    """
    writes file reviews.csv (all revews from all restaurants) and 100restaurants.csv (general info of all restaurants).
    :param name: list of names of all restaurants
    :param links: list of links of all restaurants
    :return: None
    """
    if not os.path.exists("scrap_date.txt"):
        old_date='1900-01-01 00:00:00.000000'
        print('Writing reviews.csv')
        with open('reviews.csv', 'w') as f:
            f.write('Name,Place,Comment,Overall,Food,Service,Ambience,Date,Vip,User,N_rev\n')
        scrap_date = datetime.strptime(old_date.split('.')[0], "%Y-%m-%d %H:%M:%S")
    else:
        with open('scrap_date.txt', 'r') as f:
            text_date = f.readline().split('.')[0]
            scrap_date = datetime.strptime(text_date, "%Y-%m-%d %H:%M:%S")

    print('Appending scrape results')
    for n_res in range(len(links)):
        print('Writing', name[n_res], n_res, "of", len(links))
        try:
            (places, comments, overall, food, service, ambience, dates, vips, users, n_revs) = get_all_reviews(links[n_res], scrap_date)
        except:
            print("No reviews found for:", name[n_res])
        else:
            with open('reviews.csv', 'a') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                for i_rev in range(len(places)):
                    row = [name[n_res], places[i_rev], comments[i_rev], overall[i_rev], food[i_rev], service[i_rev], ambience[i_rev], dates[i_rev], vips[i_rev], users[i_rev], n_revs[i_rev]]
                    spamwriter.writerow(row)

    with open('scrap_date.txt', 'w') as f:
        f.write(str(datetime.now()))

    #Writing restaurants
    print('Writing 100restaurants.csv')
    # restaurant_info(links, name).to_csv('100restaurants.csv')



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
        write_csv(restaurants, rest_links)
    if args.db:
        # print('database')
        build_db()


if __name__ == '__main__':
    main()
