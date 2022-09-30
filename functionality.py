import logging
import sqlite3
from getpass import getpass
import secrets
from base64 import urlsafe_b64encode
import hashlib as hashlib
from cryptography.fernet import Fernet
from constants import *
from statements import sql_queries as sql
from statements import logging_statements as log
from ExchangeAPI import *


logging.basicConfig(filename="./.log", level=logging.DEBUG)

"""
    Logging setup and associated functionality.
"""
if logging.getLogger():

  def INFO(msg: str):
    try: return logging.info(msg)
    except: pass

  def DEBUG(msg: str):
    return logging.debug(msg)

else: pass


def ErrorHandling(error):
  logging.exception("oops: {error}")
  return exit()  


class CryptographyMethods():
  """ A collection of tools specifically dealing with the security
  of certain given credentials.

  One-Way SHA-256 hashes are implemented through self.SHA256()
  Two-Way Fernet encryption is implemented through self.Encryption()
    -- Custom keys are created with self.BuildKey(), which allows
       for the use of an 'imaginary' encr
  """

  def __init__(self):
    self = self 

  def SHA256(self, secret: str):
    """ Create a SHA-256 hash of whatever value is given. """
    return hashlib.sha256(secret.encode()).hexdigest()


  def BuildKey(self, username: str, password: str):
    """ Create a two-way encryption key using the first 32
    digits of the hash of a username and password strings.

        The results are then encoded in urlsafe-base64 bytes
    and returned to thre caller. """
    basecode = self.SHA256(str(username + password))[:32]
    key = urlsafe_b64encode(basecode.encode())
    return key


  def Encryption(self, phrase: bytes, target: str):
    intelligence = Fernet(phrase)
    return intelligence.encrypt(bytes(target, 'utf-8'))
  

  def Decryption(self, phrase: bytes, target: str):
    intelligence = Fernet(phrase)
    return intelligence.decrypt(target)

class Database():
 
  def __init__(self):
    """ Establish a persistent connection to the credential database;
    ensure that the proper tables and headers are present then create a
    pointer if so, and attempt to create them if not.

    Credential Database Tables & Headers

        - credentials
            - username
            - password
            - key
            - secret

        - $user_ledger
            - id
            - timestamp
            - position
            - symbol
            - amount
            - price

        - market
            - high
            - low
            - open
            - close
            - period
    """
    self.db = "./.credentials.db"
    self.crypto = CryptographyMethods()

    try:
      DEBUG(f"{log['Database Connection']}:\n{self.db}\n")
      # Initiate the database connection.
      self.connection = sqlite3.connect(self.db)
      # Create the connection cursor.
      self.cursor = self.connection.cursor()    
  
      DEBUG(f"{log['Database Connection Success']}\n")

      try:# Check for the existence of the 'crednetials' table.
        # Declare our intention;
        DEBUG(f"{log['Query Execution']}:\n{sql['Check Table Existence']}\n")
        # Invoke the statement.
        self.cursor.execute(
          sql['Check Table Existence'],
          ("credentials",)
        )# Call the success.
        DEBUG(f"{log['Query Success']}\n")
      # If we can't check whether the table exists; handle it.
      except Exception as error: ErrorHandling(error)

      # If the table exists, then do nothing.
      if len(self.cursor.fetchall()) > 0: pass
      # Otherwise, attempt to create the table.
      else:
        # Declare our intention;
        DEBUG(f"{log['Query Execution']}:\n{sql['Create Credentials Table']}\n")
        try:
          # Invoke the statement.
          self.cursor.execute(sql['Create Credentials Table'])
          # Call the success.
          DEBUG(f"{log['Query Success']}\n")
          # Save the table and it's headers.
          self.connection.commit()
        # If we can't create the credentials table; handle it.
        except Exception as error: ErrorHandling(error)

    # If we can't connect to the database; handle it.
    except Exception as error: ErrorHandling(error)


  def StoreCredentials(self, username, password, key, secret):    
    """ Add the username and password hash to the database.
    It is assumed that any arguments passed to this function other than
    the credabase are already encrypted. """

    try:# Write new entries to the credentials table.
      DEBUG(f"{log['Query Execution']}:\n{sql['Enter New Credentials']}\n")
      self.cursor.execute(
        sql['Enter New Credentials'],
        (username, password, key, secret)
      )
      DEBUG(f"{log['Query Success']}\n")   
    # If we can't enter new credentials to the table; handle it.
    except Exception as error: ErrorHandling(error)
  
    # Save the addition.
    return self.connection.commit()


  def ValidateCredentials(self, username: str, password: str):
    """ Accepts a username and password and checks for their existence
    within the database. """

    try:# Search for the password within the credentials table.
      # Declare our intention;
      DEBUG(f"{log['Query Execution']}:\n{sql['Select Password']}\n")
      # Invoke the statement.
      self.cursor.execute(sql["Select Password"], (username,))
      # Call the success.
      DEBUG(f"{log['Query Success']}\n")
    # If we can't Find the password within the table, handle it.
    except Exception as error: ErrorHandling(error)
  
    # After approving the user we validate the password.
    logged_password = str(self.cursor.fetchall()[0][0])
  
    # Log the attempt.
    DEBUG(f"{log['Check Password']}\n")
    # Compare the given password string to what's on file.
    if password == logged_password:
      # The password matches.
      DEBUG(f"log['Confirm Password']\n")
      return True
    else: # The password does not match.
      DEBUG(f"log['Deny Password']\n")
      return False

  def RetrieveCredentials(self, username, key):
    """ Calls the CryptographyMethods.Encryption() method on a given
    users market key and markey secret using a supplied key. 
    
        The key is the first 32 characters of the hash of the users
    password appended to their name. """

    try:# Select the key and secret values for a user.
      # Declare our intention;
      DEBUG(f"{log['Query Execution']}:\n{sql['Market Key/Secret']}\n")
      # Invoke the statement.
      self.cursor.execute(sql['Market Key/Secret'], (username,))
      # Declare success.
      DEBUG(f"{log['Query Success']}\n")
    # If we can't retrieve the key/secret from the database; handle it.
    except Exception as error: ErrorHandling(error)

    # Store the results, and select the return object itself.
    _results = self.cursor.fetchall()[0]

    # Key comes first in the statement, so it's indexed first.
    EncryptedKey = _results[0]
    # Secret is second, so it gets the next index.
    EncryptedSecret = _results[1]

    # Decrypt the key.
    UnencryptedKey = self.crypto.Decryption(
      phrase=key,
      target=EncryptedKey
    )

    # Decrypt the secret.
    UnencryptedSecret = self.crypto.Decryption(
      phrase=key,
      target=EncryptedSecret
    )

   # Package up the results, and return them to the caller.
    return (UnencryptedKey, UnencryptedSecret)


