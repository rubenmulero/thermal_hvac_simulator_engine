# -*- coding: utf-8 -*-

"""
Main class of the Rest API. Here we define endpoints with their functions. Also we define some configuration
for Flask and manage error codes.
"""

import logging
import arrow
from functools import wraps
from flask import Flask, request, make_response, Response, abort, redirect, url_for, session, flash, jsonify, \
    request_finished, render_template
import numpy as np
from tqdm import tqdm

from api.utilities import Utilities
from simulator.simulator import Simulator
from util.constants import YEAR

__author__ = 'Rubén Mulero'

# Configuration
ACTUAL_API = '0.1'
AVAILABLE_API = '0.1', '0.2', '0.3'
SECRET_KEY = 'JVYfwEc3FbJKiy$SGSgGLAp2ecmUtXRLAXVrcjLXc&ntuNCoYjBGR^D2Pi#xND^!XdX5kivhfpzsC**X*Lb$7Q29hn'
SQLALCHEMY_DATABASE_URI = 'sqlite://'
MAX_LENGHT = 26000000  # in bytes        ~~ 26Mb
# Defining local variables to load exogenous data
PREV_WEATHER_DATA = 'weather_data_2018_minute.csv'
CURRENT_WEATHER_DATA = 'weather_data_2019_minute.csv'
ELECTRICITY_DATA = 'electricity_price_2019.csv'

# Loading the simulation engine
# Stabilising the simulation engine by loading the contextual data. Here you can modify simulation steps.
simulator_engine = Simulator(CURRENT_WEATHER_DATA, PREV_WEATHER_DATA, ELECTRICITY_DATA)

# Create application and load config.
app = Flask(__name__)
app.config.from_object(__name__)

# TOOD --> you are going to make a class instance and then recover the DB object to manipulate DB
# db = SQLAlchemy(app)

###################################################################################################
###################################################################################################
######                              WRAPPERS
###################################################################################################
###################################################################################################

