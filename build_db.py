# pip install PyMySQL #TODO requirementx.txt
import pymysql.cursors
import pandas as pd

DB_NAME = 'testing_project'
FILENAME = 'reviews.csv'

#TODO (2) connections in a separate file
#TODO comments
#TODO pretiffy (del prints)

def build_db():
    print('Updating database:', DB_NAME)
    connection = pymysql.connect(host='localhost',
                                 user='ariela',
                                 password='ariela')

    data = pd.read_csv(FILENAME)
    data['Date'].fillna('999', inplace=True)
    data.fillna(0, inplace=True)
    # print(data.shape)


    try:
        with connection.cursor() as cur:
            # print('try: Creating database', DB_NAME)
            cur.execute('CREATE DATABASE '+ DB_NAME)
            # cur.execute('SHOW DATABASES')
            # for x in cur:
            #     print(x)
        connection = pymysql.connect(host='localhost',
                                     user='ariela',
                                     password='ariela',
                                     db=DB_NAME,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)



    except pymysql.err.ProgrammingError:
        # print('In except')
        connection = pymysql.connect(host='localhost',
                                     user='ariela',
                                     password='ariela',
                                     db=DB_NAME,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cur:
            cur.execute('''SELECT date FROM reviews WHERE date NOT LIKE 'nan' ORDER BY date DESC LIMIT 1 ''') #TODO fix date dinned vs reviewd
            result = cur.fetchall()
        last_date = result[0]['date']
        # print(type(last_date), last_date)
        # print(data[data['Date']>last_date])
        new_data = data[data['Date']>last_date]
        # print("last_date:", last_date)
        # print("new data: \n", new_data, '\n', len(new_data))


    else:
        # print('in else')
        new_data = data
        with connection.cursor() as cur:
            # cur.execute('SHOW TABLES')
            # for x in cur:
            #     print(x)

            cur.execute('''CREATE TABLE users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user VARCHAR(50),
                    place VARCHAR(50),
                    vip INT
                    )''')

            cur.execute('''CREATE TABLE reviews (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    res_id INT,
                    user_id INT,
                    restaurant VARCHAR(50),
                    comment LONGTEXT,
                    overall INT,
                    food INT,
                    service INT,
                    ambience INT,
                    date VARCHAR(255),
                    n_rev INT,

                    FOREIGN KEY (user_id) REFERENCES users(id)
                                    )''')


            # missing line: FOREIGN KEY (res_id) REFERENCES restaurants(id), #TODO

            # cur.execute('SHOW TABLES')
            # for x in cur:
            #     print(x)



    finally:
        # print('in finally')
        new_data.reset_index(inplace=True)
        with connection.cursor() as cur:
            for i in range(len(new_data)):
                querry = 'select id from users where user = \'' +  str(new_data.loc[i, 'User']) + '\' and place = \'' + str(new_data.loc[i, 'Place']) + '\';'
                cur.execute(querry)
                result = cur.fetchall()
                if len(result)>0:
                    user_id = result[0]['id']
                    cur.execute("""INSERT INTO reviews
                                    (user_id, restaurant, comment, overall, food,
                                    service, ambience, date, n_rev)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                                # TODO str(new_data.loc[i,'Comment'])
                                (int(user_id), str(new_data.loc[i, 'Name']), 'comment', int(new_data.loc[i, 'Overall']),
                                 int(new_data.loc[i, 'Food']),
                                 int(new_data.loc[i, 'Service']), int(new_data.loc[i, 'Ambience']),
                                 str(new_data.loc[i, 'Date']),
                                 int(new_data.loc[i, 'N_rev'])))

                else:
                    cur.execute("""INSERT INTO users (user, place, vip)
                                                    VALUES (%s, %s, %s)""",
                                (str(new_data.loc[i, 'User']), str(new_data.loc[i, 'Place']), int(new_data.loc[i, 'Vip'])))

                    cur.execute("""INSERT INTO reviews
                    (user_id, restaurant, comment, overall, food,
                    service, ambience, date, n_rev)

                    VALUES (LAST_INSERT_ID(), %s, %s, %s, %s, %s, %s, %s, %s)""",  #TODO str(new_data.loc[i,'Comment'])
                                (str(new_data.loc[i, 'Name']), 'comment', int(new_data.loc[i, 'Overall']), int(new_data.loc[i, 'Food']),
                                 int(new_data.loc[i, 'Service']), int(new_data.loc[i, 'Ambience']), str(new_data.loc[i, 'Date']),
                                 int(new_data.loc[i, 'N_rev'])))

            # cur.execute('''select * from reviews LIMIT 5''')
            # for x in cur:
            #     print(x)
            connection.commit()

    print('\nDatabase updated:', DB_NAME)

# build_db()

