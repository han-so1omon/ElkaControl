import sys
import struct
import matplotlib.pyplot as plt
import re

f = open("acks.log","r")

gx,gy,gz,time = [],[],[],[]

def joinbytes(values):
    val = struct.unpack('h',values[0:2])
    return val[0]

def flatten(l):
  res = []
  for r in l:
    if isinstance(r, list):
      res.extend(flatten(r))
    else:
      res.append(r)
  return res

i = 0

lines = f.readlines()

#for l in (raw.strip().split(',') for raw in lines[:-1]): 
#    print l


for l in lines[:-1]: 
    r = re.split(r"(\d+:\d+:\d+.\d+,array\('B',)",l)
    r1 = r[-1][2:-3]
    columns = r1.strip().split(',')
    #i=i+1
    #print str(columns[:2]), i, len(lines), '\n'
    
    if len(columns)>10:
    #gx.append(str(joinbytes(columns[0:2])))
        gx_high = chr(int(columns[11]))
        gx_low = chr(int(columns[12]))
        gy_high = chr(int(columns[13]))
        gy_low = chr(int(columns[14]))
        gz_high = chr(int(columns[15]))
        gz_low = chr(int(columns[16])) 
        gx_join = ([str(joinbytes(gx_low+gx_high))])
        gx.append(flatten(gx_join))
        gy_join = ([str(joinbytes(gy_low+gy_high))])
        gy.append(flatten(gy_join))
        gz_join = ([str(joinbytes(gz_low+gz_high))])
        gz.append(flatten(gz_join))
        i = i+1


gx = flatten(gx)
gyro_x = [int(c) for c in gx]
gy = flatten(gy)
gyro_y = [int(c) for c in gy]
gz = flatten(gz)
gyro_z = [int(c) for c in gz]
 
#plt.plot(time,gyro_y,'r',time,gyro_x,'b')
plt.subplot(311),plt.plot(gyro_x,'r')
plt.subplot(312),plt.plot(gyro_y,'b')
plt.subplot(313),plt.plot(gyro_z,'b')
plt.show()


