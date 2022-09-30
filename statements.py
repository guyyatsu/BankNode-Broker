from constants import *

sql_queries = {

  # Compares a given string to the username column in the credentials table.
  "Select Username": "SELECT username FROM credentials WHERE username=?;",

  # Select the given users password hash.
  "Select Password": "SELECT password FROM credentials WHERE username=?;",

  # Selects the users exchange key and secret.
  "Market Key/Secret": "SELECT key,secret FROM credentials WHERE username=?;",

  # Creates a table named 'credentials' in a given database if it doesn't already exist.
  "Create Credentials Table": (
    f"CREATE TABLE IF NOT EXISTS credentials("
        f"username TEXT, "
        f"password TEXT, "
        f"key BYTES, "
        f"secret BYTES"
    f")"
  ),

  # Enter a new row in the credentials table.
  "Enter New Credentials": (
    f"INSERT INTO credentials("
    f"username,password,key,secret"
    f") "
    f"VALUES ( ?, ?, ?, ? );"
  ),

  # Check for table name in master record.
  "Check Table Existence": (
    f"SELECT name FROM sqlite_master WHERE type='table' AND name=?;"
  ),

  # Record a transaction to the ledger.
  "Ledge Transaction": (
    f"INSERT INTO ledger("
      f"time,id,symbol,type,side,cost,share,price,"
  ),

}


logging_statements = {

  # Blank timestamp
  "": f"{timestamp}",

  # Check whether or not the user exits within the database.
  "Check User Existence": f"{timestamp}Validating user existence",

  # Confirm users existence.
  "Confirm User": f"{timestamp}User exists.",

  # Deny uers existence.
  "Deny User": f"{timestamp}User does not exist.",

  # Check password.
  "Check Password": f"{timestamp}Validating password...",

  # Confirm password.
  "Confirm Passwword": f"{timestamp}Password accepted.",

  # Deny password.
  "Deny Passwword": f"{timestamp}Password denied.",

  # Connect to the database.
  "Database Connection": f"{timestamp}Attempting connection to database",

  # Disconnect from the database.
  "Database Disconnect": f"{timestamp}Closing database connection.",

  # Connection succeeds;
  "Database Connection Success": f"{timestamp}Connection succeeded.",

  # Connection fails;
  "Database Connection Error": f"{timestamp}Connection failed! Stack Trace",

  # Query execution:
  "Query Execution": f"{timestamp}Attempting SQL Query",

  # Query Success:
  "Query Success": f"{timestamp}Query Success!",

  # Query Failure:
  "Query Failure": f"{timestamp}Query Failure!",
}
