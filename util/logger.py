
"""
This is an additional file which contains some utilities, like logging engine, threading specifications and so on.

"""

import logging
import os
import pathlib


from logging.handlers import SMTPHandler


ADMINS = ['ruben.mulero@tecnalia.com']


LOG_FOLDER = str(pathlib.Path(__file__).parent.absolute()) + '/../logs'

class LoggingClass:
    """
    This class is used to rotate the information from STDOUT to a real file with  a given name.

    This class also includes a handler to send emails to the application administrators in order to inform about
    potential errors in the system.

    """

    def __init__(self, p_file_name):
        self.logger = logging.getLogger(p_file_name)
        self.logger.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        if not os.path.exists(LOG_FOLDER):
            os.makedirs(LOG_FOLDER)
        log_file = LOG_FOLDER + '/{file_name}.log'.format(file_name=p_file_name)
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.DEBUG)
        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # add the handlers to the logger
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

        # Configure the Mail handler.
        mail_handler = SMTPHandler(mailhost=('172.26.150.152', 465),
                                   fromaddr='nubio@tecnalia.com',
                                   toaddrs=ADMINS, subject='YourApplication Failed',
                                   credentials=('nubio@tecnalia.com', 'fC5174$2'))
        mail_handler.setLevel(logging.ERROR)
        self.logger.addHandler(mail_handler)

    def get_logger(self):
        return self.logger
