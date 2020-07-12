import pymysql.cursors
import pandas as pd
import logging
import re
import os
import data_base.build_db_queries as q

DB_NAME = 'testing_project'
FOLDER = 'data'
FILENAME = 'reviews.csv'
FILENAME2 = '100restaurants.csv'
MAX_CHAR = 254
USER = 'ariela'
PASSWORD = 'ariela'
logging.basicConfig(level=10)


def make_connection():
    """Returns a connection to create database"""
    connection = pymysql.connect(host='localhost',
                                 user=USER,
                                 password=PASSWORD)
    return connection


def make_connection_db():
    """Returns a connection to modify database"""
    connection = pymysql.connect(host='localhost',
                                 user=USER,
                                 password=PASSWORD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


def get_data():
    """
    Reads restaurants and reviews data from the files.
    It fillsna with 0
    Selects only new data from the reviews that is not in the database
    :return:
    new_data: df of the new reviews data (that is not in the database)
    data2: df of the data of the restaurants
    """
    path = os.path.join(FOLDER,FILENAME)
    print(path)
    data = pd.read_csv(os.path.join(FOLDER,FILENAME))
    data2 = pd.read_csv(os.path.join(FOLDER,FILENAME2))
    data.fillna(0, inplace=True)
    data2.fillna(0, inplace=True)
    data2.replace('None', 0, inplace=True)
    data2.reset_index(inplace=True)
    logging.debug('data.shape:' + str(data.shape))

    connection = make_connection_db()
    with connection.cursor() as cur:
        cur.execute(
            '''SELECT date FROM reviews ORDER BY date DESC LIMIT 1''')
        result = cur.fetchall()
    try:
        last_date = result[0]['date']
    except IndexError:
        last_date = '1900-01-01 00:00:00.000000'
    new_data = data[data['Dates'] > last_date]
    logging.debug('shape new_data:' + str(new_data.shape))
    new_data.reset_index(inplace=True)

    return new_data, data2


def strip_comment(comment):
    """Returns a comment with only alphanumeric and ' ' content"""
    com = re.sub('[^A-Za-z0-9 ]+', ' ', comment)
    len_comment = min(len(com), MAX_CHAR)
    return com[:len_comment]


def insert_restaurants(cur, df):
    """
    Inserts information of df into restaurants table
    :param cur: cursor
    :param df: data frame to be inserted
    :return: None
    """
    for i in range(len(df)):
        cur.execute(q.return_rest_name,
                    {'rest_name': str(df.loc[i, 'Name'])})
        result = cur.fetchall()
        if len(result) > 0:
            # restaurant is in database
            rest_name = result[0]['rest_name']
            cur.execute(q.insert_restaurant,
                        (str(rest_name), str(df.loc[i, 'Location']), str(df.loc[i, 'Cuisine type']),
                         int(df.loc[i, 'No. of reviews']), str(df.loc[i, 'Noise']),
                         float(df.loc[i, 'Food rating']), float(df.loc[i, 'Service rating']),
                         float(df.loc[i, 'Ambience rating']), float(df.loc[i, 'Value rating']),
                         str(df.loc[i, 'Rating distribution']), str(df.loc[i, 'Recommendations'])))

        else:
            # restaurant is not on the table restaurants
            cur.execute(q.insert_n_restaurant,
                        (str(df.loc[i, 'Name']), str(df.loc[i, 'Location']),
                         str(df.loc[i, 'Cuisine type']),
                         int(df.loc[i, 'No. of reviews']), str(df.loc[i, 'Noise']),
                         float(df.loc[i, 'Food rating']), float(df.loc[i, 'Service rating']),
                         float(df.loc[i, 'Ambience rating']), float(df.loc[i, 'Value rating']),
                         str(df.loc[i, 'Rating distribution']), str(df.loc[i, 'Recommendations'])))


def insert_reviews_and_users(cur, df):
    """
    Inserts information of df into the tables reviews and users.
    If the user alreday exists takes its id to the reviews table. Else it creates new user and inserts the review
    :param cur: cursor
    :param df: df of information to insert
    :return: None
    """
    for i in range(len(df)):
        comment = strip_comment(str(df.loc[i, 'Comments']))
        cur.execute(q.return_user_id,
                    {'user': str(df.loc[i, 'Users']), 'place': str(df.loc[i, 'Place'])})
        result = cur.fetchall()
        cur.execute(q.return_rest_id, {'rest_name': str(df.loc[i, 'Name'])})
        id = cur.fetchall()[0]['id']
        if len(result) > 0:
            # User is in database
            user_id = result[0]['id']
            cur.execute(q.insert_reviews_w_user,
                        (int(user_id), int(id), str(df.loc[i, 'Name']), str(comment),
                         int(df.loc[i, 'Overall rating']), int(df.loc[i, 'Food rating']),
                         int(df.loc[i, 'Service rating']),
                         int(df.loc[i, 'Ambience rating']), str(df.loc[i, 'Dates']),
                         int(df.loc[i, 'No. of reviews'])))
        else:
            # User is not on the table users
            cur.execute(q.insert_users,
                        (str(df.loc[i, 'Users']), str(df.loc[i, 'Place']),
                         int(df.loc[i, 'VIP'])))

            cur.execute(q.insert_reviews_n_user,
                        (int(id), str(df.loc[i, 'Name']), str(comment), int(df.loc[i, 'Overall rating']),
                         int(df.loc[i, 'Food rating']), int(df.loc[i, 'Service rating']),
                         int(df.loc[i, 'Ambience rating']),
                         str(df.loc[i, 'Dates']), int(df.loc[i, 'No. of reviews'])))


def build_db():
    """
    If there is no database it creates it with the content of reviews.csv file.
    If there is a database it updates it with the new values in the reviews.csv file it compares it by date.
    It checks if there is an existing user in the users table
    :return: None
    """
    logging.info('Updating database:' + DB_NAME)
    connection = make_connection()

    try:
        # Creates a database
        with connection.cursor() as cur:
            cur.execute('CREATE DATABASE ' + DB_NAME)
        connection = make_connection_db()
        logging.info('Database:' + DB_NAME + ' created')

    except pymysql.err.ProgrammingError:
        # If database is there, it connects to it and filters the new data from the DataFrame
        logging.info('Database:' + DB_NAME + ' found')
        connection = make_connection_db()

    else:
        # Creates the tables for the database
        with connection.cursor() as cur:
            cur.execute(q.create_table_restaurants)
            cur.execute(q.create_table_users)
            cur.execute(q.create_table_reviews)
        logging.info('Created tables')

    finally:
        # Updates the database with all new information
        new_data, data2 = get_data()
        with connection.cursor() as cur:
            insert_restaurants(cur, data2)
            insert_reviews_and_users(cur, new_data)
            connection.commit()

    logging.info('Database updated:' + DB_NAME)

