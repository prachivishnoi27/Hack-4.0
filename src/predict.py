# Listens to audio with noise and predicts it's name
import pydub
import wave
from scipy.io import wavfile
import utils
from db import DB
import glob
import os

def predict(sample):
  '''
    Predicts song from small unknown sample
  '''

  # get fingerprints with offset
  # query each fingerprint to get matching fingerprints
  # take all matching fingerprints and find the matching song_id
  # return song details
  pass


def record(given_length=10):
  '''
    Records audio signal and convert it to required format
  '''

  # record audio signal of given_length
  # clean audio (remove noise)
  # return audio sample
  pass


def predict_from_file(file_path):
  channels = extract_channels(file_path)

  db_client = DB('fingerprints.db')

  print("len of channels: ", len(channels))

  for channel in channels:
    matches = utils.match(channel, db_client)

    print("len of matches: ", len(matches))

    song = utils.align_matches(matches)
    print(song)


def extract_channels(path):
  channels = []
  Fs, frames = wavfile.read(path)
  wave_object = wave.open(path)
  nchannels, sampwidth, framerate, num_frames, comptype, compname = wave_object.getparams()

  for channel in range(nchannels):
    channels.append(frames[:, channel])
  return channels

path = 'data/query/test/'
files = [f for f in glob.glob(path + "**/*.wav", recursive=True)]

for wavefile in files:
  predict_from_file(wavefile)
  print("Actual name: ", wavefile)