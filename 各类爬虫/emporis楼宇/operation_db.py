

import sqlite3


def create_sql():
    conn = sqlite3.connect('spider_emporis.db')
    cursor = conn.cursor()
    sql_create = [
                """CREATE TABLE IF NOT EXISTS empories_building(
                building_id integer PRIMARY KEY AUTOINCREMENT,
                continent_name varchar(20) NOT NULL,
                country_name varchar(50) NOT NULL,
                city_name varchar(50) NOT NULL,
                building_name varchar(50) NOT NULL,
                alternative_name varchar(50) default NULL,
                address varchar(255) default NULL,
                height varchar(10) default NULL,
                above_floor varchar(10) default NULL,
                below_floor varchar(10) default NULL,
                start_time varchar(10) default NULL,
                end_time varchar(10) default NULL,
                building_type varchar(50) default NULL,
                building_status varchar(50) default NULL,
                main_usage varchar(100) default NULL,
                side_usage varchar(100) default NULL,
                features_amenities varchar(255) default NULL,
                longitude varchar(30) default NULL,
                latitude varchar(30) default NULL,
                image_address varchar(255) default NULL );""",
                """CREATE TABLE IF NOT EXISTS building_url(
                building_id integer PRIMARY KEY AUTOINCREMENT,
                building_url varchar(255) NOT NULL);"""]
    for sql in sql_create:
        cursor.execute(sql)
    cursor.close()
    conn.close()


def drop_sql():
    conn = sqlite3.connect('spider_emporis.db')
    cursor = conn.cursor()
    sql_drop = ['drop table IF EXISTS building_url', 'drop table IF EXISTS empories_building']
    for sql in sql_drop:
        cursor.execute(sql)
    cursor.close()
    conn.close()


if __name__ == '__main__':
    drop_sql()
    create_sql()


