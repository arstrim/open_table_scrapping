create_table_restaurants = '''CREATE TABLE restaurants (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    rest_name VARCHAR(50),
                    location VARCHAR(255),
                    cuisine_type VARCHAR(50)
                    )'''

create_table_rest_review = '''CREATE TABLE rest_review (
                    rest_id INT,
                    nb_reviews INT,
                    noise VARCHAR(50),
                    food_rating FLOAT,
                    service_rating FLOAT,
                    ambience_rating FLOAT,
                    value_rating FLOAT,
                    rating_distribution VARCHAR(255),
                    recommendations VARCHAR(50),
                    FOREIGN KEY (rest_id) REFERENCES restaurants(id)
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
                    overall INT,
                    food INT,
                    service INT,
                    ambience INT,
                    date VARCHAR(255),
                    n_rev INT,
                    FOREIGN KEY (rest_id) REFERENCES restaurants(id),
                    FOREIGN KEY (user_id) REFERENCES users(id)
                                    )'''

create_table_comments = '''CREATE TABLE comments (
                    rev_id INT,
                    comment LONGTEXT,
                    FOREIGN KEY (rev_id) REFERENCES reviews(id)
                                    )'''


insert_users = '''INSERT INTO users (user, place, vip) VALUES (%s, %s, %s)'''

insert_reviews_w_user = '''INSERT INTO reviews
                                    (user_id, rest_id, restaurant, overall, food,
                                    service, ambience, date, n_rev)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''

insert_reviews_n_user = '''INSERT INTO reviews
                        (user_id, rest_id, restaurant, overall, food, service, ambience, date, n_rev)
                        VALUES (LAST_INSERT_ID(), %s, %s, %s, %s, %s, %s, %s, %s)'''

insert_comment = '''INSERT INTO comments (rev_id, comment) VALUES (LAST_INSERT_ID(), %s)'''

insert_restaurant = '''INSERT INTO restaurants
                                    (rest_name, location, cuisine_type)
                                    VALUES (%s, %s, %s)'''

insert_rest_review = '''INSERT INTO rest_review
                                    (rest_id, nb_reviews, noise,
                                     food_rating, service_rating, ambience_rating, value_rating,
                                     rating_distribution, recommendations)
                                     VALUES (LAST_INSERT_ID(), %s, %s, %s, %s, %s, %s, %s, %s)'''

update_restaurant = '''UPDATE restaurants SET
                                    location = %(loc)s,
                                    cuisine_type = %(cus)s
                                    WHERE id = %(id)s '''

update_rest_review = '''UPDATE rest_review SET
                                    nb_reviews = %(n_rev)s,
                                    noise = %(noise)s,
                                    food_rating = %(f_rate)s,
                                    service_rating = %(s_rate)s,
                                    ambience_rating = %(a_rate)s,
                                    value_rating = %(v_rate)s,
                                    rating_distribution = %(rate_dist)s,
                                    recommendations = %(rec)s
                                    WHERE rest_id = %(id)s '''

#return_rest_name = 'SELECT rest_name FROM restaurants WHERE rest_name = %(rest_name)s'

return_user_id = 'SELECT id FROM users WHERE user = %(user)s AND place = %(place)s'

return_rest_id = 'SELECT id FROM restaurants WHERE rest_name = %(rest_name)s'

