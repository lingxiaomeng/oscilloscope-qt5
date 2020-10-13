import struct

d1 = [0, 0, 1]
d2 = [0, 0, 17]
d3 = [0, 0, 234]
d4 = [0, 0, 214]

abs = (d1[2] << 8) + d2[2]
phase = (d3[2] << 8) + d4[2]
res = struct.pack('HH', abs, phase)



res = struct.unpack('HH', res)
abs = res[0]
phase = res[1]
abs = struct.unpack('h', struct.pack('H', abs))
phase = struct.unpack('h', struct.pack('H', phase))

print(abs[0] / 4096)
print(phase[0] / 2048)