def limit_content_length(max_length):
    """
    This is a decorator method that checks if the user is sending too long data. The idea is to have some control
    over user's POST data to avoid server overload.
    If user sends data that is too long this method makes an error code 413
    :param string max_length: The maximum length of the requested data in bytes
    :return: decorator if all is ok or an error code 413 if data is too long
    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            cl = request.content_length
            if cl is not None and cl > max_length:
                logging.error("The users sends a too large request data to the server")
                abort(413)
            return f(*args, **kwargs)

        return wrapper

    return decorator


###################################################################################################
###################################################################################################
######                              SIGNALS
###################################################################################################
###################################################################################################

@app.after_request
def after_request(response):
    """
    This signal is used to write information in the INFO log
    :param response: The needed information
    :return: The response instance
    """
    # If the action is succesfull we write into INFO log file
    route = request.url_rule and request.url_rule.endpoint or "No route provided"
    method = request.method or "No method provided"
    ip = request.remote_addr or "No IP provided"
    agent = request.user_agent.string or "No user_agent provided"
    status = response.status or "No Status provided"
    data = response.data or "No data provided"
    # Writing into log file
    app.logger.info("%s - %s - %s- %s - %s - %s" % (ip, agent, method, route, status, data))
    return response



###################################################################################################
###################################################################################################
######                              Error handlers
###################################################################################################
###################################################################################################

@app.errorhandler(500)
def data_sent_error(error):
    resp = make_response("Data entered is invalid, please check your JSON\n", 500)
    return resp


@app.errorhandler(400)
def data_sent_error(error):
    resp = make_response("You have sent a bad request. If your request contains a JSON based structure"
                         "check it might be bad formatted.", 400)
    return resp


@app.errorhandler(413)
def data_sent_too_long(error):
    msg = "Data entered is too long, please send data with max length of %d bytes \n" % MAX_LENGHT
    resp = make_response(msg, 413)
    return resp


###################################################################################################
###################################################################################################
######                              GET FUNCTIONS
###################################################################################################
###################################################################################################


@app.route('/')
def index():
    """
    Redirect to the latest  API version
    :return: Redirect to the latest api version
    """
    logging.info("Redirection to last api version.....")
    return redirect(url_for('api', version=app.config['ACTUAL_API']))


@app.route('/api')
def api_redirect():
    """
    Redirect to the latest API version
    :return: Redirection to the current api version
    """
    logging.info("Redirection to last api version.....")
    return redirect(url_for('api', version=app.config['ACTUAL_API']))


@app.route('/api/<version>')
def api(version=app.config['ACTUAL_API']):
    """
    This is our main page.
    :param basestring version: Api version
    :return: Render with the index page of the API
    """
    if Utilities.check_version(app, version):
        # Loading main page of the APi
        return render_template('index.html')
    else:
        return "You have entered an invalid api version", 404



###################################################################################################
###################################################################################################
######                              POST functions
###################################################################################################
###################################################################################################


@app.route('/api/<version>/train', methods=['POST'])
@limit_content_length(MAX_LENGHT)
def train(version=app.config['ACTUAL_API']):
    """
    " Performs a complete training using the simulation environment. The data sent by the requester must follow
    the following format.

    {
        "action": [0,1,0,1,0,1,0,1,0,1,0,..…], # ← AI actions to be taken...
        “datetime_start”: “2020-03-23” #
        “datetime_end”: “2020-04-23” #
        "simulation_steps": 60 # Optionally change time between steps
    }

    Return data is:

    {
        "t_i": [20.0, 21.0, 23.0,...],
        "t_s": [21.0, 23.0, ..], # ← These are important values!!!
        "t_a": [23.0, 24.0, 25.0, …],
        "date": ["2020-01-01 00:05", …],
        “GHI” : [1.2, 23.3, 23.4, ...]
    }

    """

    res = {
        'status': False,
        'msg': None
    }

    #TODO --> follow this guide to upload files: https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/

    if Utilities.check_connection(app, version):
        # We created a list of Python dict.
        data = request.json
        msg = Utilities.check_train(data)
        if data and not msg:
            logging.info("Training data is correct..")
            actions = data.get('action', None)
            # todo Limit this part to few iterations.
            date = arrow.get(data['datetime_end']) if data.get('datetime_end', None) else None
            # TODO --> trampa, intenta usar la constructora de la clase
            max_simulated_steps = simulator_engine._get_simulator_timesteps(YEAR, date)
            print("Total timesteps to simulate: {timesteps}".format(timesteps=max_simulated_steps))
            # TODO --> get_timestep based on the current date. The idea is to set the simulator timestamp to the desired place.

            # Check if the simulated steps are the same as the sent actions before starting the simulation process..
            if len(actions) == max_simulated_steps:
                simulator_engine.reset_simulator()
                simulation_results = list()
                for i in tqdm(range(0, max_simulated_steps)):
                    action = actions[i]
                    data = simulator_engine.simulate_step(action, 50.0)
                    # Change the data to fit with the original simulation engine
                    t_s, t_h, t_i, t_e = data[0]
                    t_a = data[1]
                    i_s = data[3]
                    date = simulator_engine.get_current_timestamp()
                    # Insert into a dict
                    results_dict = {
                        "t_i": t_i,
                        "t_s": t_s,
                        "t_a": t_a,
                        "date": date.format(),
                        "GHI": i_s
                    }
                    # Appending to the final list of results
                    simulation_results.append(results_dict)
                current_timestep = simulator_engine.get_timestep()
                print("Current timestep is: {timestep_done}".format(timestep_done=current_timestep))
                if current_timestep == len(simulation_results):
                    # The entire simulation process is correct, we will send back the results.
                    res['status'] = True
                    res['msg'] = "Simulation done successfully, check data for further analisis"
                    res['data'] = simulation_results
                else:
                    res['msg'] = "The call and sent data was OK, but something happened in the simulation process and " \
                                 "data is not correct"
                return jsonify(res), 200
            else:
                res['msg'] = "The given simulation actions has no the same length as the simulation data. " \
                             "Given simulation actions: {n_actions}; " \
                             "Given simulation steps: {simulation_steps}".format(n_actions=len(data['action']),
                                                                                 simulation_steps=max_simulated_steps)
                return jsonify(res), 400
        else:
            logging.error("train: there is a problem with entered data")
            # Data is not valid, sending a message containing the information.
            # Standard Error
            res['msg'] = "The send data format is not correct, please check it"
            return jsonify(res), 400
    else:
        # Something is wrong in the call
        res['msg'] = "You send an incorrect API version or your Content-type is not JSON serializable "
        return jsonify(res), 400
