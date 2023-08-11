import os

import numpy as np
from PIL import Image
import change
import restore

im = Image.open('qr0.png').resize((600, 600))
img = np.array(im, dtype='uint8') * 255
cg_index = change.reorder_index(np.arange(0, img.shape[0])).tolist()
for i in range(0, img.shape[0]):
    img[i] = img[i][cg_index]
Image.fromarray(np.array(img, dtype='uint8')).save('cg_img.png')

cg_im = Image.open('cg_img.png')
cg_img = np.array(cg_im, dtype='uint8')
re_index = restore.recover_index(np.arange(0, cg_img.shape[0])).tolist()
for i in range(0, cg_img.shape[0]):
    cg_img[i] = cg_img[i][re_index]
Image.fromarray(np.array(cg_img, dtype='uint8')).save('re_img.png')

