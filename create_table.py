import sqlite3



db_file = 'fingerprints.db'

# create connection
conn = sqlite3.connect(db_file)
c = conn.cursor()

# create table if not exists
c.execute('''
  CREATE TABLE IF NOT EXISTS fingerprints (
    sha char(20) PRIMARY KEY,
    song_id integer NOT NULL,
    offset integer NOT NULL
  );
  ''')

conn.close()