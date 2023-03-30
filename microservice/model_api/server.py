"""
.. module:: <x>.server
   :synopsis: script with the main behaviour of the API and the views
    ::views::
        :view ping_db: host:port/ping_db - to check if there is connection to the db from
                        the microservice
        :view ping: host:port/ping - to check if the microservice itself is up and running

.. moduleauthor:: (C) <group - enterprise> - <user> 2022
"""
import logging
import traceback

from pyodbc import Connection

from flask import Flask, jsonify

from interface_data_base import InterfaceDataBase
from constants import ColName

app = Flask(__name__, instance_relative_config=True)

def get_logger(level: int = logging.INFO) -> logging.Logger:
    """
    Method to get the logger of the flask application

    :param level: level which will show the logs
    :return:
    :rtype: logging.Logger
    """
    # remove current handler to add new format
    for hdl in app.logger.handlers[:]:
        if isinstance(hdl, logging.StreamHandler):
            app.logger.removeHandler(hdl)

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    app.logger.addHandler(handler)

    app.logger.setLevel(level)
    app.logger.propagate = False

    return app.logger


def get_json_credentials(server_app):
    """
    Method to extract the credentials from the database

    :param server_app:
    :return: dict with credentials needed to connecto to db
    """
    return {
        ColName.DATA_BASE: server_app.config['DB_NAME'],
        ColName.SERVER: server_app.config['DB_SERVER'],
        ColName.DRIVER: server_app.config['DB_DRIVER'],
        ColName.USER: server_app.config['DB_USER'],
        ColName.PASS: server_app.config['DB_PASS'],
        ColName.PORT: "",
        ColName.SCHEMA: server_app.config['DB_SCHEMA'],
    }



def get_connection_db(_app) -> Connection:
    """
    Method to get a conenction to the db

    :param _app:
    :return: pyodbc.Connection
    """
    cnxn = get_interface_db(_app=_app)
    cnxn = cnxn.connection
    return cnxn


def get_interface_db(_app, logger: logging.Logger = None) -> InterfaceDataBase:
    """
    Method to get a InterfaceDataBase instance with connection to the db

    :rtype: InterfaceDataBase
    """
    credentials: dict = get_json_credentials(server_app=_app)
    interface = InterfaceDataBase(credentials=credentials, logger=logger)

    try:
        interface.establish_connection()

    except ConnectionError as exc:
        raise exc
    except Exception as exc:
        raise exc
    # ConnectionError(f'Cannot connect to database. \n Further details: \n {exc}')

    return interface


@app.get("/pingDB")
def ping_db():
    """
    Method to test if there is connection to the db

    :return:
    """
    try:
        if get_connection_db(_app=app) is None:
            credent = get_json_credentials(server_app=app)

            del credent['Pass']

            return str(f"Cannot connect to internal DB. Using credentials: \n{credent} (Password not shown) "
                       + f"\n {traceback.format_exc()}"), 404
        else:
            return "Connection with db succeded", 200

    except Exception as exc:
        return f"Errors trying to connect to DB: \n{exc} \n {traceback.format_exc()}", 404


@app.get("/ping")
@app.get("/")
def ping():
    """
    Method to check if the service is up, running and reachable

    :return:
    """
    return "Service ON!", 200


# e.g. /main/id1=1;id2=1;id3="2"
@app.get(
    "/main/id1=<int:id_1>;id2=<int:id_2>;id3=<id_3>")
def main_request(id_1: int, id_2: int, id_3: str):
    """
    Main method to execute the main reque

    :param id_1:
    :type id_1: int

    :param id_2:
    :type id_2: int

    :param id_3:
    :type id_3: str

    :returns: <X>
    """
    logger = get_logger(level=app.config['LOGGER_LEVEL'])

    try:
        logger.info(f'Received request: simId={id_1};projId={id_2};projVersion={id_3}')

        status, exc = 200, ""

        if exc == "" and status == 200:
            return "Success!", status
        else:
            raise exc

    except ConnectionError as err:
        message = f'{str(err)} \n {traceback.format_exc()}'
        status = 404
        logger.exception(err)

    except Exception as err:
        message = f'An unexpected error occurred please contact your administrator.\n For more details explore: {err}'
        status = 400
        logger.exception(f'Unexpected error: {err}\n{traceback.format_exc()}')

    response = ""
    return jsonify(response), status
