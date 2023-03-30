# -*- coding: utf-8 -*-
"""
.. module:: <>.config
   :synopsis: Classes to manage the configuration of different environments (Development, Staging, Production)
              Edit the class attributes depending on the environment
.. moduleauthor:: (C) <grp or enterprise> - <author> 2022
"""
from logging import INFO, DEBUG as DEBUG_LOGGING

from constants import ColName

class Config:
    """
    Base class which the rest of configs inherit from.
    Use it for parameters that are the same in all configurations.

    :param DB_DRIVER: sql client driver used by the library pyodbc. To check avalaible
        drivers check https://wiki.python.org/moin/ODBCDrivers
        By default '{ODBC Driver 17 for SQL Server}', up-to-date driver, older
        ones can cause problems because the don't support JSON files as strings
        insertions.
    :type DB_DRIVER: str

    :param str HOST: host to call the app. By default '0.0.0.0' will listen on all IPs of
    the network, this can be used in this project because AKS (https://docs.microsoft.com/en-us/azure/aks/) manages
    all the traffic and this micro-service is configure to not be accessible by public IPs.
    :type HOST: str

    :param PORT: port to listen from. By default the app uses port 80
    :type PORT: int
    """
    DB_DRIVER = '{ODBC Driver 17 for SQL Server}'
    HOST = '0.0.0.0'
    PORT = 80
    DB_SCHEMA = "dbo"
    DEBUG = False
    TESTING = False
    DB_NAME = None
    DB_SERVER = None
    DB_USER = None
    DB_PASS = None
    LOGGER_LEVEL = INFO


class ProductionConfig(Config):
    """
    Extended class of :class:`Config` to manage Production Environment Configuration
    """
    DB_NAME = ""
    DB_SERVER = ".database.windows.net"
    DB_USER = ""
    DB_PASS = ""

    # FIXME
    DEBUG = True
    TESTING = True
    ENV = 'development'


class StagingConfig(Config):
    """
    Extended class of :class:`Config` to manage Staging Environment Configuration
    """
    DB_NAME = ""
    DB_SERVER = ""
    DB_USER = ""
    DB_PASS = ""

    # Valid values for flask config.ENV are only development and production
    # But this value was used to create a different configuration than development
    # DevelopmentConfig has different TESTING and DEBUG parameters
    ENV = 'development'


class DevelopmentConfig(Config):
    """
    Extended class of :class:`Config` to manage Development Environment Configuration
    """
    TESTING = True
    DEBUG = True
    LOGGER_LEVEL = DEBUG_LOGGING
    DB_NAME = ""
    DB_SERVER = ""
    DB_USER = ""
    DB_PASS = ""
