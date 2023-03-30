"""
.. module:: <>.interface_data_base
   :synopsis: class containing the logic to work with the database

.. moduleauthor:: (C) <> - <> 2022
"""

import logging
from typing import Union, Tuple

from pyodbc import connect, Connection, Cursor

from constants import ColName

import json

_logger = logging.getLogger(__name__)


def execute_query(query: str, params: Union[tuple, None, str],
                  cursor: Cursor,
                  logger: logging.Logger = None
                  ) -> Union[Tuple[int, Union[str, Exception]]]:
    try:
        if params is None:
            cursor.execute(query)
        else:
            cursor.execute(query, params)
        cursor.commit()

        return 200, ""
    except Exception as e:

        try:
            cursor.close()
        except Exception as exc:
            msg = f'Couldnt close database, probably it was closed before. {exc}'
            if logger is None:
                _logger.exception(msg)
            else:
                logger.exception(msg)
        return 400, Exception(
            f"Something went wrong updating tables GeneratedJSON or Simulation.\n For more details:\n\n {e}")


class InterfaceDataBase(object):
    """
    This class converts data format between input and output

            *Attributes* :

                *connection* :
                ``pyodbc connection to the SQL server database``

                *credentials* :
                ```Dictionary that contain the credentials to connect to the database``

            *Methods* :

                *establish_connection* :
                ``This method establish the connection to the SQLServer database.``

                *update_table* :
                ``This method update table in database.``

                *close_connection* :
                ``This method closes the connection to the database.``
    """

    # The code (int number) depends on the db values
    status_codes = {"Sucess": 3,
                    "a": 4,
                    "b": 5,
                    "Failed": 6,
                    "Aborted": 7}

    def __init__(self, credentials: dict, logger: logging.Logger = None) -> None:
        self.connection: Union[Connection, None] = None
        self.credentials = credentials

        if logger is None:
            self.logger = _logger
        else:
            self.logger = logger

    def establish_connection(self):
        """
        This method establish the connection to the SQLServer database.
        """

        # MSSQL Server Connection
        sql_conn_str_auth = str('DRIVER={driver};SERVER={server};DATABASE={db}' +
                                ';UID={user};PWD={passw};').format(
            driver=self.credentials[ColName.DRIVER],
            server=self.credentials[ColName.SERVER],
            db=self.credentials[ColName.DATA_BASE],
            user=self.credentials[ColName.USER],
            passw=self.credentials[ColName.PASS])

        # Other params that could be needed
        # + f'PORT={self.credentials[ColName.PORT]};')
        # Trusted_Connection=yes;

        self.logger.info(f'\tEstablishing connexion with server:{self.credentials[ColName.SERVER]}...')
        self.connection = connect(sql_conn_str_auth)

        return self

    def update_table(self, status: int, id: int, table: str = '<>', cursor: Cursor = None):

        if cursor is None:
            if self.connection is None:
                self.establish_connection()
            cursor = self.connection.cursor()

        # Updating Simulation table
        query: str = """
                        UPDATE dbo.{table}
                        SET status= {status}, date=GETDATE()
                        WHERE id = {id};
                     """.format(status=status, table=table, id=id)

        execute_query(query=query, params=None, cursor=cursor)

    def upload_json(self, response_json: dict, id: int,
                    table: str = '<>'):
        """
        ``This method write in database.``

        """
        try:
            if response_json is None:
                raise Exception('Empty json response')

            if self.connection is None:
                self.establish_connection()

            cursor = self.connection.cursor()

            status = self.status_codes[response_json['Status']]

            # Insert response_json into json table
            json_response = json.dumps(response_json)

            query = """
                        INSERT dbo.{table}
                        (id, date, jsonFile)
                        VALUES ({id}, GETDATE(), ?);
                    """.format(table=table, id=id)

            execute_query(query=query, params=(json_response), cursor=cursor)

            # Updating table with the execution status
            cursor = self.connection.cursor()
            self.update_table(status=status, table=table, cursor=cursor, id=id)

            return 200, ""
        except Exception as e:
            return 400, e

    def close_connection(self):
        """
        ``This method closes the connection to the database.``
        """
        self.connection.close()

    def __del__(self):
        """
        ``del behaviour``
        """
        self.logger.info('\t Closing connection to db.')
        if self.connection is not None:
            if not self.connection.closed:
                try:
                    self.connection.close()
                except Exception as exc:
                    self.logger.debug(f'{exc}')
