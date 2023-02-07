# ----------------------------------------------------------------------
# JPEG Image Compression
# ----------------------------------------------------------------------

import numpy as np
import cv2
import math
import json

# ------------------------------------------------------------
# BGR to YCbCr conversion / perform 4:2:2 or 4:2:0
# ------------------------------------------------------------
def ycbcr_compress(img, mode):
  l, w, _ = img.shape
  if mode == 420:
    row_step, col_step = 2, 2
  elif mode == 422:
    row_step, col_step = 2, 1
  else: # mode = 444, no compression
    row_step, col_step = 1, 1

  # BGR to YCbCr conversion
  y = 0.299 * img[:,:,2] + 0.587 * img[:,:,1] + 0.114 * img[:,:,0]
  cb = 0.565 * (img[:,:,0] - y)
  cr = 0.713 * (img[:,:,2] - y)

  # CbCr compresion
  cb = cb[::row_step, ::col_step]
  cr = cr[::row_step, ::col_step]

  return y, cb, cr

def ycbcr_recover(y, cb, cr, mode):
  l, w = y.shape

  # restore cb, cr
  cb_rc = np.zeros((l, w))
  cr_rc = np.zeros((l, w))
  if mode == 420:
    cb_rc[::2, ::2] = cb
    cr_rc[::2, ::2] = cr
    # o: known   x: recovery target   .: unknown
    # o . o
    # x . x
    # o . o
    for i in range(1, l, 2): # odd numbers
      for j in range(0, w, 2): # even numbers
        if i + 1 < l:
          cb_rc[i, j] = (cb_rc[i-1, j] + cb_rc[i+1, j]) / 2
          cr_rc[i, j] = (cr_rc[i-1, j] + cr_rc[i+1, j]) / 2
        else: # last row; use row i-1
          cb_rc[i, j] = cb_rc[i-1, j]
          cr_rc[i, j] = cr_rc[i-1, j]
    # o x o
    # o . o
    # o x o
    for i in range(0, l, 2): # even numbers
      for j in range(1, w, 2): # odd numbers
        if j + 1 < w:
          cb_rc[i, j] = (cb_rc[i, j-1] + cb_rc[i, j+1]) / 2
          cr_rc[i, j] = (cr_rc[i, j-1] + cr_rc[i, j+1]) / 2
        else: # last column; use column j-1
          cb_rc[i, j] = cb_rc[i, j-1]
          cr_rc[i, j] = cr_rc[i, j-1]
    # o o o
    # o x o
    # o o o
    for i in range(1, l, 2): # odd numbers
      for j in range(1, w, 2): # odd numbers
        # row average
        if i + 1 < l:
          row_avg_cb = (cb_rc[i-1, j] + cb_rc[i+1, j]) / 2
          row_avg_cr = (cr_rc[i-1, j] + cr_rc[i+1, j]) / 2
        else: # last row; use row i-1
          row_avg_cb = cb_rc[i-1, j]
          row_avg_cr = cr_rc[i-1, j]

        # column average
        if j + 1 < w:
          col_avg_cb = (cb_rc[i, j-1] + cb_rc[i, j+1]) / 2
          col_avg_cr = (cr_rc[i, j-1] + cr_rc[i, j+1]) / 2
        else: # last row; use column j-1
          col_avg_cb = cb_rc[i, j-1]
          col_avg_cr = cr_rc[i, j-1]

        # target value
        cb_rc[i, j] = (row_avg_cb + col_avg_cb) / 2
        cr_rc[i, j] = (row_avg_cr + col_avg_cr) / 2
  elif mode == 422:
    cb_rc[::2, :] = cb
    cr_rc[::2, :] = cr
    for i in range(1, l, 2): # odd numbers
      if i + 1 < l:
        # restore row i by averaging row i-1, i+1
        cb_rc[i, :] = (cb_rc[i-1, :] + cb_rc[i+1, :]) / 2
        cr_rc[i, :] = (cr_rc[i-1, :] + cr_rc[i+1, :]) / 2
      else: # last row; use row i-1
        cb_rc[i, :] = cb_rc[i-1, :]
        cr_rc[i, :] = cr_rc[i-1, :]
  else: # mode = 444, no compression
    cb_rc = cb
    cr_rc = cr

  # recover BGR image
  b = (cb_rc / 0.565) + y
  r = (cr_rc / 0.713) + y
  g = (y - (0.299 * r) - (0.114 * b)) / 0.587
  bgr = np.zeros((l, w, 3), dtype='int16')
  bgr[:,:,0] = b
  bgr[:,:,1] = g
  bgr[:,:,2] = r

  return bgr

