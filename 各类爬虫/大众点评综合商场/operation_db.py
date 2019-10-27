

import sqlite3


def create_sql():
    conn = sqlite3.connect('shop_data.db')
    cursor = conn.cursor()
    sql_create = [
                """CREATE TABLE IF NOT EXISTS dzdp_shop(
                shop_id integer PRIMARY KEY AUTOINCREMENT,
                shop_name varchar(100) NOT NULL,
                shop_address varchar(255) default NULL,
                shop_province varchar(50) default NULL,
                shop_city varchar(50) default NULL,
                shop_city_dp varchar(50) default NULL,
                shop_level varchar(50) default NULL,
                shop_comment varchar(50) default NULL,
                shop_consume varchar(50) default NULL,
                shop_quality varchar(50) default NULL,
                shop_env varchar(50) default NULL,
                shop_service varchar(50) default NULL,
                g_longitude varchar(30) default NULL,
                g_latitude varchar(30) default NULL,
                gps_longitude varchar(30) default NULL,
                gps_latitude varchar(30) default NULL,
                shop_image varchar(255) default NULL,
                shop_url varchar(255) default NULL);"""]
    for sql in sql_create:
        cursor.execute(sql)
    cursor.close()
    conn.close()


def drop_sql():
    conn = sqlite3.connect('shop_data.db')
    cursor = conn.cursor()
    sql_drop = ['drop table IF EXISTS dzdp_shop']
    for sql in sql_drop:
        cursor.execute(sql)
    cursor.close()
    conn.close()


if __name__ == '__main__':
    drop_sql()
    create_sql()


