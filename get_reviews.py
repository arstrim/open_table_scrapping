import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import datetime as today


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
            date = datetime.today() + today.timedelta(int(date[6]))
        else:
            date = datetime.strptime(date[9:], '%B %d, %Y')
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


def get_all_reviews(rest_link, scrap_date):
    """
    Initializes the lists of features.
    get_comment_info() for every review.
    Returns a list per feature of all reviews.

    INPUT: rest_link: string of the restaurant link
    INPUT: scrap_date: datetime object, only returns comments after that
    OUTPUT: tuple of lists: (places, comments, overall, food, service, ambience, dates, vips, users, n_revs)
    """
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
    for last_page in pages: pass
    last_page = min(MAX_PAGES, int(last_page.text))

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
            (place, rating, comment, date, vip, user, n_rev) = get_comment_info(rev, scrap_date)
            if all(ele is None for ele in (place, rating, comment, date, vip, user, n_rev)) :
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

    return (places, comments, overall, food, service, ambience, dates, vips, users, n_revs)