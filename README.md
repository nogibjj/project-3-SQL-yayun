# project-3-SQL-yayun
[![Python application test with Github Actions using devcontainers](https://github.com/nogibjj/project-3-SQL-yayun/actions/workflows/main.yml/badge.svg)](https://github.com/nogibjj/project-3-SQL-yayun/actions/workflows/main.yml)

This is a SQL data analysis project from YAYUN HUANG for DUKE MIDS IDS706 course.

# Question of interst
* What are 10 countries with the highest and the lowest co2 emission in 2018? What are their GDP?
* What are gdp-per-capita, co2-emission-per-person and co2-emission-per-sqkm for the countries found in the previous question
* Which industry cause the most CO2 emission in a specific country?
* Which country have the highest cumulative CO2 since 1995?


# Command to find answer of these question
* What are 10 countries with the highest and the lowest co2 emission in 2018? What are their GDP?
`./cli.py ten-countries`

* What are gdp-per-capita, co2-emission-per-person and co2-emission-per-sqkm for the countries found in the previous question
`./cli.py co2-perunit`

* Which industry cause the most CO2 emission in a specific country?
`./cli.py co2-industry`

* Which country have the highest cumulative CO2 since 1995?
`./cli.py high-cumco2`


Reference
<https://medium.com/@esfoobar/developing-a-flask-postgresql-application-using-github-codespaces-33c01a2d5551>
