import re

#regexes
time_regex = re.compile('(?P<h>\d{2}):(?P<m>\d{2}):(?P<s>\d{2})\.(?P<ms>\d{2})')

def tail(path, max_length):
  file = open(path, 'r')
  file.seek(0, 2)
  size = file.tell()

  length = min([size, max_length])
  file.seek(-length, 2)
  result = file.read(length)
  file.close

  return result

def timestring_to_seconds(s):
  match = time_regex.search(s)
  h = match.group('h')
  m = match.group('m')
  s = match.group('s')
  ms = match.group('ms')

  return float(h) * 60 * 60 + float(m) * 60 + float(s) + float('0.%s' % ms)
