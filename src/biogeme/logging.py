""" Interface for the use of the loggers in Biogeme

:author: Michel Bierlaire
:date: Thu Mar 23 17:53:22 2023

"""
import logging

DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL


def get_screen_logger(level=WARNING):
    logger = logging.getLogger('biogeme')
    logger.setLevel(DEBUG)
    formatter_debug = logging.Formatter(
        '[%(levelname)s] ' '%(asctime)s ' '%(message)s ' '<%(filename)s:%(lineno)d>'
    )
    formatter_normal = logging.Formatter('%(message)s ')
    formatter = formatter_debug if level == DEBUG else formatter_normal
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def get_file_logger(filename, level=WARNING):
    logger = logging.getLogger('biogeme')
    logger.setLevel(DEBUG)
    formatter = logging.Formatter(
        '[%(levelname)s] ' '%(asctime)s ' '%(message)s ' '<%(filename)s:%(lineno)d>'
    )
    file_handler = logging.FileHandler(filename)
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger