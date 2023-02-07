import json

name = 'cat_psjpeg.json'
fr = open(name)
dict_load = json.load(fr)
code = dict_load["code"]
data = list(map(int, dict_load["data"]))
dim = dict_load["dim"]

l = dim[0]
w = dim[1]
print(f'size of the image: {l} x {w} x 3 = {l*w*3}')
print(f'size of compressed data: {len(data)}')
print(f'compression rate: {len(data) / (l*w*3)}')

s = ''
s = s.join(list(map(str, data)))
data_bits = len(s)
data_bytes = data_bits // 8
print(f'data size in bits: {data_bits}')
print(f'data size in bytes: {data_bits//8}')
