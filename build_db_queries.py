create_table_users = '''CREATE TABLE users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user VARCHAR(50),
                    place VARCHAR(50),
                    vip INT
                    )'''

create_table_reviews = '''CREATE TABLE reviews (
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
                                    )'''

            # missing line: FOREIGN KEY (res_id) REFERENCES restaurants(id), #TODO

insert_users = '''INSERT INTO users (user, place, vip) VALUES (%s, %s, %s)'''

return_user_id = 'SELECT id FROM users WHERE user = %(user)s AND place = %(place)s'

insert_reviews_w_user = '''INSERT INTO reviews
                                    (user_id, restaurant, comment, overall, food,
                                    service, ambience, date, n_rev)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''

insert_reviews_n_user = '''INSERT INTO reviews
                        (user_id, restaurant, comment, overall, food, service, ambience, date, n_rev)
                        VALUES (LAST_INSERT_ID(), %s, %s, %s, %s, %s, %s, %s, %s)'''

