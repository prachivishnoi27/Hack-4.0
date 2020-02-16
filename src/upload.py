# Upload wav files to db after converting to fingerprints first

import argparse
import os
import pydub
import wave
import scipy.io
import glob



# parser = argparse.ArgumentParser()
# parser.add_argument("dir", help="directory containing wav files")
# args = parser.parse_args()
# print(args.dir)
# print(type(args.dir))

def upload_wav_to_db():
  path = 'data/'
  files = [f for f in glob.glob(path + "**/*.wav", recursive=True)]

  for f in files:
    print(f)

    # open wav file

    #call get_fingerprints() for each of it's samples
    #insert all fingerprints to db with song_id, offset
