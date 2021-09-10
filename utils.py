import struct

def char(c):
    # char 1 byte
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    # short 2 bytes
    return struct.pack('=h', w)

def dword(d):
    # long 4 bytes
    return struct.pack('=l', d)

def color(r,g,b):
    if(r>255):
        r = 255
    if(g>255):
        g = 255
    if(b>255):
        b = 255
    if(r<0):
        r = 0
    if(g<0):
        g = 0
    if(b<0):
        b = 0
    return bytes([b,g,r])