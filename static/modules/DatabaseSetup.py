import sqlite3


def SetupCredentialsDatabase(database):
  connection = sqlite3.connection(database)
  cursor = connection.cursor()
  cursor.execute( f"CREATE TABLE IF NOT EXISTS credentials "
                  f"(username TEXT,"
                  f"password TEXT,"
                  f"alpaca BLOB)"                            )

  return connection.commit()