# debug input to output algorithm to produce correct values
import numpy as np

def convert_raw(raw):
  out = []
  sz = len(raw)
  for i in range(sz):
    if i == 0: # transform thrust to [1000 2000]
      out.append(int((3 + raw[i])*500))
    else: # transform roll,pitch,yaw to [-1000 1000]
      out.append(int(raw[i]*1000))
  print out
  out = split_bytes(out)
  return out

def flatten(l):
  res = []
  for r in l:
    if isinstance(r, list):
      res.extend(flatten(r))
    else:
      res.append(r)
  return res

def split_bytes(vals):
  l = []
  if isinstance(vals, list):
    l.extend(flatten(map(split_bytes,vals)))
  else:
    print bin(vals>>8)
    l.append((vals>>8)&0xff)
    l.append(vals&0xff)
  return l

# combines adjacent array bytes in arrays
def combine_arr_bytes(a,two_comp='no'):
  sz = len(a)/2
  if two_comp=='yes':
    # add thrust element to list
    l = [(a[0]<<8) + a[1]]
    for i in range(1,sz):
      c = (a[2*i]<<8) + (a[2*i+1])
      if a[2*i] > 127: 
        c -= 2**16
      l.append(c)
    return l
  else:
    return [((a[2*i]<<8)+a[2*i+1]) for i in range(sz)]

raw = np.linspace(-1,1,100)
raw = np.column_stack((raw,raw,raw,raw))
conv = map(convert_raw,raw)
cmb = [combine_arr_bytes(a,arr='out') for a in conv]
print cmb
