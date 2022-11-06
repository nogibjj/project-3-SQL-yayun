#!/usr/bin/env python

# command line app
import click
import sqlite3
from a1_insertdb import insert_db
from a2_querydb import connect_db, create_df, top10_2018, per_unit, cum_co2_highest, industry_co2, cum_co2

# build a click group
@click.group()
def cli():
    """A simple CLI to query a SQL database"""

# build  click commands to insert new data
@cli.command()
@click.option(
    "--filename",
    prompt = "enter file name")
@click.option(
    "--table",
    prompt = "enter table name(co2/land_lit) to insert new data",
)
def cli_insert(filename, table):
    """insert new data to existing table"""
    insert_db(filename, table)

# build click commands to direct query database
@cli.command()
@click.option(
    "--query",
    prompt = "enter query to query country_co2(co2db) database"
)
def cli_query(query):
    """query co2db"""
    # connect to database
    connect = sqlite3.connect("co2db")
    cursor = connect.cursor()
    df = create_df(cursor.execute(query).fetchall())
    print(df)

# build click commands to execute prebuilt query
@cli.command()
def ten_countries():
    """Conturies with 10 highest and 10 lowest CO2 emission in 2018"""
    top10_2018()
@cli.command()
def co2_perunit():
    """average co2 emission per perspon, per sq.km and GDP per capita"""
    per_unit()

@cli.command()
def cum_co2():
    """Find country with the highest cumulative co2 since 1990 in 2018"""
    cum_co2_highest()

@cli.command()
@click.option(
    "--country",
    prompt = "Enter country name(First letter uppercase)"
)
def industry_co2(country):
    """Find cumulative CO2 emission in different industry of intersted country"""
    industry_co2(country)

@cli.command()
def high_cumCo2():
    cum_co2()

# run the CLI
if __name__ == "__main__":
    cli()









