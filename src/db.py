# Database API

import os
import sqlite



class DB():
  '''
    Database handler class
  '''
  def __init__(self, hostname, username, password, database):
    # init db connection
    self.database = database
    try:
      self.connection = mysql.connect(
        hostname, username, password, 
        database, cursorclass=cursors.DictCursor)  

      self.connection.autocommit(False)
      self.cursor = self.connection.cursor()

    except e:
      print("Connection error: unable to connect to db")

  def insert_fingerprints(self, fingerprints):
    # insert all fingerprints into db
    pass
  def query(self, fingerprint):
    # find matching fingerprints in db with the given fingerprint
    pass
  def matches(self):
    # combine all matches for the unknown sample and calculate their offsets
    pass
  