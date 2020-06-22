import argparse
import csv
import requests
from bs4 import BeautifulSoup
from restaurant_class import Restaurant
from restaurant_info import restaurant_info


LINK = 'https://www.opentable.com/m/best-restaurants-in-america-for-2017/'

def write_csv(name, links):
    """
    writes file reviews.csv (all revews from all restaurants) and 100restaurants.csv (general info of all restaurants).
    :param name: list of names of all restaurants
    :param links: list of links of all restaurants
    :return: None
    """
    print('Writing reviews.csv')
    with open('reviews.csv', 'w') as f:
        f.write('Name,Place,Comment,Overall,Food,Service,Ambience,Date,Vip')
    for n_res in range(len(links)):
        print('Writing', name[n_res], n_res, "of", len(links))
        temp_res = Restaurant(links[n_res])
        try:
            (places, comments, overall, food, service, ambience, dates, vips) = temp_res.get_all_reviews()
        except:
            print("No reviews found for:", name[n_res])
        else:
            with open('reviews.csv', 'a') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                for n_rev in range(len(places)):
                    row = [name[n_res], places[n_rev], comments[n_rev], overall[n_rev], food[n_rev], service[n_rev], ambience[n_rev], dates[n_rev], vips[n_rev]]
                    spamwriter.writerow(row)

    #Writing restaurants
    print('Writing 100restaurants.csv')
    restaurant_info(links, name).to_csv('100restaurants.csv')



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
    args = parser.parse_args()

    if args.w:
        print("writting csv")
        (rest_links, restaurants) = get_links_and_names()
        # rest_links = ['https://www.opentable.com/1770-house', 'https://www.opentable.com/arethusa-al-tavolo']
        # restaurants = ['1770 House', 'Arethusa al tavolo']
        write_csv(restaurants, rest_links)


if __name__ == '__main__':
    main()
