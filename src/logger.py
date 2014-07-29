#-*-coding:utf-8-*-
from etc.settings import *
from logging.handlers import RotatingFileHandler
import logging
from os import path

fileHandler = RotatingFileHandler(path.join(LOG_DIRECTORY,log_file_name),maxBytes=LOG_SIZE,backupCount=100)
fileHandler.setFormatter(logging.Formatter(LOG_FORMAT,datefmt=LOG_DATE_FORMAT))
logger = logging.getLogger('aramonitor')
logger.setLevel(logging.DEBUG)
logger.addHandler(fileHandler)

def log(msg) :
    logger.info(msg)
    if DEBUG:print msg

def log_error(msg) :
    logger.error(msg)
    if DEBUG:print msg
