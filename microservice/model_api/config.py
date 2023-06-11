# -*- coding: utf-8 -*-
"""
.. module:: <>.config
   :synopsis: Classes to manage the configuration of different environments (Development, Staging, Production)
              Edit the class attributes depending on the environment
.. moduleauthor:: (C) <grp or enterprise> - <author> 2022
"""
from logging import ERROR, INFO, DEBUG as DEBUG_LOGGING

from constants import ColName


class Config:
    """
    Base class which the rest of configs inherit from.
    Use it for parameters that are the same in all configurations or by default values.

    :param str HOST: host to call the app. By default '0.0.0.0' will listen on all IPs of
    the network, this can be used in this project because AKS (https://docs.microsoft.com/en-us/azure/aks/) manages
    all the traffic and this micro-service is configure to not be accessible by public IPs.
    :type HOST: str

    :param PORT: port to listen from. By default the app uses port 80
    :type PORT: int
    """
    DEBUG = False
    TESTING = False
    LOGGER_LEVEL = INFO


class ProductionConfig(Config):
    """
    Extended class of :class:`Config` to manage Production Environment Configuration
    """
    LOGGER_LEVEL = ERROR
    ENV = 'production'


class StagingConfig(Config):
    """
    Extended class of :class:`Config` to manage Staging Environment Configuration
    """

    # Valid values for flask config.ENV are only development and production
    # But this value was used to create a different configuration than development
    # DevelopmentConfig has different TESTING and DEBUG parameters
    ENV = 'staging'


class DevelopmentConfig(Config):
    """
    Extended class of :class:`Config` to manage Development Environment Configuration
    """
    ENV = 'development'
    TESTING = True
    DEBUG = True
    LOGGER_LEVEL = DEBUG_LOGGING
