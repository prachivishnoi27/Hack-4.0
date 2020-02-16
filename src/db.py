# Database API

import os
import sqlite3



class DB():
  '''
    Database handler class
  '''


  def __init__(self, db_file):
    # init db connection
    self.db_file = db_file
    try:
      self.connection = sqlite3.connect(db_file)  

      # self.connection.autocommit(False)
      self.cursor = self.connection.cursor()

    except e:
      print("DB error: unable to connect to db")


  def insert_fingerprint(self, sha, song_id, offset):
    # insert fingerprint into db
    # insert (sha, song_id, offset) tuple
    try:  
      self.connection.execute('''''')
      self.connection.commit()
    except e:
      print("DB error: unable to insert to db")   

  def query(self, fingerprint):
    # find matching fingerprints in db with the given fingerprint
    try:
      self.connection.execute()
    except e:
      print("DB error: unable to query db")

  def matches(self, fingerprints):
    # find all fingerprints matches with their offsets
    # for given list of fingerprints
    matches = []

    for fp in fingerprints:
      sha, song_id, offset = fp
      matches_for_curr_sha = self.connection.query(sha)
      for row in matches_for_curr_sha:
        matches.append((row[0], row[1] - offset))
    
    return matches