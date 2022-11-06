import sqlite3
import numpy as np
import pandas as pd

def connect_db():
    connect = sqlite3.connect("co2db")
    cursor = connect.cursor()
    return cursor

def create_df(results, cursor):
    column_names = [x[0] for x in cursor.description]
    df = pd.DataFrame(results, columns = column_names)
    return df

# Query to answer some questions of interest

# query 1: 
# q1-high: in 2018, which 10 countries have highest co2 emmision? what is their average GDP?
# q1-low: in 2018, which 10 countries have lowest co2 emmision? what is their average GDp?


def top10_2018(cursor = connect_db()):
    q1_10_high = "SELECT year_, country, co2, gdpm FROM co2 WHERE (year_ = 2018) AND (co2 IS NOT '') ORDER BY co2 DESC LIMIT 10"
    q1_10_low = "SELECT year_, country, co2, gdpm FROM co2 WHERE (year_ = 2018) AND (co2 IS NOT '') AND (gdpm IS NOT '') ORDER BY co2 LIMIT 10"
    high_avearge = f'WITH t1 AS ({q1_10_high}) SELECT AVG(gdpm) GDP FROM t1'
    low_avearge = f'WITH t1 AS ({q1_10_low}) SELECT AVG(gdpm) GDP FROM t1'

    high_df = create_df(cursor.execute(q1_10_high).fetchall(),cursor)
    print("Top 10 countries with highest Co2(tons) emission in 2018:")
    print(high_df)
    high_avg_df = int(cursor.execute(high_avearge).fetchall()[0][0])
    print(f"The average GDP of these 10 countries is {high_avg_df} millions.")
    print("")
    low_df = create_df(cursor.execute(q1_10_low).fetchall(),cursor)
    print("Top 10 countries with lowest Co2(tons)  emission in 2018:")
    print(low_df)
    low_avg_df = int(cursor.execute(low_avearge).fetchall()[0][0])
    print(f"The average GDP of these 10 countries is {low_avg_df} millions.")

# query 2: 
# What's average co2 emission per person and co2 emission per sq.km in the highest and the lowest 10 co2 emission country

def per_unit(cursor = connect_db()):
    q2_high = """WITH thigh AS(SELECT c.*, l.area, l.literacy
        FROM  co2 AS c
        JOIN land_lit AS l
        ON c.country = l.country
        WHERE c.year_ = 2018 AND c.co2 IS NOT ''
        ORDER BY c.co2 DESC
        LIMIT 10)

        SELECT AVG(co2*1000000000/population) co2_per_person_mg, AVG(co2*1000000/area) co2_per_sqft_g, AVG(gdpm * 1000/population) gdp
        FROM thigh"""

    q2_low = """WITH tlow AS(SELECT c.*, l.area, l.literacy
        FROM  co2 AS c
        JOIN land_lit AS l
        ON c.country = l.country
        WHERE c.year_ = 2018 AND c.co2 IS NOT ''
        ORDER BY c.co2
        LIMIT 10)
        SELECT AVG(co2*1000000000/population) co2_per_person_mg, AVG(co2*1000000/area) co2_per_sqft_g, AVG(gdpm * 1000/population) gdp
        FROM tlow"""
    

    high_df = create_df(cursor.execute(q2_high).fetchall(),cursor)
    print(f"In the top 10 co2 emission countries, \nco2 emission per person: {np.round(high_df.iloc[0,0])} gram CO2.\nco2 emission per sq.km : {np.round(high_df.iloc[0,1])} gram CO2.")
    print(f"GDP per capita: {np.round(high_df.iloc[0,2],3)} K.")

    print("")
    low_df = create_df(cursor.execute(q2_low).fetchall(),cursor)
    print(f"In the last 10 co2 emission countries, \nco2 emission per person: {np.round(low_df.iloc[0,0])} gram CO2.\nco2 emission per sq.km : {np.round(low_df.iloc[0,1])} gram CO2.")
    print(f"GDP per capita: {np.round(low_df.iloc[0,2],3)} K.")

