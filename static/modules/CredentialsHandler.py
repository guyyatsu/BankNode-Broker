from CryptographyMethods import CryptographyMethods

CryptographyMethods = CryptographyMethods()

def StoreCredentials( username, password, key, secret, api="alpaca" ):
  """ Encrypt a users username, password, key, and secret for safe
  storage.

  Store the credentials within the applications database. """


  # Create a unique key for encrypting and decrypting secrets.
  EncryptionKey = CryptographyMethods.BuildKey(username, password)

  # Hash the username and password.
  username = CryptographyMethods.SHA256(username)
  password = CryptographyMethods.SHA256(password)

  # Encrypt the sensitive API credentials.
  key = CryptographyMethods.Encryption(EncryptionKey, key)
  secret = CryptographyMethods.Encryption(EncryptionKey, secret)

  # Make the credentials immutable; store key/secret together.
  CredPacket = ( username,#      CredPacket[0]
                 password,#      CredPacket[1]
                 (key,secret) )# CredPacket[2]

  # Check to make sure the column for the given api exists.
  cursor.execute( "PRAGMA table_info(?);", (api,) )
  if cursor.fetchall()[0][0] > 0: pass

  # Create the column if it doesn't exist
  else: cursor.execute( "ALTER TABLE ? ADD ? BLOB", (credentials, api) )

  # Create a new row for the user.
  UserDatabase.Create_Row( "credentials",
                           "username",
                           CredPacket[0]  )

  # Store the users password hash.
  UserDatabase.Add_Value( "credentials",
                          "password",
                          CredPacket[1],
                          CredPacket[0]  )

  # Store the users secrets to the appropriate api.
  UserDatabase.Add_Value( "credentials",
                          api,
                          CredPacket[2],
                          CredPacket[0]  )


def RetrieveCredentials(username, password, api="alpaca"):
  """ """
  # Rebuild the key before hashing.
  EncryptionKey= CryptographyMethods.BuildKey(username, password)

  # Hash the username and password.  
  username= CryptographyMethods.SHA256(username)
  password= CryptographyMethods.SHA256(password)

  # Return the results 
  return UserDatabase.Value_Lookup( api,
                                    "credentials",
                                    "username",
                                    username       )