# ------------------------------------------------------------
# 8x8 DCT
# ------------------------------------------------------------
def dct8x8(input_m):
  # fill zeros if boundary blocks have size smaller than 8x8
  l, w = input_m.shape
  rl, rw = l % 8, w % 8
  new_l = l if rl == 0 else l - rl + 8
  new_w = w if rw == 0 else w - rw + 8
  new_m = np.zeros((new_l, new_w))
  new_m[:l, :w] = input_m
  new_m -= 128

  # perform DCT
  m = np.arange(8).reshape(8,1)
  n = np.arange(8)
  dct_result = np.zeros(new_m.shape)
  C = np.ones(8)
  C[0] = 1 / math.sqrt(2)
  for u8 in range(0, l, 8):
    for v8 in range(0, w, 8):
      for u in range(8):
        for v in range(8):
          A = C[u] * C[v] / 4 # constant
          c1 = np.cos((2 * m + 1) * u * np.pi / 16) # first cos term
          c2 = np.cos((2 * n + 1) * v * np.pi / 16) # second cos term
          dct_result[u8+u,v8+v] = A * np.sum(new_m[u8+m, v8+n] * c1 * c2)
  return dct_result

def idct8x8(input_m, l_init, w_init):
  l, w = input_m.shape
  u = np.arange(8).reshape(8,1)
  v = np.arange(8)
  idct_result = np.zeros((l, w))
  C = np.ones(8)
  C[0] = 1 / math.sqrt(2)
  for m8 in range(0, l, 8):
    for n8 in range(0, w, 8):
      for m in range(8):
        for n in range(8):
          A = C[u] * C[v] / 4 # constant
          c1 = np.cos((2 * m + 1) * u * np.pi / 16) # first cos term
          c2 = np.cos((2 * n + 1) * v * np.pi / 16) # second cos term
          idct_result[m8+m,n8+n] = np.sum(A * input_m[m8+u, n8+v] * c1 * c2)
  return idct_result[:l_init, :w_init] + 128

# ------------------------------------------------------------
# quantization
# ------------------------------------------------------------
def qtz(input_m, inverse=False):
  # JPEG standard of 50% compression quantization table
  qtz_table = np.array([
    [16, 11, 10, 16, 24, 40, 51, 61],
    [12, 12, 14, 19, 26, 58, 60, 55],
    [14, 13, 16, 24, 40, 57, 69, 56],
    [14, 17, 22, 29, 51, 87, 80, 62],
    [18, 22, 37, 56, 68,109,103, 77],
    [24, 35, 55, 64, 81,104,113, 92],
    [49, 64, 78, 87,103,121,120,101],
    [72, 92, 95, 98,112,100,103, 99]
  ])
  l, w = input_m.shape
  output_m = np.zeros((l, w))
  for u8 in range(0, l, 8):
    for v8 in range(0, w, 8):
      if (inverse): # restore values before quantization
        output_m[u8:u8+8, v8:v8+8] = input_m[u8:u8+8, v8:v8+8] * qtz_table
      else:         # perform quantization
        output_m[u8:u8+8, v8:v8+8] = input_m[u8:u8+8, v8:v8+8] // qtz_table
  return output_m

# ------------------------------------------------------------
# differential coding for DC terms
# ------------------------------------------------------------
def diff_enc(input_m):
  l, w = input_m.shape
  enc = input_m.copy() # reserve first column as decoding reference
  for i in range(1, w):
    enc[:, i] = input_m[:, i] - input_m[:, i-1]
  return enc
  
def diff_dec(input_m):
  l, w = input_m.shape
  dec = input_m.copy() # use first column as decoding reference
  for i in range(1, w):
    dec[:, i] = input_m[:, i] + dec[:, i-1]
  return dec