# query 3
# In past 10(till 2018) years, which country has the highest cumulative CO2 emission?

def cum_co2_highest(cursor = connect_db()):
    q3 = """WITH t3 AS(
        SELECT *
        FROM co2
        WHERE (year_ <= 2018) AND (year_ > 2008))
        
        SELECT year_, country, 
            SUM(co2) OVER (PARTITION BY country ORDER BY year_) AS cumulative_co2
        FROM t3
        WHERE (year_ = 2018) AND (t3.co2 IS NOT '')
        ORDER BY cumulative_co2 DESC
        LIMIT 1"""
    country = create_df(cursor.execute(q3).fetchall(),cursor).iloc[0,1] 
    print(f"From 2008 till 2018, {country} has the highest cumulative CO2 emission.")
# query 4
# from query 4, we found the country with highest cumulative CO2 emission is China. Now, I want to check from which industry it led to most CO2 emission. Coal caused most co2 emission, then oil, then gas, then other


def industry_co2(cursor = connect_db(), country = "China"):
    q4_china = f"""
        SELECT year_,
        SUM(co2) OVER (PARTITION BY country ORDER BY year_) AS cumulative_co2,
        SUM(coal_co2) OVER (PARTITION BY country ORDER BY year_) AS cumulative_coal_co2,
        SUM(gas_co2) OVER (PARTITION BY country ORDER BY year_) AS cumulative_gas_co2,
        SUM(oil_co2) OVER (PARTITION BY country ORDER BY year_) AS cumulative_oil_co2,
        SUM(other_industry_co2) OVER (PARTITION BY country ORDER BY year_) AS cumulative_other_co2
        FROM co2
        WHERE (year_ <= 2018) AND (year_ > 2008) AND (country = {country})
        LIMIT 3   
    """
    q4_us =  """
        SELECT year_,
        SUM(co2) OVER (PARTITION BY country ORDER BY year_) AS cumulative_co2,
        SUM(flaring_co2) OVER (PARTITION BY country ORDER BY year_) AS cumulative_flaring_co2,
        SUM(coal_co2) OVER (PARTITION BY country ORDER BY year_) AS cumulative_coal_co2,
        SUM(gas_co2) OVER (PARTITION BY country ORDER BY year_) AS cumulative_gas_co2,
        SUM(oil_co2) OVER (PARTITION BY country ORDER BY year_) AS cumulative_oil_co2,
        SUM(other_industry_co2) OVER (PARTITION BY country ORDER BY year_) AS cumulative_other_co2
        FROM co2
        WHERE (year_ <= 2018) AND (year_ > 2008) AND (country = 'United States')
        LIMIT 1   
    """

    industry_dfc = create_df(cursor.execute(q4_china).fetchall(),cursor)
    print("CO2 emission from each industry in China:")
    print(industry_dfc)

    industry_dfus = create_df(cursor.execute(q4_us).fetchall(),cursor)
    print("CO2 emission from each industry in US:")
    print(industry_dfus)

# query 5
# Identify the country with the highest cumulative CO2 since 1990 (), I want to know in which year China's CO2 emission exceed US

def cum_co2(cursor = connect_db()):
    q5 = """
        WITH t1 AS(
        SELECT year_, country, 
        SUM(co2) OVER (PARTITION BY country ORDER BY year_) AS cumulative_co2 
        FROM (SELECT * FROM co2 WHERE year_ >= 1990) sub)
                
        SELECT a.year_, a.country
        FROM t1 as a
        JOIN (SELECT year_, MAX(cumulative_co2) max_cum FROM t1 GROUP BY year_) b
        ON a.year_ = b.year_ AND a.cumulative_co2 = b.max_cum
        WHERE a.year_ > 2000
    """
    df = create_df(cursor.execute(q5).fetchall(),cursor)
    print("The country with highest cumulative CO2 emission since 1995")
    print(df)
    return cursor
