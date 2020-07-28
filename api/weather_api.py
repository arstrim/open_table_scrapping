import pymysql.cursors
import json
import logging
import requests
import sys
from datetime import datetime, timedelta
from requests.exceptions import HTTPError
from data_base.build_db import make_connection_db
import api.weather_api_queries as q


API_LIMIT = 1000


def build_weathers(connection):
    """
    Creates table weathers and creates new foreign key to reviews table
    :param connection: connection to database
    :return: None
    """
    with connection.cursor() as cur:
        try:
            cur.execute(q.create_weathers)
        except pymysql.InternalError:
            logging.info('Table weather already exists')

        try:
            cur.execute('''ALTER TABLE reviews ADD COLUMN weather_id INT''')
            cur.execute('''ALTER TABLE reviews ADD FOREIGN KEY (weather_id) REFERENCES weathers(id);''')
        except pymysql.InternalError:
            logging.info('Weather id column in reviews already exists')
    logging.info('Ready to use API')


def exists_weather_id(connection, result):
    """
    Checks if information about this place already exists in the database
    :param connection: connection to database
    :param result: dictionary of date, rest_id and zipcode on database needed to extract weather information
    :return: weather_id: None if there is no information, or the weather_id of that day and place
    """
    with connection.cursor() as cur:
        cur.execute(q.select_weather_id, {'date': result['date'], 'rest_id': result['rest_id']})
        table_weather_ids = cur.fetchall()

    weather_id = None
    for i_id in table_weather_ids:
        if i_id['weather_id'] is not None:
            weather_id = i_id['weather_id']
            break
    return weather_id


def get_weather(connection, result, key):
    """
    Makes a call to weatherbit API,
    inserts the information in weathers table and updates the weather_id in reviews table
    :param connection: connection to database
    :param result: dictionary of date, rest_id and zipcode on database needed to extract weather information
    :param key: API key
    :return: None
    """
    try:
        int(result['zipcode'])
    except ValueError:
        return
    else:
        next_day = str(datetime.strptime(result['date'], '%Y-%m-%d') + timedelta(days=1))[:10]
        try:
            r = requests.get("http://api.weatherbit.io/v2.0/history/daily",
                             params={
                                 'key': key,
                                 "start_date": result['date'],
                                 "end_date": next_day,
                                 "postal_code": result['zipcode']
                             })
            r.raise_for_status()
        except HTTPError:
            logging.critical('cannot find api call')
        else:
            current = r.json()
            logging.debug('requested from api: date: ' + str(result['date']) + ' zipcode: ' + str(result['zipcode']))
            with connection.cursor() as cur:
                try:
                    cur.execute(q.insert_row_weathers, current['data'][0])
                except KeyError:
                    logging.info('exceded API limit: ', str(current))
                else:
                    # INSERT THIS VALUE FOR ALL in weather_id #TODO can be where id in list
                    cur.execute(q.select_reviews_id, {'date': result['date'], 'rest_id': result['rest_id']})
                    ids = cur.fetchall()
                    for id in ids:
                        cur.execute(q.update_weather_id_last_id, {'id': id['id']})
            logging.debug('inserted row in weathers and updated weather_id in reviews')


def update_weather_id_in_reviews(connection, result, weather_id):
    """
    Updates the weather_id in reviews with the existing weather_id found in reviews table
    :param connection: connection to database
    :param result: dictionary of date, rest_id and zipcode on database needed to extract weather information
    :param weather_id: weather id extracted from reviews table
    :return: None
    """
    with connection.cursor() as cur:
        cur.execute(q.select_reviews_id, {'date': result['date'], 'rest_id': result['rest_id']})
        ids = cur.fetchall()
        for id in ids:
            cur.execute(q.update_weather_id, {'weather_id': weather_id, 'id': id['id']})


def weather_api(user, password):
    """
    Looks for all combinations of zipcode and dates in database.
    Creates a new table: weathers and a forgein key in the reviews table to point at it
    Limitations: API_LIMIT limit of calls the program will do, currently it has 4 keys (1000 cals per key),
        if they get used you have to wait a day to reuse them, the program will not crash.
    :param user: username of the database
    :param password: password of the database
    :return: None
    """
    try:
        connection = make_connection_db(user, password)
    except pymysql.err.InternalError:
        logging.critical('Database not found, please load database before trying this api')
        sys.exit()
    build_weathers(connection)
    with connection.cursor() as cur:
        cur.execute(q.select_weather_parameters)
        result = cur.fetchall()

    key = '736defaca7664db3aedb4e753de94e88'
    key1 = '37fefcd23dd04613ba84b4d661d3c1eb'
    key2 = '9f3017b6990c4a5ba7c7d8c4ccd3565d'
    key3 = 'b32537f061e84935ae6700dd9a97ce53'
    keys = [key, key1, key2, key3]
    k = 0   #index of keys

    # for i in range(40, 100): #TODO change for less calls in debug
    for i in range(len(result)):
        logging.info('looping ' + str(i) + ' of total ' + str(len(result)))
        weather_id = exists_weather_id(connection, result[i])
        if weather_id is None:
            get_weather(connection, result[i], keys[k])
            logging.info('call made succesfully')
        else:
            update_weather_id_in_reviews(connection, result[i], weather_id)
        if i % API_LIMIT == 0 and k < len(keys) and i != 0:
            k += 1
            try:
                logging.debug('changed key to: ' + str(keys[k]))
            except IndexError:
                connection.commit()
                logging.info('Not enough keys to perform this database')
                sys.exit()
        if i % (API_LIMIT/10) == 0:
            connection.commit()
    connection.commit()
    logging.info('Updated weathers and reviews table')
