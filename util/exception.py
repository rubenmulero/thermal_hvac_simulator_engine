#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This file contains different custom exceptions to raise it if for some reason my program has an specific error.
The idea is to detect some problems in the calculations and create their own error exception system.


@author: Rubén Mulero
"""

from util.logger import LoggingClass

logger = LoggingClass('exceptions').get_logger()


class TemperatureValidationError(Exception):
    """
    This class is intented to raise an exception when the given temperatures in the model are not correct or are
    out of range in the specific standards.

    """
    def __init__(self, message, errors):
        super().__init__(message)
        # Extra parameters
        self.errors = errors
        print('Printing Errors:')
        print(errors)
        # Saving into exceptions logging
        logger.error(message + " " + str(errors))
