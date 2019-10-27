import sqlite3


def create_sql_hw():
    conn = sqlite3.connect('huawei_shop.db')
    cursor = conn.cursor()
    sql_create = [
        """CREATE TABLE IF NOT EXISTS store_huawei(
        store_id integer PRIMARY KEY AUTOINCREMENT,
        name varchar(100) NOT NULL,
        address varchar(255) default NULL,
        province varchar(50) default NULL,
        city varchar(50) default NULL,
        dist varchar(50) default NULL,
        bd_longitude varchar(30) default NULL,
        bd_latitude varchar(30) default NULL,
        gps_longitude varchar(30) default NULL,
        gps_latitude varchar(30) default NULL,
        image varchar(255) default NULL);"""]
    for sql in sql_create:
        cursor.execute(sql)
    cursor.close()
    conn.close()


def create_sql_ry():
    conn = sqlite3.connect('huawei_shop.db')
    cursor = conn.cursor()
    sql_create = [
        """CREATE TABLE IF NOT EXISTS store_rongyao(
        store_id integer PRIMARY KEY AUTOINCREMENT,
        name varchar(100) NOT NULL,
        address varchar(255) default NULL,
        province varchar(50) default NULL,
        city varchar(50) default NULL,
        dist varchar(50) default NULL,
        bd_longitude varchar(30) default NULL,
        bd_latitude varchar(30) default NULL,
        gps_longitude varchar(30) default NULL,
        gps_latitude varchar(30) default NULL,
        image varchar(255) default NULL);"""]
    for sql in sql_create:
        cursor.execute(sql)
    cursor.close()
    conn.close()


def drop_sql():
    conn = sqlite3.connect('huawei_shop.db')
    cursor = conn.cursor()
    sql_drop = ['drop table IF EXISTS store_rongyao']
    for sql in sql_drop:
        cursor.execute(sql)
    cursor.close()
    conn.close()


if __name__ == '__main__':
    drop_sql()
    # create_sql_hw()
    create_sql_ry()
