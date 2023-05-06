import logging
import os

import mysql.connector

logging.basicConfig(filename='app.log', format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)

host = os.getenv('MYSQL_HOST')
user = os.getenv('MYSQL_USER')
password = os.getenv('MYSQL_PASSWORD')
database = os.getenv('MYSQL_DATABASE')

try:
    connect = mysql.connector.connect(
        host=host,
        user=user,
        password=password
    )
except Exception as e:
    logging.error(e)
    raise e

crs = connect.cursor()
crs.execute("""CREATE DATABASE IF NOT EXISTS password_manager_base""")

try:
    connectDB = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
except Exception as e:
    logging.error(e)
    raise e

cursor = connectDB.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tg_id BIGINT
);""")

cursor.execute("""CREATE TABLE IF NOT EXISTS services (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100)
);""")

cursor.execute("""CREATE TABLE IF NOT EXISTS passwords_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    service_id INT,
    login VARCHAR(50),
    password VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE CASCADE ON UPDATE CASCADE
);""")
