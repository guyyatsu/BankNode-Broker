#!/bin/python3

from dateutil.parser import parse as ConvertDate
from datetime import datetime


class IncrementError(Exception):
  """ A custom exception used for telling users of
  the DrawGraph function that their chosen increment
  is not defined."""
  print("The given increment is not valid.")
  exit()


def ConvertToTimestamp(date):
  """ Create a UNIX timestamp out of a given date. """
  return round(datetime.timestamp(ConvertDate(date, dayfirst=False)))







def ExtractSecrets(username, password, target):
  # Build the key from the hash of the username + password.
  EncryptionKey= CryptographyMethods.BuildKey(username, password)

  # The 'target' is a tuple; where target[0] is the key...
  key= CryptographyMethods.Decryption(EncryptionKey, target[0])
  # And target[1] is the secret.
  secret= CryptographyMethods.Decryption(EncryptionKey, target[1])

  # Give up the results as a tuple.
  return (key, secret)
