# Upload wav files to db after converting to fingerprints first

import argparse
import os
import pydub
import wave
from scipy.io import wavfile
import scipy.io
import glob
import utils
from db import DB



# parser = argparse.ArgumentParser()
# parser.add_argument("dir", help="directory containing wav files")
# args = parser.parse_args()
# print(args.dir)
# print(type(args.dir))

def upload_wav_to_db():
  path = 'data/'
  files = [f for f in glob.glob(path + "**/*.wav", recursive=True)]

  for wavefile in files:
    # call get_fingerprints() for each of it's samples
    # insert all fingerprints to db with song_id, offset

    channels = extract_channels(wavefile)
    song_id = wavefile.split('/')[-1].split('.')[0] #song_name

    print(song_id)

    db_client = DB('fingerprints.db')

    for channel in channels:
      utils.fingerprint(channel, song_id, db_client)

    
def extract_channels(path):
  channels = []
  Fs, frames = wavfile.read(path)
  wave_object = wave.open(path)
  nchannels, sampwidth, framerate, num_frames, comptype, compname = wave_object.getparams()

  for channel in range(nchannels):
    channels.append(frames[:, channel])
  return channels


upload_wav_to_db()
