# -*- coding: utf-8 -*-

"""
This is a set of utilities to validate the acquired data and test if the user is doing the required actions
"""

import logging
import arrow
from collections import Counter
from flask import abort, session, request, jsonify
from jsonschema import validate, ValidationError, FormatChecker


class Utilities(object):

    @staticmethod
    def check_connection(app, p_ver):
        """
        Make a full check of all needed data

        :param app: Flask application
        :param p_ver: Actual version of the API

        :return: True if everithing is OK.
                An error code (abort) if something is bad
        """
        # Check if the Api level is ok
        if Utilities.check_version(app=app, p_ver=p_ver):
            # check if the content type is JSON
            if Utilities.check_content_type():
                return True
            else:
                logging.error("check_connection: Content-type is not JSON serializable, 400")
                abort(400)
        else:
            logging.error("check_connection, Actual API is WRONG, 404")
            abort(404)

    @staticmethod
    def check_content_type():
        """
        Checks if actual content_type is OK

        :return: True if everything is ok.
                False if something is wrong
        """
        content_type_ok = False
        # Check if request headers are ok
        if request.headers['content-type'] == 'application/json':
            content_type_ok = True
        return content_type_ok

    @staticmethod
    def check_version(app, p_ver):
        """
        Check if we are using a good api version

        :param app: Flask application
        :param p_ver: API version

        :return:  True or False if api used is ok.
        """
        api_good_version = False
        if p_ver in app.config['AVAILABLE_API']:
            api_good_version = True
        return api_good_version

    @staticmethod
    def check_train(p_data):
        """
        Check if the received data follows the required JSON schema to validate it

        :param p_data The data to be checked.

        :return a MSG containing the result of the current check
        """
        msg = None
        schema = {
            "title": "train method schema",
            "type": "object",
            "properties": {
                "action": {
                    "description": "action values to send into the simulator",
                    "type": "array",
                    "uniqueItems": False,
                    "items": {
                        "type": "integer",
                        "minimum": 0,
                        "maximum": 1
                    }
                },
                "datetime_start": {
                    "description": "The start date of the simulation process",
                    "type": "string",
                    "format": "date",
                },
                "datetime_end": {
                    "description": "The end date of the simulation process",
                    "type": "string",
                    "format": "date",
                },
                "simulation_steps": {
                    "description": "Time gap between simulation steps",
                    "type": "integer",
                    "minimum": 10,
                    "maximum": 190
                }
            },
            "required": ["action", "datetime_start", "datetime_end"],
            "additionalProperties": False,
        }

        # Perform the validation process
        try:
            validate(p_data, schema, format_checker=FormatChecker())
            # If we are at this point is because everything is ok. Checking the given datetime
            start_time = p_data['datetime_start']
            end_time = p_data['datetime_end']
            if start_time > end_time:
                raise ValidationError("Start time can't be greater than end time.")
        except ValidationError as e:
            logging.error("The schema entered by the user is invalid")
            msg = e.message
        return msg
