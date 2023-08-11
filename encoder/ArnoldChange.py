import numpy as np
from pylab import *
from PIL import Image



def arnold_encode(image, shuffle_times, a, b):
    """ Arnold shuffle for rgb image
    Args:
        image: input original rgb image
        shuffle_times: how many times to shuffle
    Returns:
        Arnold encode image
    """
    # 1:创建新图像
    arnold_image = np.zeros(shape=image.shape)

    # 2：计算N
    h, w = image.shape[0], image.shape[1]
    N = h  # 或N=w

    # 3：遍历像素坐标变换
    for time in range(shuffle_times):
        for ori_x in range(h):
            for ori_y in range(w):
                # 按照公式坐标变换
                new_x = (1 * ori_x + b * ori_y) % N
                new_y = (a * ori_x + (a * b + 1) * ori_y) % N

                arnold_image[new_x, new_y] = image[ori_x, ori_y]

    return arnold_image


def arnold_decode(image, shuffle_times, a, b):
    """ decode for rgb image that encoded by Arnold
    Args:
        image: rgb image encoded by Arnold
        shuffle_times: how many times to shuffle
    Returns:
        decode image
    """
    # 1:创建新图像
    decode_image = np.zeros(shape=image.shape)

    # 2：计算N
    h, w = image.shape[0], image.shape[1]
    N = h  # 或N=w

    # 3：遍历像素坐标变换
    for time in range(shuffle_times):
        for ori_x in range(h):
            for ori_y in range(w):
                # 按照公式坐标变换
                new_x = ((a * b + 1) * ori_x + (-b) * ori_y) % N
                new_y = ((-a) * ori_x + ori_y) % N
                decode_image[new_x, new_y] = image[ori_x, ori_y]
    return decode_image

if __name__ == '__main__':
    img0 = '用于隐藏水印的灰度图片的副本.jpeg'
    img_0 = np.array(Image.open(img0))
    img_af = arnold_encode(img_0, 7, 2, 2)
    Image.fromarray(np.array(img_af, dtype='uint8')).convert(mode='L').save(f'arnoldtest_af.jpeg', quality=100)
    img_re = arnold_decode(img_af, 7, 2, 2)
    Image.fromarray(np.array(img_re, dtype='uint8')).convert(mode='L').save(f'arnoldtest_re.jpeg', quality=100)
    print((img_0 == img_re).all())
