import numpy as np
import qrcode  # 加载二维码生成库
from pylab import *
import os
from PIL import Image
import shutil
import decoder
import change
import restore

def arnold_encode(image, shuffle_times, a, b):
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


def ReadFile(file_path):
    """
    读取文件内容, 按行返回list \n
    :param file_path: 文件地址
    :return: list_str 内容列表
    """
    fp = open(file_path, "r", encoding="utf-8", errors="ignore")
    list_str = fp.readlines()
    return list_str


def judgement(file_path, limit_length):
    """
    根据文件字符数量进行分段操作 \n
    :param limit_length: 字符长度上限
    :param file_path: 文件地址
    :return: 内容列表 list_str, 断点 list_split
    """
    list_str = ReadFile(file_path)
    list_split = []
    count = 0

    # 字符数每超过1000, 就记录一次中断点位置
    for index, item in enumerate(list_str):
        count += len(item)
        if count > limit_length:
            list_split.append(index-1)  # -1才是真正的最后一行字符串
            count = len(list_str[index])  # 从中断处重新计算长度

    list_split.append(len(list_str) - 1)  # 加上最后一行的下标
    return list_str, list_split


def mycopyfile(srcfile, dstpath, outname):  # 复制函数
    if not os.path.isfile(srcfile):
        print("%s not exist!" % (srcfile))
    else:
        fpath, fname = os.path.split(srcfile)  # 分离文件名和路径
        name, format = fname.split('.')
        outname = f'{outname}.{format}'
        if not os.path.exists(dstpath):
            os.makedirs(dstpath)  # 创建路径
        shutil.copy(srcfile, dstpath + outname)  # 复制文件
        print("copy %s -> %s" % (srcfile, dstpath + outname))


def MakeQrcode(original_fileName, limit_length, size):
    """
    生成二维码图片 \n
    :param original_fileName: 原始文件名和格式
    :param ImageName: 图片名
    :param file_path: 数据文件地址
    :param limit_length: 字符长度上限
    :return: ImageList: 二维码图片地址列表
    """

    # 断言, 原始文件名必须包含格式
    # assert ".py" in original_fileName, "fileName must contain '.py'"
    # 初始化构造器  error_correction 容错等级
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=2,
        border=4,
    )
    count = 0
    list_str, list_split = judgement(original_fileName, limit_length)
    ImageList = []

    # 根据断点, 截取数据生成二维码
    for index, item in enumerate(list_str):
        qr.add_data(item)
        if index == list_split[len(list_split) - 1]:
            qr.add_data(original_fileName + '\n')
        if index in list_split:
            qr.add_data(count)
            qr.make(fit=True)
            # img = qr.make_image() # 使用make方法生成二维码，第一个参数是要存储的数据，可以是字符串等类型
            # img.save(f'qr{count}.png')  # 这一部分的内容可以单独提取出来做成一个path
            img = np.array(qr.make_image().get_image().resize((size, size)), dtype='uint8') * 255
            # h_index = change.reorder_index(np.arange(0, img.shape[0])).tolist()
            # for i in range(0, img.shape[0]):
            #     img[i] = img[i][h_index]
            # ImageList.append(f'{ImageName}{count}.png')
            count += 1
            ImageList.append(img)
            qr.clear()
    return ImageList

def get_size(filename):
    # Obtain the file size: KB
    size = os.path.getsize(filename)
    return size / 1024

# 压缩图片文件
def compress_image(img_path, out_path, mb=74, step=1, quality=100):
    """不改变图片尺寸压缩图像大小
    :param img_path: 压缩图像读取地址
    :param out_path: 压缩图像存储地址
    :param mb: 压缩目标，KB
    :param step: 每次调整的压缩比率
    :param quality: 初始压缩比率
    :return: 压缩文件地址，压缩文件大小
    """
    o_size = get_size(img_path)
    if o_size <= mb:
        return -1

    img = Image.open(img_path)

    while o_size > mb:
        img = Image.open(img_path)
        img = img.convert('L')
        img.save(out_path, quality=quality)
        if quality - step < 0:
            break
        quality -= step
        o_size = get_size(out_path)

    os.remove(img_path)
    print('压缩后文件大小(kb): ' + str(o_size))
    return quality

def getEncodeImg(image_list, img0, change, kb):
    count = 1
    # threshold = 255 - change
    threshold = change

    out_path = 'out'
    if os.path.exists(out_path):
        shutil.rmtree(out_path)
        os.mkdir(out_path)
    else:
        os.mkdir(out_path)

    # 先返回原图
    if image_list.__len__() != 0:
        mycopyfile(img0, 'out/', '0')

    img0 = np.array(Image.open(img0), dtype='uint8')

    for index, QR0 in enumerate(image_list):
        if count == 1:
            Image.fromarray(np.array(QR0, dtype='uint8')).convert(mode='L').save('加密前1.png')
        QR0 = np.array(np.where(QR0 == 0, change, 0), dtype='uint8')
        # QR0 = np.array(arnold_encode(QR0, 4, 1, 1), dtype='uint8')
        img0_af = np.where(img0 > threshold, img0 - change, img0)
        # 加密
        QR0_length = QR0.shape[0]
        h = img0.shape[0]
        l = img0.shape[1]
        img0_af[:QR0_length, :QR0_length] += QR0
        # 补充剩余部分噪声背景
        rdm_index = np.random.permutation(l - QR0.shape[0])
        img0_af[:h, QR0_length:l] += QR0[:, rdm_index]
        # 写回加密后的图片
        # cv2.imwrite('加密后未压缩.jpeg', np.array(img0_af, dtype='uint8'), (cv2.IMWRITE_JPEG_QUALITY, 100))
        Image.fromarray(np.array(img0_af, dtype='uint8')).convert(mode='L').save(f'{out_path}/加密后未压缩{count}.jpeg', quality=100)
        # Image.fromarray(np.array(img0_af)).save("test01.png")
        quality = compress_image(f'{out_path}/加密后未压缩{count}.jpeg', f'{out_path}/{count}.jpeg', mb=kb)
        if quality != -1:
            os.remove(f'{out_path}/{count}.jpeg')
            Image.fromarray(np.array(img0_af, dtype='uint8')).convert(mode='L').save(f'{out_path}/{count}.jpeg', quality=quality)
        print("压缩后的文件名："+f'{out_path}/{count}.jpeg')
        print('=========')
        count += 1

if __name__ == '__main__':
    # 读取原图片以及其像素大小、磁盘大小
    img0 = '用于隐藏水印的灰度图片.jpeg'
    img0_kb = get_size(img0) * 1.05
    h = np.array(Image.open(img0), dtype='uint8').shape[0]
    l = np.array(Image.open(img0), dtype='uint8').shape[1]
    size = np.where(h > l, l, h)

    # 读取要加密的文件
    original_fileName = 'secret.py'

    # 设置单个二维码存储最大字符，并生成对应二维码列表
    limit_length = 1000
    image_list = MakeQrcode(original_fileName, limit_length, size)

    # 设置隐写程度超参数，并生成加密后的图片
    change = 3
    getEncodeImg(image_list, img0, change, img0_kb)
    # print(image_list)

    # 查看本次加密后是否能完整读出信息
    decoder.decode('out')
    print("加密成功！！")
    os.remove(f'out/{original_fileName}')




