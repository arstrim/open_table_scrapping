import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import datetime as today
import pandas as pd

MAX_PAGES = 2


def get_date(review, scrap_date):
    """
    Scraps the date of the review and checks if it is previous from scrap_date
    :param review: review to scrape
    :param scrap_date: checks if the date of the review is before that
    :return: date of review or -1 if the date is older than scrap_date
    """
    date = review.find('span', class_='oc-reviews-47b8de40').text
    try:
        if date[-1] == 'o':
            if type(date[6]) == int:
                date = datetime.today() + today.timedelta(int(date[6]))
            else:
                date = datetime.today() + today.timedelta(1)
        elif date[0] == 'D':
            date = datetime.strptime(date[9:], '%B %d, %Y')
        else:
            date = datetime.strptime(date[12:], '%B %d, %Y')
    except:
        date = None
    else:
        if date < scrap_date:
            # print('\tDate:', date, 'already scraped')
            return -1
        # else:
        #     print('  New entry:', date)

    return date


def get_comment_info(review, scrap_date):
    """
    Returns place, rating, comment, date of a review.
    Note: only place, returns None
    INPUT: review: BeautifulSoup object of the review
    INPUT: scrap_date: datetime object, only returns comments after that
    OUTPUT: tuple of strings: (place, rating, comment, date, vip, user, n_rev)
    Note: if date is older than scrap_date it returns tupple of Nones
    """
    date = get_date(review, scrap_date)
    if date == -1:
        return None, None, None, None, None, None, None

    try:
        place = review.find('span', class_='oc-reviews-9fda5cd0').text
    except:
        place = None
    try:
        rating = review.find('div', class_='oc-reviews-0d90fee7').text
    except:
        rating = None
    try:
        comment = review.find('p').text
    except:
        comment = None
    try:
        vip = True if review.find('span', class_='oc-reviews-42b9159d').text == 'vip' else False
    except:
        vip = False

    user = review.find('div', class_='oc-reviews-954a6007').find_all('span')[1].text
    n_rev = re.search('[0-9]*', review.find('div', class_='oc-reviews-ef72a012').text).group(0)

    return place, rating, comment, date, vip, user, n_rev


def get_reviews(rest_link, rest_name, scrap_date):
    """
    Initializes the lists of features.
    get_comment_info() for every review.
    Returns a list per feature of all reviews.
    INPUT: rest_link: string of the restaurant link
    INPUT: scrap_date: datetime object, only returns comments after that
    OUTPUT: tuple of lists: (places, comments, overall, food, service, ambience, dates, vips, users, n_revs)
    """
    names = []
    places = []
    comments = []
    dates = []
    overall = []
    food = []
    service = []
    ambience = []
    vips = []
    users = []
    n_revs = []

    r = requests.get(rest_link)
    soup_rest = BeautifulSoup(r.content, 'html.parser')
    # Geting last_page
    pages = soup_rest.find_all('button', class_='reviewUpdateParameter oc-reviews-b0c77e5f')
    last_page = len(pages) - 1
    last_page = min(MAX_PAGES, last_page)

    # looping through pages 1 to last_page (min(MAX_PAGES, last_page))
    for i in range(1, last_page):
        if i != 1:  # Because it was already read to get the first page
            rest_link = rest_link
            rest_link += '?page=' + str(i)
            r = requests.get(rest_link)
            soup_rest = BeautifulSoup(r.content, 'html.parser')

        # Finds all the reviews
        reviews = soup_rest.find_all('div', class_='oc-reviews-5a88ccc3')
        for rev in reviews:
            names.append(rest_name)
            (place, rating, comment, date, vip, user, n_rev) = get_comment_info(rev, scrap_date)
            if all(ele is None for ele in (place, rating, comment, date, vip, user, n_rev)):
                continue
            # Stores the variables in lists
            else:
                places.append(place)
                comments.append(comment)
                try:
                    overall.append(int(re.split(r'(\d)', rating)[1]))
                except:
                    overall.append(None)
                try:
                    food.append(int(re.split(r'(\d)', rating)[3]))
                except:
                    food.append(None)
                try:
                    service.append(int(re.split(r'(\d)', rating)[5]))
                except:
                    service.append(None)
                try:
                    ambience.append(int(re.split(r'(\d)', rating)[7]))
                except:
                    ambience.append(None)

                dates.append(date)

                vips.append(vip)
                users.append(user)
                n_revs.append(int(n_rev))

    return names, places, comments, overall, food, service, ambience, dates, vips, users, n_revs


def get_all_reviews(rest_links, restaurants, scrap_date):
    all_names = []
    all_places = []
    all_comments = []
    all_dates = []
    all_overall = []
    all_food = []
    all_service = []
    all_ambience = []
    all_vips = []
    all_users = []
    all_n_revs = []
    for i in range(len(rest_links)):
        print('Now scraping reviews of restaurant {i} out of {total}'.format(i=i+1, total=len(rest_links)))
        (names, places, comments, overall, food, service, ambience, dates, vips, users, n_revs) = \
            get_reviews(rest_links[i], restaurants[i], scrap_date)
        all_names += names
        all_comments += comments
        all_places += places
        all_food += food
        all_overall += overall
        all_service += service
        all_ambience += ambience
        all_dates += dates
        all_vips += vips
        all_users += users
        all_n_revs += n_revs

    # Creating data base
    d = {'Name': all_names, 'Place': all_places, 'Comments': all_comments, 'Overall rating': all_overall,
         'Food rating': all_food, 'Service rating': all_service, 'Ambience rating': all_ambience,
         'Dates': all_dates, "VIP": all_vips, 'Users': all_users, 'No. of reviews': all_n_revs}

    df = pd.DataFrame(data=d)
    df.to_csv("reviews.csv")