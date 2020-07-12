create_table_restaurants = '''CREATE TABLE restaurants (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    rest_name VARCHAR(50),
                    location VARCHAR(255),
                    cuisine_type VARCHAR(50),
                    nb_reviews INT,
                    noise VARCHAR(50),
                    food_rating FLOAT,
                    service_rating FLOAT,
                    ambience_rating FLOAT,
                    value_rating FLOAT,
                    rating_distribution VARCHAR(255),
                    recommendations VARCHAR(50)
                    )'''



create_table_users = '''CREATE TABLE users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user VARCHAR(50),
                    place VARCHAR(50),
                    vip BIT 
                    )'''

create_table_reviews = '''CREATE TABLE reviews (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    rest_id INT,
                    user_id INT,
                    restaurant VARCHAR(50),
                    comment LONGTEXT,
                    overall INT,
                    food INT,
                    service INT,
                    ambience INT,
                    date VARCHAR(255),
                    n_rev INT,
                    FOREIGN KEY (rest_id) REFERENCES restaurants(id),
                    FOREIGN KEY (user_id) REFERENCES users(id)
                                    )'''


insert_users = '''INSERT INTO users (user, place, vip) VALUES (%s, %s, %s)'''

return_user_id = 'SELECT id FROM users WHERE user = %(user)s AND place = %(place)s'

return_rest_id = 'SELECT id FROM restaurants WHERE rest_name = %(rest_name)s';

insert_reviews_w_user = '''INSERT INTO reviews
                                    (user_id, rest_id, restaurant, comment, overall, food,
                                    service, ambience, date, n_rev)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

insert_restaurant = '''INSERT INTO restaurants
                                    (rest_name, location, cuisine_type, nb_reviews, noise,
                                    food_rating, service_rating, ambience_rating, value_rating, 
                                    rating_distribution, recommendations)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

insert_reviews_n_user = '''INSERT INTO reviews
                        (user_id, rest_id, restaurant, comment, overall, food, service, ambience, date, n_rev)
                        VALUES (LAST_INSERT_ID(), %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

insert_n_restaurant = '''INSERT INTO restaurants
                                    (rest_name, location, cuisine_type, nb_reviews, noise,
                                    food_rating, service_rating, ambience_rating, value_rating, 
                                    rating_distribution, recommendations)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

return_rest_name = 'SELECT rest_name FROM restaurants WHERE rest_name = %(rest_name)s'

