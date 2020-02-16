# Hashing implementations
#
# Functions to convert channel sample to fingerprints(hashes)
import numpy as np
import hashlib
import matplotlib.mlab as mlab
from scipy.ndimage.morphology import generate_binary_structure, iterate_structure, binary_erosion
from scipy.ndimage.filters import maximum_filter



Fs = 44100 
wsize = 4096 
wratio = 0.5
fan_value = 15 
amp_min = 10
min_hash_time_delta = 0


def fingerprint(sample, song_id, db_client):
  """Used for learning known songs"""
  hashes = process_channel(sample, song_id=song_id)
  print("Generated %d hashes" % len(hashes))
  # db_client.insert_hashes(hashes)
  for hash in hashes:
    db_client.insert_fingerprint(hash)

def match(sample, db_client):
  """Used for matching unknown songs"""
  hashes = process_channel(sample)
  matches = db_client.return_matches(hashes)
  return matches

def process_channel(channel_sample, song_id=None):
  """
    FFT the channel, log transform output, find local maxima, then return
    locally sensitive hashes. 
  """
  # FFT the signal and extract frequency components
  arr2D = mlab.specgram(
    channel_sample, 
    NFFT=wsize, 
    Fs=Fs,
    window=mlab.window_hanning,
    noverlap=int(wsize* wratio))[0]

  # apply log transform since specgram() returns linear array
  arr2D = 10 * np.log10(arr2D)
  arr2D[arr2D == -np.inf] = 0 # replace infs with zeros
  
  # find local maxima
  local_maxima = get_2D_peaks(arr2D, plot=False)

  # return hashes
  return generate_hashes(local_maxima, song_id=song_id)

def get_2D_peaks(arr2D, plot=False):

  # http://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.morphology.iterate_structure.html#scipy.ndimage.morphology.iterate_structure
  struct = generate_binary_structure(2, 1)
  peak_neigh_size = 20
  neighborhood = iterate_structure(struct, peak_neigh_size) 

  # find local maxima using our fliter shape
  local_max = maximum_filter(arr2D, footprint=neighborhood) == arr2D 
  background = (arr2D == 0)
  eroded_background = binary_erosion(background, structure=neighborhood, border_value=1)
  detected_peaks = local_max ^ eroded_background # this is a boolean mask of arr2D with True at peaks

  # extract peaks
  amps = arr2D[detected_peaks]
  j, i = np.where(detected_peaks) 

  # filter peaks
  amps = amps.flatten()
  peaks = zip(i, j, amps)
  peaks_filtered = [x for x in peaks if x[2] > amp_min] # freq, time, amp
  
  # get indices for frequency and time
  frequency_idx = [x[1] for x in peaks_filtered]
  time_idx = [x[0] for x in peaks_filtered]

  return zip(frequency_idx, time_idx)

def generate_hashes(peaks, song_id=None):
  """
  Hash list structure:
    sha1-hash[0:20]    song_id, time_offset
  [(e05b341a9b77a51fd26,   (3, 32)), ... ]
  """
  fingerprinted = set() # to avoid rehashing same pairs
  hashes = []

  peaks = list(peaks)

  for i in range(len(peaks)):
    for j in range(fan_value):
      if i+j < len(peaks) and not (i, i+j) in fingerprinted:

        freq1 = peaks[i][0]
        freq2 = peaks[i+j][0]
        t1 = peaks[i][1]
        t2 = peaks[i+j][1]
        t_delta = t2 - t1
        
        if t_delta >= min_hash_time_delta:
          h = hashlib.sha1(("%s|%s|%s" % (str(freq1), str(freq2), str(t_delta))).encode('utf-8'))
          hashes.append((h.hexdigest()[0:20], (song_id, t1)))
        
        # ensure we don't repeat hashing
        fingerprinted.add((i, i+j))
  return hashes
    
def align_matches(matches, record_seconds=0, verbose=False):
  """
    Finds hash matches that align in time with other matches and finds
    consensus about which hashes are "true" signal from the audio.
    
    Returns a dictionary with match information.
  """
  # align by diffs
  diff_counter = {}
  largest = 0
  largest_count = 0
  song_id = -1
  for tup in matches:
    sid, diff = tup
    if not diff in diff_counter:
      diff_counter[diff] = {}
    if not sid in diff_counter[diff]:
      diff_counter[diff][sid] = 0
    diff_counter[diff][sid] += 1

    if diff_counter[diff][sid] > largest_count:
      largest = diff
      largest_count = diff_counter[diff][sid]
      song_id = sid
  
  # extract idenfication        
  songname = song_id
  songname = songname.replace("_", " ")
  
  # return match info
  song = {
    "song_name" : songname
  }
      
  return song