# ------------------------------------------------------------
# zigzag for AC terms
# ------------------------------------------------------------
def zigzag(input_m):
  l, _ = input_m.shape # input_m is assumed to be a square
  upper_right = True # zigzag scan direction
  output_arr = []

  for i in range(1, 2*l - 1): # ignore dc term [0][0], start from 1
    for j in range(i + 1):
      if i - j >= l or j >= l: # out of range
        continue
      if upper_right: # [i][0] => [0][i]
        target = input_m[i-j][j]
      else:           # [0][i] => [i][0]
        target = input_m[j][i-j]
      output_arr.append(target)
    upper_right = not upper_right # switch direction

  # find end of block(EOB) and ignore values after EOB
  eob = 0
  s = len(output_arr)
  for i in range(s):
    if output_arr[i]:
      eob = i

  return output_arr[:eob+1]

def inv_zigzag(seq, l):
  recover_m = np.zeros((l, l))
  k = 0
  i, j = 1, 0
  upper_right = True # zigzag scan direction
  while k < len(seq):
    recover_m[i][j] = seq[k]
    if upper_right: # [i][0] => [0][j]
      if j == l-1:
        i += 1
        upper_right = False
      elif i == 0:
        j += 1
        upper_right = False
      else:
        i -= 1
        j += 1
    else:           # [0][j] => [i][0]
      if i == l-1:
        j += 1
        upper_right = True
      elif j == 0:
        i += 1
        upper_right = True
      else:
        i += 1
        j -= 1
    k += 1

  return recover_m

# ------------------------------------------------------------
# Huffman coding
# ------------------------------------------------------------
def Huffman_enc(data):
  # count every value in m and store in dictionary
  data_size = data.size
  flat = data.flatten()
  count = dict()
  for i in range(data_size):
    if flat[i] not in count:
      count[flat[i]] = 1
    else:
      count[flat[i]] += 1

  # encode and store code in dictionary
  code = dict()
  current_code = 0
  while count: # count is not empty
    k = max(count, key=count.get) # key with max value
    count.pop(k)
    code[k] = bin(current_code)[2:] # [2:] to remove prefix '0b'
    current_code += 1

  # construct new matrix with values replaced by corresponding codes
  map_code = np.vectorize(lambda n: code[n])
  new_data = map_code(data)
  return code, new_data

def Huffman_dec(data, code):
  inv_code = dict()
  for key, value in code.items():
    inv_code[value] = int(float(key))
  #print(inv_code[10010])
  data_restore = list(map(lambda n: inv_code[str(n)], data))
  return data_restore

# ------------------------------------------------------------
# main function
# ------------------------------------------------------------
def JPEG_compress(img):
  l, w, _ = img.shape
  mode = 420 # 4:4:4, 4:2:2, 4:2:0

  # convert image to YCbCr and perform 4:2:2 or 4:2:0
  print('Performing YCbCr compression ... ', end='')
  y, cb, cr = ycbcr_compress(img, mode)
  cbl, cbw = cb.shape
  print('done')

  # perform 8x8 DCT (the type mentioned in the ADSP course)
  print('Perfomring DCT ... ', end='')
  y_dct = dct8x8(y)
  cb_dct = dct8x8(cb)
  cr_dct = dct8x8(cr)

  cb_shape = cb_dct
  cr_shape = cr_dct
  print('done')

  # quantization
  print('Quantizing ... ', end='')
  y_q = qtz(y_dct)
  cb_q = qtz(cb_dct)
  cr_q = qtz(cr_dct)
  #y_q = y_dct // 1
  #cb_q = cb_dct // 1
  #cr_q = cr_dct // 1
  print('done')

  # differential encoding for DC terms
  print('Performing differential encoding ... ', end='')
  y_dc = diff_enc(y_q[::8, ::8])
  cb_dc = diff_enc(cb_q[::8, ::8])
  cr_dc = diff_enc(cr_q[::8, ::8])
  print('done')

  # zigzag for AC terms
  print('Performing zigzag ... ', end='')
  yl = y_dc.shape[0]
  yw = y_dc.shape[1]
  y_ac = np.array([])
  y_ac_sizes = []
  for i in range(yl):
    for j in range(yw):
      yzz = zigzag(y_q[i*8:i*8+8, j*8:j*8+8])
      y_ac_sizes.append(len(yzz))
      y_ac = np.concatenate((y_ac, np.array(yzz)))

  cbdcl = math.ceil(cbl / 8)
  cbdcw = math.ceil(cbw / 8)
  cb_ac = np.array([])
  cr_ac = np.array([])
  cb_ac_sizes = []
  cr_ac_sizes = []
  for i in range(cbdcl):
    for j in range(cbdcw):
      cbzz = zigzag(cb_q[i*8:i*8+8, j*8:j*8+8])
      crzz = zigzag(cr_q[i*8:i*8+8, j*8:j*8+8])
      cb_ac_sizes.append(len(cbzz))
      cr_ac_sizes.append(len(crzz))
      cb_ac = np.concatenate((cb_ac, np.array(cbzz)))
      cr_ac = np.concatenate((cr_ac, np.array(crzz)))
  print('done')

  # Huffman coding
  print('Performing Huffman coding ... ', end='')
  pack = np.concatenate((
    y_dc.flatten(), 
    cb_dc.flatten(), 
    cr_dc.flatten(), 
    y_ac, cb_ac, cr_ac
  ))
  code, data = Huffman_enc(pack)
  dim = [l, w, cbl, cbw, y_ac_sizes, cb_ac_sizes, cr_ac_sizes]
  print('done')
  print('JPEG compression finished')

  return list(data), code, dim, mode

