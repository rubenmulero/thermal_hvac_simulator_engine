"""
This file will be used to store data in a database, or CSV files.

Data will be received in a Python like dict and store it.

"""

import os
import csv
import json

from util.logger import LoggingClass


logger = LoggingClass('weather_api').get_logger()


def save_to_csv(p_data, p_path):
    """
    By giving data and a destination path, this method stores the obtained data in a CSV file format.

    :param p_data: a Python list of dicts
    :return: True or False
    """
    keys = p_data[0].keys()
    with open(p_path, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(p_data)

    print("Data stored ok")
