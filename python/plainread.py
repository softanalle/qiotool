#!/usr/bin/python3


import sys
import io

device='/dev/random'

def formathex(a):
    out = ''
    for j in range(0, len(a)):
        out = out + format(a[j], '02x')

    return out

f = open(device, 'rb')

for i in range(0,10):
    data=f.read(40)
    print("%03d = %s" % (i, formathex(data)))


f.close()
