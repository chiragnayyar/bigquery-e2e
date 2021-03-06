#!/usr/bin/python2.7
# All rights to this package are hereby disclaimed and its contents
# released into the public domain by the authors.

'''Resolves ZIP codes from latitude and longitude pairs.

Uses the zip_centers.json file to build a k-d Tree that is used
for the zip-code assignment.
'''

import json
import sys

# Imports from files in local directory:
from kdtree import KDTree

class ZipPoint(tuple):
  '''Tuple containing a lat, long, and zip code.'''
  def __new__(cls, json_dict):
    return super(ZipPoint, cls).__new__(
      cls, (json_dict['lat'], json_dict['lng']))

  def __init__(self, json_dict):
    self.zip = json_dict['zip']

with open('zip_centers.json', 'r') as f:
  ZIP_INDEX = KDTree([ZipPoint(json.loads(r)) for r in f])

def apply(input):
  val = json.loads(input)
  closest = ZIP_INDEX.query((val['lat'], val['lng']))
  if closest:
    val['zip'] = closest[0].zip
    yield json.dumps(val) + '\n'
  else:
    yield input

if __name__ == '__main__':
  for line in sys.stdin:
    for o in apply(line):
      print o,
