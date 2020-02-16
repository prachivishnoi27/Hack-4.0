# Database API

import os
import sqlite



class DB():
  '''
    Database handler class
  '''
  def __init__(self, hostname, username, password, database):
    # connect
    self.database = database
    try:
      self.connection = mysql.connect(
        hostname, username, password, 
        database, cursorclass=cursors.DictCursor)  

      self.connection.autocommit(False)
      self.cursor = self.connection.cursor()

    except e:
      print("Connection error: unable to connect to db")

  def insert_fingerprint(self):
    pass
  def query(self):
    pass
  def matches(self):
    pass
  