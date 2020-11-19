import cv2
import os

import mysql.connector

import pymysql

db_name="DB_Animes2"

db2 = pymysql.connect("localhost","root","cc",db_name)
print(db2)

cursor2 = db2.cursor ()

table_name = "Madoka"
create_fields_comm = f"CREATE TABLE {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, anime_name VARCHAR(255), episode_num VARCHAR(255), capture_time VARCHAR(255), img LONGBLOB NOT NULL, text VARCHAR(255))"

insert_statement=f"INSERT INTO {table_name} (word_missing) VALUES (%s)"

cursor2.execute(insert_statement)