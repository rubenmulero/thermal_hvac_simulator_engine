"""
This is CSV parser to  check and load data in a pandas Dataframe format.


"""

import csv

from pathlib import Path
import pandas as pd

from util.logger import LoggingClass

logger = LoggingClass('context_data').get_logger()


class CSVParser:

    def __init__(self, p_path):
        self.path = Path(p_path)

    def parse_data(self, p_file, p_datetime_format=None):
        """
        Using the provided file, this method loads its contents in a pandas object

        :param p_file: The name of the file to load
        :param p_datetime_format: If the csv file contains date in the first column, insert the format to parse it into
                    date values.

        :return: A pandas object with the loaded data or None if nothing detected
        """
        data = None
        if self._is_csv(p_file):
            # Loading file using pandas
            logger.info("Valid CSV file found, loading it")
            csv_file = self.path / p_file
            if p_datetime_format:
                # Parsing datetime field to date type
                data = pd.read_csv(str(csv_file), parse_dates=[0],
                                   infer_datetime_format=p_datetime_format, index_col=[0])
            else:
                # Regular loading
                data = pd.read_csv(str(csv_file))
            # Checking if NaN values are present and making a linear interpolation if necessary.
            if data.isnull().values.any():
                print("NaN values detected in {file}, doing a linear interpolation to fill it.".format(file=p_file))
                logger.info("NaN values detected in {file}, doing a linear interpolation to fill it.".format(file=p_file))
                data = data.interpolate()

        return data

    def _is_csv(self, p_file):
        """
        Checks if the current loaded file is a CSV file.

        :param p_file: A file name
        :return: True if it is a CSV file, False otherwise.
        """
        res = False
        if self._check_file(p_file):
            # Seems to be a valid file, checking extension
            if p_file.endswith('.csv'):
                res = True
        return res

    def _check_file(self, p_file):
        """
        This method checks if the provided file exist or not in the system

        :param p_file: A file name
        :return: True if the file exists in the current path, False otherwise
        """
        res = False
        if self._check_path():
            my_file = self.path / p_file
            if my_file.is_file():
                # File exists
                res = True
            else:
                print("The provided file do not exist in the system: {path}".format(path=my_file))
                logger.warning("The provided file do not exist in the system: {path}".format(path=my_file))
        return res

    def _check_path(self):
        """
        This method checks if the provided path in the constructor exist or not in the system

        :return: True if it is a path, else False
        """
        res = False
        if self.path.is_dir():
            res = True
        else:
            print("The provided path do not exist in the system: {path}".format(path=self.path))
            logger.warning("The provided path do not exist in the system: {path}".format(path=self.path))
        return res
