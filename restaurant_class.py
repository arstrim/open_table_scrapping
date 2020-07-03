import re 
import requests
from bs4 import BeautifulSoup


LINK = 'https://www.opentable.com/m/best-restaurants-in-america-for-2017/'



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

