# import required packages
import sqlite3
def create_db_table():
	# create and connect to database
	connect = sqlite3.connect("co2db")
	cursor = connect.cursor()

	# Create table query
	# query to create a table about co2 emission related to each country
	cr_co2 = """CREATE TABLE co2
		(country varchar,
		year_ int,
		iso_code varchar,
		population BIGINT,
		gdpm decimal,
		co2 decimal,
		coal_co2 decimal,
		flaring_co2 decimal, 
		gas_co2 DECIMAL, 
		oil_co2 DECIMAL,
		other_industry_co2 decimal);"""
	# query to create a table about land size, literacy rate related to each country
	cr_land = """CREATE TABLE land_lit
		(country varchar,
		area int, 
		literacy decimal);"""
	
	# execute query to create table
	cursor.execute(cr_co2)
	cursor.execute(cr_land)

if __name__ == "__main__":
	create_db_table()
	