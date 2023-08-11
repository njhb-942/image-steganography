import os

import numpy as np
from PIL import Image

im = Image.open('用于隐藏水印的灰度图片.jpeg')
img = np.array(im)

Image.fromarray(np.array(img, dtype='uint8')).convert(mode='L').save('用于隐藏水印的灰度图片.png')