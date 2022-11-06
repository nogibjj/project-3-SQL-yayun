# insert data 
import sqlite3
import csv


def initial_build():
    # execute query
    # connect to database
    connect = sqlite3.connect("co2db")
    cursor = connect.cursor()

    # Insert data query
    # query to insert csv data into existing table
    insert_co2 = """INSERT INTO co2 VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    insert_land = """INSERT INTO land_lit VALUES(?, ?, ?)"""

    # Readl files
    co2_path = "owid-co2-data_2.csv"
    land_path = "land_lit.csv"

    file_co2 = open(co2_path)
    data_co2 = csv.reader(file_co2)
    next(data_co2) # pass header row

    file_land = open(land_path)
    data_land = csv.reader(file_land)
    next(data_land) # pass header row

    # execute inesert query
    cursor.executemany(insert_co2, data_co2)
    cursor.executemany(insert_land, data_land)
    # close and save the change of db
    connect.commit()
	# connect.close()






def insert_db(path, table):
    # execute query
    # connect to database
    connect = sqlite3.connect("co2db")
    cursor = connect.cursor()
    file = open(path)
    data = csv.reader(file)
    next(data) # pass header row
    
    if table == 'co2':
        insert = """INSERT INTO co2 VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    else:
        insert = """INSERT INTO land_lit VALUES(?, ?, ?)"""
    
    cursor.executemany(insert, data)
    connect.commit()
	# connect.close()

if __name__ == "__main__":
    
    initial_build()
    # connect.commit()
	# connect.close()


