import pymysql.cursors
import pandas as pd
import logging
import re
import build_db_queries as q

DB_NAME = 'testing_project'
FILENAME = 'reviews.csv'
FILENAME2 = '100restaurants.csv'
MAX_CHAR = 254
logging.basicConfig(level=10)


def make_connection():
    """Returns a connection to create database"""
    connection = pymysql.connect(host='localhost',
                                 user='ariela',
                                 password='ariela')
    return connection


def make_connection_db():
    """Returns a connection to modify database"""
    connection = pymysql.connect(host='localhost',
                                 user='ariela',
                                 password='ariela',
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


def strip_comment(comment):
    """Returns a comment with only alphanumeric and ' ' content"""
    com = re.sub('[^A-Za-z0-9 ]+', ' ', comment)
    len_comment = min(len(com), MAX_CHAR)
    return com[:len_comment]


def build_db():
    """
    If there is no database it creates it with the content of reviews.csv file.
    If there is a database it updates it with the new values in the reviews.csv file it compares it by date.
    It checks if there is an existing user in the users table
    :return: None
    """
    logging.info('Updating database:' + DB_NAME)
    connection = make_connection()

    data = pd.read_csv(FILENAME)
    data2 = pd.read_csv(FILENAME2)
    data['Dates'].fillna('0', inplace=True)
    data.fillna(0, inplace=True)
    logging.debug('data.shape:' + str(data.shape))

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
        with connection.cursor() as cur:
            cur.execute(
                '''SELECT date FROM reviews WHERE date NOT LIKE 'nan' ORDER BY date DESC LIMIT 1 ''')  # TODO fix date dinned vs reviewd
            result = cur.fetchall()
        last_date = result[0]['date']
        logging.debug('last date on db:' + last_date)
        new_data = data[data['Dates'] > last_date]
        logging.debug('shape new_data:' + str(new_data.shape))

    else:
        # Creates the tables for the database
        new_data = data
        new_data2 = data2
        with connection.cursor() as cur:
            cur.execute(q.create_table_users)
            cur.execute(q.create_table_reviews)
            cur.execute(q.create_table_restaurants)  # TODO missing line check file build_db_queries.py
        logging.info('Created tables')

    finally:
        # Updates the database with all new information
        new_data.reset_index(inplace=True)
        new_data2.reset_index(inplace=True)
        with connection.cursor() as cur:
            for i in range(len(new_data)):
                comment = strip_comment(str(new_data.loc[i, 'Comments']))
                cur.execute(q.return_user_id,
                            {'user': str(new_data.loc[i, 'Users']), 'place': str(new_data.loc[i, 'Place'])})
                result = cur.fetchall()
                if len(result) > 0:
                    # User is in database
                    user_id = result[0]['id']
                    cur.execute(q.insert_reviews_w_user,
                                (int(user_id), str(new_data.loc[i, 'Name']), str(comment),
                                 int(new_data.loc[i, 'Overall rating']), int(new_data.loc[i, 'Food rating']),
                                 int(new_data.loc[i, 'Service rating']),
                                 int(new_data.loc[i, 'Ambience rating']), str(new_data.loc[i, 'Dates']),
                                 int(new_data.loc[i, 'No. of reviews'])))
                else:
                    # User is not on the table users
                    cur.execute(q.insert_users,
                                (str(new_data.loc[i, 'Users']), str(new_data.loc[i, 'Place']),
                                 int(new_data.loc[i, 'VIP'])))

                    cur.execute(q.insert_reviews_n_user,
                                (str(new_data.loc[i, 'Name']), str(comment), int(new_data.loc[i, 'Overall rating']),
                                 int(new_data.loc[i, 'Food rating']), int(new_data.loc[i, 'Service rating']),
                                 int(new_data.loc[i, 'Ambience rating']),
                                 str(new_data.loc[i, 'Dates']), int(new_data.loc[i, 'No. of reviews'])))

            for i in range(len(new_data2)):
                cur.execute(q.return_rest_name,
                            {'rest_name': str(new_data2.loc[i, 'Name'])})
                result = cur.fetchall()
                if len(result) > 0:
                    # restaurant is in database
                    rest_name = result[0]['rest_name']
                    cur.execute(q.insert_restaurant,
                                (str(rest_name), str(new_data2.loc[i, 'Location']), str(new_data2.loc[i, 'Cuisine type']),
                                 int(new_data2.loc[i, 'No. of reviews']), str(new_data2.loc[i, 'Noise']),
                                 float(new_data2.loc[i, 'Food rating']), float(new_data2.loc[i, 'Service rating']),
                                 float(new_data2.loc[i, 'Ambience rating']), float(new_data2.loc[i, 'Value rating']),
                                 str(new_data2.loc[i, 'Rating distribution']), int(new_data2.loc[i, 'Recommendations'])))

                else:
                    # restaurant is not on the table restaurants
                    cur.execute(q.insert_n_restaurant,
                                (str(new_data2.loc[i, 'Name']), str(new_data2.loc[i, 'Location']),
                                 str(new_data2.loc[i, 'Cuisine type']),
                                 int(new_data2.loc[i, 'No. of reviews']), str(new_data2.loc[i, 'Noise']),
                                 float(new_data2.loc[i, 'Food rating']), float(new_data2.loc[i, 'Service rating']),
                                 float(new_data2.loc[i, 'Ambience rating']), float(new_data2.loc[i, 'Value rating']),
                                 str(new_data2.loc[i, 'Rating distribution']), int(new_data2.loc[i, 'Recommendations'])))

            connection.commit()

    logging.info('Database updated:' + DB_NAME)

