# Database API

import os
import sqlite3
from sqlite3 import Error



class DB():
  '''
    Database handler class
  '''
  counter = 0


  def __init__(self, db_file):
    # init db connection
    self.db_file = db_file
    try:
      self.connection = sqlite3.connect(db_file)  

      # self.connection.autocommit(False)
      self.cursor = self.connection.cursor()

    except Error as e:
      print("DB error: unable to connect to db")


  def insert_fingerprint(self, hash):
    # insert fingerprint into db
    # insert (sha, song_id, offset) tuple
    sha, (song_id, offset) = hash
    print(sha, song_id, offset)
    comm = '''
        INSERT INTO fingerprints(sha, song_id, offset)
        VALUES("%s", "%s", "%s");
      ''' % (str(sha), str(song_id), str(offset))
    try:  
      self.cursor.execute(comm)
    except Error as e:
      print("DB error: unable to insert to db")
      print(e) 

  def query(self, fingerprint):
    # find matching fingerprints in db with the given fingerprint
    matches = []
    comm = '''
        SELECT * FROM fingerprints
        WHERE sha = "%s";
      ''' % (fingerprint)
    try:
      self.cursor.execute(comm)
      rows = self.cursor.fetchall()
      for row in rows:
        matches.append((row[1], row[2]))
    except Error as e:
      print("DB error: unable to query db")
    
    return matches

  def return_matches(self, fingerprints):
    # find all fingerprints matches with their offsets
    # for given list of fingerprints
    matches = []

    x = 0

    for fp in fingerprints:
      x += 1
      sha, (song_id, offset) = fp
      matches_for_curr_sha = self.query(sha)
      if x % 100 == 0:
        print(x)
      for row in matches_for_curr_sha:
        # match song_id, diff in offset
        matches.append((row[0], row[1] - offset))
      
      if x > 1000:
        break
    
    return matches