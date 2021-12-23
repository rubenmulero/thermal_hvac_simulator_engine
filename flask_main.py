#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This is a flask based rest API to make available the current simulation engine to external calls.

Useful to share the code and make some current simulation options available


@author: Rubén Mulero

"""

from api.endpoints import app as application

# main execution
if __name__ == '__main__':
    # Run the application
    application.run(debug=True, host='0.0.0.0')
