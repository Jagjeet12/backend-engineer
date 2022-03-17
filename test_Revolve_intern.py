

import pandas as pd
import pytest


# Q1 how many total number of days does the flights table cover?
def total_no_of_days_in_flight_table(path_of_flights_csv):
    try:
        flights = pd.read_csv(path_of_flights_csv)
        flights["date"] = flights.year.astype('str') + "-" + flights.month.astype('str') + "-" + flights.day.astype(
            'str')
        y = flights.date.unique().shape[0]
        return y
        #Answer: 365
    except Exception:
        print("Error:{}".format(Exception.with_traceback))


# Q2 how many departure cities (not airports) does the flights database cover?
def total_no_of_dep_cities_in_flight_table(path_of_flights_csv, path_of_airport_csv):
    try:
        airports = pd.read_csv(path_of_airport_csv)
        flights = pd.read_csv(path_of_flights_csv)
        x = flights.origin.unique().tolist()
        y = airports.query('IATA_CODE in @x')['CITY'].unique().shape[0]
        print('Total no. of Departure Cities in Flight table are {}'.format(y))
        return y
        #Answer: 2
    except Exception:
        print("Error:{}".format(Exception.with_traceback))


# Q3 what is the relationship between flights and planes tables?
def relation_between_flights_and_planes(path_of_flights_csv, path_of_planes_csv):
    try:
        flight = pd.read_csv(path_of_flights_csv)
        planes = pd.read_csv(path_of_planes_csv)
        x = [i for i in planes.columns.tolist() if i in flight.columns.tolist()]
        z = []
        for i in x:
            a = planes[i].unique()
            b = flight[i].unique()
            if all(item in b for item in a):
                if (planes.shape[0] == a.shape[0]) and (flight[i].shape[0] > b.shape[0]):
                    z.append("Planes and Flights table have one-to-many relation on column " + str(i))

            if all(item in a for item in b):
                if (planes.shape[0] > a.shape[0]) and (flight[i].shape[0] == b.shape[0]):
                    z.append("Flights and Planes table have one-to-many relation on column " + str(i))

        return z
        #Answer: ["Flights and Planes table have one-to-many relation on column tailnum"]
    except Exception:
        print("Error:{}".format(Exception.with_traceback))


# Q4 which airplane manufacturer incurred the most delays in the analysis period?
def manufacturer_with_max_delay(path_of_flights_csv, path_of_planes_csv):
    try:
        flight = pd.read_csv(path_of_flights_csv)
        planes = pd.read_csv(path_of_planes_csv)
        df = pd.merge(planes, flight, on='tailnum', how='right')
        df['Total delay'] = df['dep_delay'] + df['arr_delay']
        df = df.groupby('manufacturer')[['manufacturer', 'Total delay']].sum('Total delay')
        x = df[df['Total delay'] == df['Total delay'].max()].index[0]
        return x
        #Answer: 'EMBRAER'
    except Exception:
        print("Error:{}".format(Exception.with_traceback))


# Q5 which are the two most connected cities?
def two_most_connected_cities(path_of_flights_csv, path_of_airport_csv):
    try:
        airports = pd.read_csv(path_of_airport_csv)
        flights = pd.read_csv(path_of_flights_csv)
        df = flights.groupby(['origin', 'dest']).count()
        idx = df[df['day'] == df['day'].max()].index[0]
        y = airports.query('IATA_CODE in @idx')['CITY'].unique().tolist()
        print('Two most connected cities are "{}" and "{}" '.format(y[0], y[1]))
        return y
        #Answer: ['New York', 'Los Angeles']
    except Exception:
        print("Error:{}".format(Exception.with_traceback))


# using pytest to test these functions()
@pytest.mark.parametrize("path_of_flights_csv,expected", [('flights.csv', 365)])
def test_fuc1(path_of_flights_csv, expected):
    assert total_no_of_days_in_flight_table(path_of_flights_csv) == expected


@pytest.mark.parametrize("path_of_flights_csv,path_of_airport_csv,expected", [('flights.csv', 'airports.csv', 2)])
def test_fuc2(path_of_flights_csv, path_of_airport_csv, expected):
    assert total_no_of_dep_cities_in_flight_table(path_of_flights_csv, path_of_airport_csv) == expected


@pytest.mark.parametrize("path_of_flights_csv,path_of_planes_csv,expected", [
    ('flights.csv', 'planes.csv', ["Planes and Flights table have one-to-many relation on column tailnum"])])
def test_fuc3(path_of_flights_csv, path_of_planes_csv, expected):
    assert relation_between_flights_and_planes(path_of_flights_csv, path_of_planes_csv) == expected


@pytest.mark.parametrize("path_of_flights_csv, path_of_planes_csv,expected", [('flights.csv', 'planes.csv', 'EMBRAER')])
def test_fuc4(path_of_flights_csv, path_of_planes_csv, expected):
    assert manufacturer_with_max_delay(path_of_flights_csv, path_of_planes_csv) == expected


@pytest.mark.parametrize("path_of_flights_csv,path_of_airport_csv,expected",
                         [('flights.csv', 'airports.csv', ['New York', 'Los Angeles'])])
def test_fuc5(path_of_flights_csv, path_of_airport_csv, expected):
    assert two_most_connected_cities(path_of_flights_csv, path_of_airport_csv) == expected


# ===================================================================== test session starts ======================================================================
# platform win32 -- Python 3.8.8, pytest-6.2.3, py-1.10.0, pluggy-0.13.1 -- C:\Users\Tarsampaji\anaconda3\python.exe
# cachedir: .pytest_cache
# rootdir: C:\Users\Tarsampaji\Desktop\DataScience\Intern\Revolve\backend-engineer-main\data
# plugins: anyio-2.2.0
# collected 5 items
#
# test_Revolve_intern.py::test_fuc1[flights.csv-365] PASSED                                                                                                 [ 20%]
# test_Revolve_intern.py::test_fuc2[flights.csv-airports.csv-2] PASSED                                                                                      [ 40%]
# test_Revolve_intern.py::test_fuc3[flights.csv-planes.csv-expected0] PASSED                                                                                [ 60%]
# test_Revolve_intern.py::test_fuc4[flights.csv-planes.csv-EMBRAER] PASSED                                                                                  [ 80%]
# test_Revolve_intern.py::test_fuc5[flights.csv-airports.csv-expected0] PASSED                                                                              [100%]
#
# ======================================================================= warnings summary =======================================================================
# ..\..\..\..\..\..\anaconda3\lib\site-packages\pyreadline\py3k_compat.py:8
#   C:\Users\Tarsampaji\anaconda3\lib\site-packages\pyreadline\py3k_compat.py:8: DeprecationWarning: Using or importing the ABCs from 'collections' instead of from
#  'collections.abc' is deprecated since Python 3.3, and in 3.9 it will stop working
#     return isinstance(x, collections.Callable)
#
# -- Docs: https://docs.pytest.org/en/stable/warnings.html
# ================================================================= 5 passed, 1 warning in 7.57s =================================================================