def JPEG_extract(data, code, dim, mode):
  [l, w, cbl, cbw, y_ac_sizes, cb_ac_sizes, cr_ac_sizes] = dim

  # calculate data offsets
  ydcl = math.ceil(l / 8)
  ydcw = math.ceil(w / 8)
  ydc_size = ydcl * ydcw
  cbdcl = math.ceil(cbl / 8)
  cbdcw = math.ceil(cbw / 8)
  cbdc_size = cbdcl * cbdcw
  img_size = l * w
  cb_size = cbl * cbw

  # decode Huffman coding
  print('Decoding data ... ', end='')
  data_restore = Huffman_dec(data, code)
  print('done')

  # restore DC terms
  print('Restoring DC terms ... ', end='')
  y_dc_data = data_restore[0:ydc_size]
  cb_dc_data = data_restore[ydc_size: ydc_size + cbdc_size]
  cr_dc_data = data_restore[ydc_size + cbdc_size: ydc_size + 2*cbdc_size]
  y_dc = diff_dec(np.array(y_dc_data).reshape(ydcl, ydcw))
  cb_dc = diff_dec(np.array(cb_dc_data).reshape(cbdcl, cbdcw))
  cr_dc = diff_dec(np.array(cr_dc_data).reshape(cbdcl, cbdcw))
  print('done')

  # restore AC terms
  print('Restoring AC terms ... ', end='')
  half = ydc_size + 2*cbdc_size
  y_ac_data = data_restore[half:ydc_size]
  cb_ac_data = data_restore[half + ydc_size: ydc_size + cbdc_size]
  cr_ac_data = data_restore[half + ydc_size + cbdc_size: ydc_size + 2*cbdc_size]
  
  start = 0
  end = 0
  k = 0
  y_restore = np.zeros((ydcl*8, ydcw*8))
  for i in range(ydcl):
    for j in range(ydcw):
      start = end
      end = end + y_ac_sizes[k]
      y_restore[i*8:i*8+8, j*8:j*8+8] = inv_zigzag(y_ac_data[start:end], 8)
      k += 1

  cb_start, cb_end = 0, 0
  cr_start, cr_end = 0, 0
  k = 0
  cb_restore = np.zeros((cbdcl*8, cbdcw*8))
  cr_restore = np.zeros((cbdcl*8, cbdcw*8))
  for i in range(cbdcl):
    for j in range(cbdcw):
      cb_start = cb_end
      cr_start = cr_end
      cb_end = cb_end + cb_ac_sizes[k]
      cr_end = cr_end + cr_ac_sizes[k]
      cb_restore[i*8:i*8+8, j*8:j*8+8] = inv_zigzag(cb_ac_data[cb_start:cb_end], 8)
      cr_restore[i*8:i*8+8, j*8:j*8+8] = inv_zigzag(cr_ac_data[cr_start:cr_end], 8)
      k += 1
  print('done')
      
  # restore Y, Cb, Cr
  print('Performing quantization and inverse DCT ... ', end='')
  y_restore[::8, ::8] = y_dc
  cb_restore[::8, ::8] = cb_dc
  cr_restore[::8, ::8] = cr_dc

  y_iq = qtz(y_restore, inverse=True)
  cb_iq = qtz(cb_restore, inverse=True)
  cr_iq = qtz(cr_restore, inverse=True)
  #y_iq = y_restore
  #cb_iq = cb_restore
  #cr_iq = cr_restore

  y_idct = idct8x8(y_iq, l, w)
  cb_idct = idct8x8(cb_iq, cbl, cbw)
  cr_idct = idct8x8(cr_iq, cbl, cbw)
  print('done')

  # restore image
  print('Converting YCbCr to BGR ... ', end='')
  img = ycbcr_recover(y_idct, cb_idct, cr_idct, mode)
  print('done')
  print('JPEG image extraction completed')

  return img

