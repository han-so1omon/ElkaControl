import struct

header = [0, 255, 255]
s = struct.pack('B' * len(header), *header)
print s
t = struct.unpack('B' * len(s), s)
print t
