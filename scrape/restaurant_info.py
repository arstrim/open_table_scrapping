# import pandas as pd
from scrape.restaurant_class import Restaurant
import pandas as pd
import os
import logging

PATH = os.path.join('data', "100restaurants.csv")


def restaurant_info(rest_links, restaurants, locations):
    """
    scrape info of all the restaurants
    """
    # Looping over all restaurants links to get the features
    food_rating = []
    service_rating = []
    ambience_rating = []
    value_rating = []
    rating_distributions = []
    noise_status = []
    recommendations = []
    nums_of_reviews = []
    cuisine_type = []
    locations_zipcode = []
    i = 0

    logging.info('Writing 100restaurants.csv')

    for idx, link in enumerate(rest_links):
        logging.info('Writing ' +  str(idx) + " of " + str(len(rest_links)))
        i += 1
        temp_res = Restaurant(link)
        try:
            food_rating.append(temp_res.get_overall_rating()['food'])
        except (IndexError, AttributeError):
            food_rating.append('None')

        try:
            service_rating.append(temp_res.get_overall_rating()['service'])
        except (IndexError, AttributeError):
            service_rating.append('None')

        try:
            ambience_rating.append(temp_res.get_overall_rating()['ambience'])
        except (IndexError, AttributeError):
            ambience_rating.append('None')

        try:
            value_rating.append(temp_res.get_overall_rating()['value'])
        except (IndexError, AttributeError):
            value_rating.append('None')

        try:
            rating_distributions.append(temp_res.rating_distribution())
        except AttributeError:
            rating_distributions.append('None')

        try:
            noise_status.append(temp_res.noise())
        except AttributeError:
            noise_status.append('None')

        try:
            recommendations.append(temp_res.recommendation())
        except AttributeError:
            recommendations.append('None')

        try:
            nums_of_reviews.append(temp_res.num_of_reviews())
        except AttributeError:
            nums_of_reviews.append('None')

        try:
            cuisine_type.append(temp_res.cuisine_type())
        except (IndexError, AttributeError):
            cuisine_type.append('None')

        try:
            if temp_res.location()[-1].isdigit():
                locations_zipcode.append(temp_res.location())
            else:
                locations_zipcode.append(locations[idx])
        except AttributeError:
            locations_zipcode.append(None)

    # Creating data base
    d = {'Name': restaurants, 'Location': locations_zipcode, 'Cuisine type': cuisine_type, 'Food rating': food_rating,
         'Service rating': service_rating,
         'Ambience rating': ambience_rating, 'Value rating': value_rating,
         'Rating distribution': rating_distributions, 'Noise': noise_status, 'Recommendations': recommendations,
         'No. of reviews': nums_of_reviews}

    df = pd.DataFrame(data=d)

    # remove any restaurant that has more that 5 none values
    df.dropna(axis=0, thresh=5, inplace=True)
    df.reset_index()

    df.to_csv(PATH)