# ------------------------------------------------------------
# test
# ------------------------------------------------------------
if __name__ == '__main__':
  # boolean variables for different tests
  # test progress:
  # - YCbCr compression: pass
  # - 8x8 DCT: pass
  # - quantization: pass
  # - differential coding: pass
  # - zigzag: pass
  # - Huffman coding: pass
  ycbcr_compress_test = False
  dct_test = False
  qtz_test = False
  diff_code_test = False
  zigzag_test = False
  Huffman_code_test = False
  jpeg_compression_test = True
  jpeg_extraction_test = True

  # JPEG compression test
  if jpeg_compression_test:
    img_path = 'cat.png'
    #img_path = 'black.jpg'
    img = cv2.imread(img_path)
    data, code, dim, mode = JPEG_compress(img)
    data_dict = {
      "data": data,
      "code": code,
      "dim" : dim,
      "mode": mode
    }
    # save pseudo jpeg file (json)
    with open('cat_psjpeg.json', 'w') as f:
      json.dump(data_dict, f)
    f.close()

  # jpeg extraction test
  if jpeg_extraction_test:
    fr = open('cat_psjpeg.json')
    dict_load = json.load(fr)
    data_l = list(map(int, dict_load["data"]))
    code_l = dict_load["code"]
    dim_l = dict_load["dim"]
    mode_l = dict_load["mode"]
    img_recover = JPEG_extract(data_l, code_l, dim_l, mode_l)
    cv2.imwrite('cat_recover.jpg', img_recover)
    print('Image recovered from json file')

  # 4:2:2, 4:2:0 compression test
  if ycbcr_compress_test:
    mode = 420
    img_path = 'cat.jpg'
    img = cv2.imread(img_path)

    # compress and recover
    y, cb, cr = ycbcr_compress(img, mode)
    img_recover = ycbcr_recover(y, cb, cr, mode)

    cv2.imwrite('recover.jpg', img_recover)
    print('image recovered from YCbCr')

  # 8x8 DCT test
  if dct_test:
    rows = 18
    cols = 10
    mn = np.random.rand(rows, cols) * 255
    mn_dct = dct8x8(mn)
    mn_recover = idct8x8(mn_dct, rows, cols)
    #print(mn)
    #print(mn_recover)
    err_dct = mn_recover - mn
    print(np.average(err_dct))

  # quantization test
  if qtz_test:
    a = np.full((16, 8), 20000)
    a_q = qtz(a)
    a_iq = qtz(a_q, inverse=True)
    print(a_q)
    print(a_iq)

  # differential coding test
  if diff_code_test:
    b = np.random.rand(6, 6) * 100
    b = b.astype(int)
    b_enc = diff_enc(b)
    b_dec = diff_dec(b_enc)
    print(b_enc)
    print(np.sum(np.abs(b_dec - b)))

  # zigzag test
  if zigzag_test:
    lc = 5
    c = np.ones((lc, lc))
    for i in range(lc):
      for j in range(i + 1):
        c[i-j, j] = i + j
    zz = zigzag(c)
    izz = inv_zigzag(zz, lc)
    print(c)
    print(zz)
    print(izz)

  # Huffman coding test
  if Huffman_code_test:
    d = np.random.rand(80,80) * 10
    d = d.astype(int)
    code, d_str = Huffman_enc(d)
    d_restore = Huffman_dec(d_str, code)
    print(code)
    print(np.sum(d_restore - d))

# ------------------------------------------------------------
# end
# ------------------------------------------------------------
