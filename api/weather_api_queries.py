create_weathers = '''CREATE TABLE weathers (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        rh FLOAT,
                        max_wind_spd_ts INT,
                        t_ghi FLOAT,
                        max_wind_spd FLOAT,
                        solar_rad FLOAT,
                        wind_gust_spd FLOAT,
                        max_temp_ts INT,
                        min_temp_ts INT,
                        clouds INT,
                        max_dni FLOAT,
                        precip_gpm INT,
                        wind_spd FLOAT,
                        slp FLOAT,
                        ts INT,
                        max_ghi FLOAT,
                        temp FLOAT,
                        pres FLOAT,
                        dni FLOAT,
                        dewpt FLOAT,
                        snow INT,
                        dhi INT,
                        precip FLOAT,
                        wind_dir INT,
                        max_dhi FLOAT,
                        ghi FLOAT,
                        max_temp INT,
                        t_dni FLOAT,
                        max_uv FLOAT,
                        t_dhi FLOAT,
                        t_solar_rad FLOAT,
                        min_temp FLOAT,
                        max_wind_dir INT,
                        snow_depth INT);
                        '''

select_weather_parameters = '''select substring(rev.date,1,10) as date, substring(res.location,-5) as zipcode, rev.rest_id from reviews as rev
    inner join restaurants as res on rev.rest_id = res.id
    group by substring(rev.date,1,10),rev.rest_id
    order by res.rest_name;'''

select_weather_id = '''select weather_id from reviews where substring(date,1,10)=%(date)s and rest_id=%(rest_id)s;'''

insert_row_weathers = '''insert into weathers (rh, max_wind_spd_ts, t_ghi, max_wind_spd,
                solar_rad, wind_gust_spd, max_temp_ts, min_temp_ts, clouds, max_dni,
                precip_gpm, wind_spd, slp, ts, max_ghi,
                temp, pres, dni, dewpt, snow, dhi, precip, wind_dir, max_dhi,
                ghi, max_temp, t_dni, max_uv, t_dhi, t_solar_rad, min_temp, max_wind_dir, snow_depth)
                values (%(rh)s, %(max_wind_spd_ts)s, %(t_ghi)s, %(max_wind_spd)s,
                %(solar_rad)s, %(wind_gust_spd)s, %(max_temp_ts)s, %(min_temp_ts)s, %(clouds)s, %(max_dni)s,
                %(precip_gpm)s, %(wind_spd)s, %(slp)s, %(ts)s, %(max_ghi)s,
                %(temp)s, %(pres)s, %(dni)s, %(dewpt)s, %(snow)s, %(dhi)s, %(precip)s, %(wind_dir)s, %(max_dhi)s,
                %(ghi)s, %(max_temp)s, %(t_dni)s, %(max_uv)s, %(t_dhi)s, %(t_solar_rad)s, %(min_temp)s, %(max_wind_dir)s, %(snow_depth)s)'''

select_reviews_id = '''SELECT id FROM reviews
                        WHERE substring(date, 1, 10) = %(date)s
                        AND rest_id = %(rest_id)s;'''


update_weather_id_last_id = '''UPDATE reviews SET weather_id = LAST_INSERT_ID() WHERE id = %(id)s;'''

update_weather_id = '''UPDATE reviews SET weather_id = %(weather_id)s WHERE id = %(id)s;'''