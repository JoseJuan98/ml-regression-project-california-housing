# -*- coding: utf-8 -*-
"""
.. module:: <>.app
   :synopsis: Script to start the Flask service.

.. moduleauthor:: (C) <grp or company> - <author> 2022
"""

# API actions
from endpoint import app
from microservice.model_api.model_utils import get_logger

from logging import INFO

if __name__ == "__main__":

    # Define logger level
    logger = get_logger(level=INFO)

    fenv = app.config['ENV']

    logger.info(f'\t-> Starting Service using environment {fenv}')
    if fenv == 'staging':
        app.config.from_object("config.StagingConfig")

    elif fenv == 'production':
        app.config.from_object("config.ProductionConfig")

    elif fenv == 'development':
        app.config.from_object("config.DevelopmentConfig")

    else:
        logger.exception(Exception(f'Invalid FLASK_ENV {fenv}'))

    del fenv

    print(f"Using db {app.config['DB_NAME']} from Server {app.config['DB_SERVER']}" +
          f" with driver {app.config['DB_DRIVER']}")

    app.run(host=str(app.config['HOST']), port=int(app.config['PORT']))
