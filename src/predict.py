# Listens to audio with noise and predicts it's name
import pyAudio
import pydub

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