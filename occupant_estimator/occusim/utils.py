#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This file contains different utility classes to be used as a resource in certain moments of the calculation process

"""

import csv
import datetime
import pandas as pd
import numpy as np


def get_hours_in_year(year):
    """
    Get number of hours for a given year
    :param year: year to get amount of days from
    :return: amount of days in a year
    :rtype: int
    """
    days_in_year = (datetime.datetime(year+1, 1, 1) - datetime.datetime(year, 1, 1)).days
    hours_in_year = 24*days_in_year
    return hours_in_year


def get_dates_from_year(year):
    """
    creates date range for the year of the calculation.
    It returns a data_range in pandas format in hourly intervals from Jan01 00:00 to Dec31 23:55

    :param year: year of first row in weather file
    :type year: int
    :return: pd.date_range with 8760 values taken by HOURS_IN_YEAR constant
    :rtype: pandas.data_range
    """
    return pd.date_range(str(year) + '/01/01', periods=get_hours_in_year(year), freq='H')


def join_distributions(profiles):
    """
    Creates a unique vector of the distributed values given by the profiles dict.

    :param profiles: A python dict containing the distribution of probabilities by day of the week.
    :return: A uniqe numpy array containing the vector of probabilities
    """
    general_distribution = []
    for key in ['WEEKDAY', 'SATURDAY', 'SUNDAY']:
        general_distribution.extend(profiles[key])
    return np.array(general_distribution)

"""
Example :

/data/OFFICE.csv

METADATA	CH-SIA-2014	OFFICE										
MONTHLY_MULTIPLIER	0.8	0.8	0.8	0.8	0.8	0.8	0.8	0.8	0.8	0.8	0.8	0.8
DAY	HOUR	OCCUPANCY	APPLIANCES	LIGHTING	WATER	HEATING	COOLING	PROCESSES	SERVERS	ELECTROMOBILITY		
WEEKDAY	1	0.0	0.1	0.1	0.0	SETBACK	OFF	0.0	0.0	0.0		
WEEKDAY	2	0.0	0.1	0.1	0.0	SETBACK	OFF	0.0	0.0	0.0		
WEEKDAY	3	0.0	0.1	0.1	0.0	SETBACK	OFF	0.0	0.0	0.0		
WEEKDAY	4	0.0	0.1	0.1	0.0	SETBACK	OFF	0.0	0.0	0.0		
WEEKDAY	5	0.0	0.1	0.1	0.0	SETBACK	OFF	0.0	0.0	0.0		
WEEKDAY	6	0.0	0.1	0.1	0.0	SETBACK	OFF	0.0	0.0	0.0		

"""


def read_cea_schedule(path_to_cea_schedule):
    """
    reader for the files ``locator.get_building_weekly_schedules``

    :param str path_to_cea_schedule: path to the cea schedule file to read.
                                     (E.g. inputs/building-properties/schedules/B001.csv)
    :return: schedule data, schedule complementary data
    :rtype a list of python dicts.
    """

    with open(path_to_cea_schedule) as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i == 0:
                metadata = row[1]
            elif i == 1:
                monthly_multiplier = [round(float(x), 2) for x in row[1:]]
            else:
                # skip all the other rows
                break

    schedule_data = pd.read_csv(path_to_cea_schedule, skiprows=2).T
    schedule_data = dict(zip(schedule_data.index, schedule_data.values))
    schedule_complementary_data = {'METADATA': metadata, 'MONTHLY_MULTIPLIER': monthly_multiplier}

    return schedule_data, schedule_complementary_data
