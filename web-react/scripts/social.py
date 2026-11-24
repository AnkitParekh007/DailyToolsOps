"""Create a local placeholder social card; replace with an approved branded asset."""
from pathlib import Path
import struct,zlib
W,H=1200,630
pixels=bytearray(bytes((12,19,35))*W*H)
def rect(x,y,w,h,c):
    for yy in range(y,y+h):
        off=(yy*W+x)*3
        pixels[off:off+w*3]=bytes(c)*w
rect(72,72,1056,486,(21,30,48))
rect(108,112,110,110,(215,7,22))
for i in range(32):
    rect(132+i,139+i,7,7,(255,255,255))
    rect(132+i,201-i,7,7,(255,255,255))
rect(171,196,31,7,(255,255,255))
glyphs={"D":["1110","1001","1001","1001","1110"],"A":["0110","1001","1111","1001","1001"],"I":["111","010","010","010","111"],"L":["100","100","100","100","111"],"Y":["101","101","010","010","010"],"T":["111","010","010","010","010"],"O":["0110","1001","1001","1001","0110"],"S":["0111","1000","0110","0001","1110"],"P":["1110","1001","1110","1000","1000"]}
x=108
for ch in "DAILYTOOLSOPS":
    rows=glyphs[ch]
    for y,row in enumerate(rows):
        for col,p in enumerate(row):
            if p=="1":rect(x+col*15,300+y*15,13,13,(245,246,250))
    x+=(len(rows[0])+1)*15
rect(108,425,320,7,(255,137,145))
def chunk(kind,data):
    return struct.pack(">I",len(data))+kind+data+struct.pack(">I",zlib.crc32(kind+data)&0xffffffff)
raw=b"".join(b"\0"+pixels[y*W*3:(y+1)*W*3] for y in range(H))
(Path(__file__).resolve().parents[1]/"public/social.png").write_bytes(b"\x89PNG\r\n\x1a\n"+chunk(b"IHDR",struct.pack(">IIBBBBB",W,H,8,2,0,0,0))+chunk(b"IDAT",zlib.compress(raw))+chunk(b"IEND",b""))
