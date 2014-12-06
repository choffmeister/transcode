import utils

import re
import subprocess

#regexes
duration_regex = re.compile('Duration:\s*(?P<time>\d{2}:\d{2}:\d{2}.\d{2})')
stream_regex = re.compile('Stream #(?P<stream_id>\d+:\d+)(\((?P<language>\w+)\))?: (?P<type>\w+): (?P<format>[\w\d]+)')
crop_regex = re.compile('crop=(?P<width>\d+):(?P<height>\d+):(?P<x>\d+):(?P<y>\d+)')

# detect crop settings
def detect_crop(src):
  proc = subprocess.Popen(['ffmpeg', '-i', src, '-t', str(100), '-filter:v', 'cropdetect', '-f', 'null', '-'], stderr=subprocess.PIPE)
  stdout, stderr = proc.communicate()
  crops = crop_regex.findall(stderr)
  return max(set(crops), key=crops.count)

 # detect duration
def detect_duration(src):
  proc = subprocess.Popen(['ffmpeg', '-i', src], stderr=subprocess.PIPE)
  stdout, stderr = proc.communicate()
  match = duration_regex.search(stderr)
  duration_str = match.group('time')
  duration_secs = utils.timestring_to_seconds(duration_str)
  return (duration_str, duration_secs)

# detects stream IDs
def detect_streams(src):
  proc = subprocess.Popen(['ffmpeg', '-i', src], stderr=subprocess.PIPE)
  stdout, stderr = proc.communicate()

  streams = []
  for m in stream_regex.finditer(stderr):
    streams.append({
      'id': m.group('stream_id'),
      'lang': m.group('language'),
      'type': m.group('type'),
      'fmt': m.group('format')
    })
  return streams