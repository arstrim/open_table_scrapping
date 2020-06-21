import re 
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import datetime as today
import pandas as pd

MAX_PAGES = 2

# Scraping 100 best restaurants in America of 2017
r = requests.get('https://www.opentable.com/m/best-restaurants-in-america-for-2017/')
soup = BeautifulSoup(r.content, 'html.parser')
restaurants = []
rest_links = []

# Collecting restaurants names and urls
for rest in soup.find_all('div', class_='restaurant tablet--flex'):
    restaurants.append(rest.find('h3').text)
    rest_links.append('https://www.opentable.com/' + rest.find('a', class_='rest-profile-link').get('href'))


# Creating Restaurant class and collecting features for each Restaurant object
class Restaurant:
    def __init__(self, link):
        self.link = link
        self.r = requests.get(self.link)
        self.soup_rest = BeautifulSoup(self.r.content, 'html.parser')

    def get_overall_rating(self):
        out = {}
        all_ratings = self.soup_rest.find('div', class_='oc-reviews-a20a12c4').text
        all_ratings = re.findall("[\d]?[.]?[\d]", all_ratings)
        out['food'] = all_ratings[0]
        out['service'] = all_ratings[1]
        out['ambience'] = all_ratings[2]
        out['value'] = all_ratings[3]
        return out

    def rating_distribution(self):
        out = re.findall('Rated [1-5] by [\d]+% people', str(self.soup_rest.find('div', class_='oc-reviews-4cf41aa6')))
        return out

    def noise(self):
        out = self.soup_rest.find('div', class_='oc-reviews-dfc07aec').find('span').text
        return out

    def recommendation(self):
        out = re.search('\d\d%', str(self.soup_rest.find_all('div', class_='oc-reviews-3bb4c330'))).group()
        return out

    def num_of_reviews(self):
        summary = self.soup_rest.find('div', class_='d3ba82e4').find_all('div', class_='c3981cf8 _965a91d5')
        out = (summary[1].text).split()[0]
        return out

    def get_date(self, review):
        date = review.find('span', class_='oc-reviews-47b8de40').text
        try:
            if date[-1] == 'o':
                date = datetime.today() + today.timedelta(int(date[6]))
            else:
                date = datetime.strptime(date[9:], '%B %d, %Y')
        except:
            date = None

        return date

    def get_comment_info(self, review):
        """
        Returns place, rating, comment, date of a review.
        Note: only place, returns None
        INPUT: review: BeautifulSoup object of the review
        OUTPUT: tuple of strings: (place, rating, comment, date)
        """
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
        date = self.get_date(review)
        try:
            vip = True if review.find('span', class_='oc-reviews-42b9159d').text == 'vip' else False
        except:
            vip = False
        return (place, rating, comment, date, vip)

    def get_all_reviews(self):
        """
        Initializes the lists of features.
        get_comment_info() for every review.
        Returns a list per feature of all reviews.

        INPUT: rest_link: string of the restaurant link
        OUTPUT: tuple of lists: (places, comments, overall, food, service, ambience, dates)
        """

        places = []
        comments = []
        dates = []
        overall = []
        food = []
        service = []
        ambience = []
        vips = []

        r = requests.get(self.link)  # TODO can be self.r
        soup_rest = BeautifulSoup(r.content, 'html.parser')  # TODO can be self.soup_rest
        # Geting last_page
        pages = soup_rest.find_all('button', class_='reviewUpdateParameter oc-reviews-b0c77e5f')
        for last_page in pages: pass
        last_page = min(MAX_PAGES, int(last_page.text))

        # looping through pages 1 to last_page (min(11, last_page))
        for i in range(1, last_page):
            if i != 1:  # Because it was already read to get the first page
                rest_link = self.link
                rest_link += '?page=' + str(i)
                r = requests.get(rest_link)
                soup_rest = BeautifulSoup(r.content, 'html.parser')

            # Finds all the reviews
            reviews = soup_rest.find_all('div', class_='oc-reviews-5a88ccc3')

            for rev in reviews:
                (place, rating, comment, date, vip) = self.get_comment_info(rev)
                # Stores the variables in lists
                places.append(place)
                comments.append(comment)
                overall.append(int(re.split(r'(\d)', rating)[1]))
                food.append(int(re.split(r'(\d)', rating)[3]))
                service.append(int(re.split(r'(\d)', rating)[5]))
                ambience.append(int(re.split(r'(\d)', rating)[7]))

                dates.append(date)

                vips.append(vip)
        return places, comments, overall, food, service, ambience, dates, vips


# Looping over all restaurants links to get the features
food_rating = []
service_rating = []
ambience_rating = []
value_rating = []
rating_distributions = []
noise_status = []
recommendations = []
nums_of_reviews = []
for link in rest_links:
    print(link)
    temp_res = Restaurant(link)
    try:
        food_rating.append(temp_res.get_overall_rating()['food'])
    except:
        food_rating.append('None')

    try:
        service_rating.append(temp_res.get_overall_rating()['service'])
    except:
        service_rating.append('None')

    try:
        ambience_rating.append(temp_res.get_overall_rating()['ambience'])
    except:
        ambience_rating.append('None')

    try:
        value_rating.append(temp_res.get_overall_rating()['value'])
    except:
        value_rating.append('None')

    try:
        rating_distributions.append(temp_res.rating_distribution())
    except:
        rating_distributions.append('None')

    try:
        noise_status.append(temp_res.noise())
    except:
        noise_status.append('None')

    try:
        recommendations.append(temp_res.recommendation())
    except:
        recommendations.append('None')

    try:
        nums_of_reviews.append(temp_res.num_of_reviews())
    except:
        nums_of_reviews.append('None')

# Creating data base
d = {'Name': restaurants, 'Food rating': food_rating, 'Service rating': service_rating,
     'Ambience rating': ambience_rating, 'Value rating': value_rating,
     'Rating distribution': rating_distributions, 'Noise': noise_status, 'Recommendations': recommendations,
     'No. of reviews': nums_of_reviews}
df = pd.DataFrame(data=d)

print(df)
print(temp_res.get_all_reviews())
