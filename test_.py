import sqlite3
from a2_querydb import (
    connect_db,
    create_df,
    top10_2018,
    per_unit,
    industry_co2,
    cum_co2,
)


def test_connect_db():
    assert connect_db() is not None


cursor = connect_db()


def test_create_df():
    assert create_df(
        cursor.execute("SELECT COUNT(*) AS count FROM co2").fetchall(), cursor
    ).columns == ["count"]


def test_top10_2018():
    q1_10_low = "SELECT year_, country, co2, gdpm FROM co2 WHERE (year_ = 2018) AND (co2 IS NOT '') AND (gdpm IS NOT '') ORDER BY co2 LIMIT 10"
    assert top10_2018().equals(create_df(cursor.execute(q1_10_low).fetchall(), cursor))


def test_per_unit():
    assert per_unit().columns[0] == "co2_per_person_mg"


def test_industry_co2():
    assert industry_co2().columns[0] == "year_"


def test_cum_co2():
    assert cum_co2().columns[0] == "year_"