class Userland():
  def __init__(self):
    self.db = Database()
    self.crypto = CryptographyMethods()

  def CreateUser(self, username):
    userHash = self.crypto.SHA256(username)

    while True:
      password = str(getpass("Password: "))
      if str(getpass("Confirmation: ")) == password: break
      else: print("Passwords did not match. Try again.")

    while True:
      key = str(getpass("Key: "))
      if str(getpass("Confirmation: ")) == key: break
      else: print("Keys did not match. Try again.")

    while True:
      secret = str(getpass("Password: "))
      if str(getpass("Confirmation: ")) == secret: break
      else: print("Secrets did not match. Try again.")
    
    EncryptionKey = self.crypto.BuildKey(username, password)

    key = self.crypto.Encryption(EncryptionKey, key)
    secret = self.crypto.Encryption(EncryptionKey, secret)
    password = self.crypto.SHA256(password)

    return self.db.StoreCredentials(userHash, password, key, secret)

  def CheckUser(self):
    """ Compare a 'user' string against all usernames within the database;
    if a match is found, then confirm their existence. Otherwise, deny them. """

    while True:

      user = str(input("Username: "))
      userHash = str(self.crypto.SHA256(user))

      # Declare intention;
      DEBUG(f"log['Check User Existence']: {user}\n")
      # Invoke statement;
      self.db.cursor.execute(
        sql["Select Username"],
        (userHash,)
      )
  
      # If the result of the statement is not empty, then the user exists.
      if len(self.db.cursor.fetchall()) > 0: break
      else: # Otherwise, they do not exist and we should deny them.
        DEBUG(f"{log['Deny User']}")
        self.CreateUser(user)

    password = str(getpass("Password: "))
    passwordHash = str(self.crypto.SHA256(password))

    if self.db.ValidateCredentials(userHash, passwordHash): pass
    else:
      DEBUG(f"{log['Deny Password']}")
      exit()

    key = self.crypto.BuildKey(user, password)

    try: return self.UserDashboard(self.db.RetrieveCredentials(userHash, key))
    except Exception as error: ErrorHandling(error)


  def UserDashboard(self, credentials):
    key = credentials[0]
    secret = credentials[1]

    #API = CoreAccountFunctionality(key, secret, url='https://api.alpaca.markets')
    #print(API.Get_Clock())
    #print(API.List_Positions())