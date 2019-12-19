import os
import json
import subprocess
import psycopg2
import psycopg2.extras
from logger import logger
import random as rn


class Connector:
  def __init__(self, dbConfig):
    self._dbConfig = dbConfig

  def establishConnection(self):
    try:
      return psycopg2.connect(
          dbname=self._dbConfig["dbName"],
          user=self._dbConfig["user"],
          password=self._dbConfig["password"],
          host=self._dbConfig["host"],
          port=self._dbConfig["port"]
      )
    except psycopg2.Error as e:
      if str(e.pgerror) != 'None':
        logger.info(e.pgerror)
        logger.info(e.diag.message_detail)
        raise ValueError()

  def closeConnection(self, connection):
    connection.close()

  def query(self, query):
    try:
      # open connection per query
      conn = self.establishConnection()
      conn.autocommit = True
      # The cursor
      cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
      cur.execute(query)
      result = [dict(record) for record in cur]
    except psycopg2.Error as e:
      if str(e.pgerror) != 'None':
        logger.info(e.pgerror)
        logger.info(e.diag.message_detail)
      else:
        logger.info("transaction success")

    finally:
      # close connection
      cur.close()
      conn.close()
    return result
