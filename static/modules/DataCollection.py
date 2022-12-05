#!/bin/python3

# Builtin Imports.
import sqlite3
import logging
from datetime import datetime

# Cryptocurrency API.
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest

# Stock API.
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest

# API timedate references.
from alpaca.data.timeframe import TimeFrame


class CredentialError(Exception):
  """ Calls exception if valid credentials
  are not given. """
  pass


def DataCollection( database: str,
                    logfile: str,
                    loglevel: int,
                    symbols: list,
                    crypto=True,
                    **credentials  ):

  # Set the logging configuration as defined by the caller.
  logging.basicConfig(filename=logfile, encoding='utf-8', level=loglevel)


  # Ensure that credentials are given if using the stocks api.
  try: if not crypto: if not credentials: raise CredentialError

  except CredentialError as error:
    logging.exception("Stock data api requires key and secret.")
    print("Stock data api requires key and secret"); exit()


  # Set up the sqlite3 database connection.
  try:
    connection = sqlite3.connect(database)
    cursor = connection.cursor()

  except Exception as error: logging.exception()


  # Create a table for each symbol.
  for symbol in symbols:
    cursor.execute( f"CREATE TABLE IF NOT EXISTS ? "
                    f"(high REAL, "
                    f"low REAL, "
                    f"open REAL, "
                    f"close REAL, "
                    f"time REAL);",
                    ( symbol, )                      )


  # formatted datetime object going all the way back.
  date = datetime.strptime("2015-12-01", "%Y-%m-%d")


  # Set up the crypto client and formulate the request.
  if crypto:
    client = CryptoHistoricalDataClient()

    parameters = CryptoBarsRequest( symbol_or_symbols=symbols,
                                    timeframe=TimeFrame.Minute,
                                    start=date                  )


  # Set up the stocks client and formulate the request.
  else:
    client = StockHistoricalDataClient( credentials["key"],
                                        credentials["secret"] )

    parameters = StockBarsRequest( symbol_or_symbols=symbols,
                                   timeframe=TimeFrame.Minute,
                                   start=date                  )


  # Retrieve the data from the api.
  try:
    logging.info("Beginning data request.")
    if crypto: data = client.get_crypto_bars(parameters)
    else: data = client.get_stock_bars(parameters)

  except Exception as error: logging.exception()

  logging.info("Data request successful.")


  # Iterate through the results and store them to the db.
  logging.info("Beginning database write.")
  try:
    for symbol in symbols:
      for point in data[symbols]:
        cursor.execute( f"INSERT INTO ? (high,low,open,close,time)"
                        f"VALUES( ?, ?, ?, ?, ? );",
                        ( symbol,
                          point.high,
                          point.low,
                          point.open,
                          point.close,
                          datetime.timestamp(point.timestamp) )     )

        connection.commit()

  except Exception as error: logging.exception()
