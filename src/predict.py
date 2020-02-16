# Listens to audio with noise and predicts it's name
import pydub
import pyaudio
import wave
from scipy.io import wavfile
import utils
from db import DB
import glob
import os
import numpy as np



def listen(seconds=7):
  # open stream
  au = pyaudio.PyAudio()
  stream = au.open(format=pyaudio.paInt16,
            channels=2,
            rate=44100,
            input=True,
            frames_per_buffer=8192)
  
  print("* recording")
  left, right = [], []
  for i in range(0, int(44100 / 8192 * seconds)):
    data = stream.read(8192)
    nums = np.fromstring(data, np.int16)
    left.extend(nums[1::2])
    right.extend(nums[0::2])
  print("* done recording")
  
  # close and stop the stream
  stream.stop_stream()
  stream.close()

  db_client = DB('fingerprints.db')
  
  # match both channels
  matches = []
  matches.extend(utils.match(left, db_client))
  matches.extend(utils.match(right, db_client))
  
  # align and return
  return utils.align_matches(matches)


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

# path = 'data/query/test/'
# files = [f for f in glob.glob(path + "**/*.wav", recursive=True)]

# for wavefile in files:
#   predict_from_file(wavefile)
#   print("Actual name: ", wavefile)

print(listen())