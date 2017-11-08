import os
import tempfile
import logging


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # create file handler which logs info messages
    fh = logging.FileHandler('foo.log', 'w', 'utf-8')
    fh.setLevel(logging.INFO)

    # create console handler with a debug log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # creating a formatter
    formatter = logging.Formatter('- %(name)s - %(levelname)-8s: %(message)s')

    # setting handler format
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger