import pandas as pd
from restaurant_class import Restaurant

def restaurant_info(rest_links, restaurants):
    """
    Build a data frame of all the restaurants
    :param rest_links: list of restaurant links
    :param restaurants: list of restaurants names
    :return: df: data frame of the general info of the restaurants
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
    i = 0
    for link in rest_links:
        print(link, i)
        i += 1
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

    return df