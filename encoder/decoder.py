import cv2
import numpy as np
import os
from PIL import Image
import restore
import change
import ArnoldChange

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

def Decoder(img):
    """
    调用微信二维码API解析二维码图片 \n
    :param img: 二维码图片地址-string
    :return: 包含二维码内容的 tuple
    """
    detect_obj = cv2.wechat_qrcode_WeChatQRCode()
    # im = cv2.imread(img)
    code_list, points = detect_obj.detectAndDecode(np.array(img, dtype='uint8'))
    return code_list


def GetContentList(imageList):
    """
    解析二维码图片, 并将其内容逐行进行拆分 \n
    :param imageList: 二维码图片地址列表-list
    :return: contentList: 所有二维码内容的嵌套列表
    """
    contentList = []
    for img in imageList:
        # img = np.array(ArnoldChange.arnold_decode(img, 4, 1, 1), dtype='uint8')
        # h_index = restore.recover_index(np.arange(0, img.shape[0])).tolist()
        # for i in range(0, img.shape[0]):
        #     img[i] = img[i][h_index]
        content = Decoder(img)
        contents = content[0].split('\n')
        contentList.append(contents)
    return contentList


def WriteToOriginFile(imageList):
    """
    将二维码内容写入原始文件 \n
    :param imageList: 二维码图片地址列表-list
    :return: 包含全部正确顺序二维码内容txt文件
    """
    contentList = GetContentList(imageList)
    # 排序, 以每个二维码最后一行的数字进行排序
    contentList.sort(key= lambda contentList:int(contentList[len(contentList)-1]), reverse=False)
    fileName = contentList[len(contentList) - 1][-2]  # 获取文件名——最后一个二维码信息中的倒数第二行的内容
    file = open(f'out/{fileName}', 'w')
    # 这里的逻辑是：contentList中包含已经按照信息中隐藏的数据，排好序的数据集合(其大小为二维码的数量)
    # 然后，遍历contentList，得到每一张二维码的内容(二维码已正确排序)contents，index为行号，content为行内容
    # 将contents非最后一行的数据，全部写入原始文件。最后一行包含的是排序信息。最终遍历完所有二维码，达到隐藏内容
    for contents in contentList:
            for index, content in enumerate(contents):
                if content == fileName:
                    continue  # 当执行到最后一个二维码内容的倒数第二行时，会读取到文件名，该文件名不需要再写入文件
                if index != len(contents) - 1:
                    file.write(content + '\n')
    file.close()

def getImgs(img_list):
    b = img_list[:]
    for i in img_list:
        if i.startswith('.') or i.endswith('.txt'):
            b.remove(i)
    img_list = b

    # 获取原始图片size
    ys = np.array(Image.open(f'out/{img_list[0]}'), dtype='int64')
    h = ys.shape[0]
    l = ys.shape[1]

    imgs = []
    for img_path in img_list:
        img = np.array(Image.open(f'out/{img_path}'), dtype='int64')
        if img.shape != ((l, h)):
            img = np.array(Image.open(f'out/{img_path}').resize((l, h)), dtype='int64')
        imgs.append(img)
    return imgs

def decode(out_path):
    # 处理整个加密后的文件夹
    img_list = sorted(os.listdir(out_path))
    imgs = getImgs(img_list)

    # 读取原始图片和加密后图片
    ys = imgs[0]
    jmh = imgs[1:]
    QR0_length = np.min(ys.shape)
    jmh = np.array(jmh)

    # 解密后的波动
    # qr = jmh - np.where(ys > threshold, ys - change, ys) + change

    # 解密成矩阵
    qr = ys[:QR0_length, :QR0_length] - jmh[:, :QR0_length, :QR0_length]
    change = np.mean(qr) * 2
    out = np.where(qr < (change * 0.5), 0, 255)
    Image.fromarray(np.array(out[0], dtype='uint8')).convert(mode='L').save('解密后1.png')
    # cv2.imwrite('out1.png', out[0, :, :])
    # cv2.imwrite('out2.png', out[1, :, :])
    # cv2.imwrite('out3.png', out[2, :, :])
    # cv2.imwrite('out4.png', out[3, :, :])
    # cv2.imwrite('out5.png', out[4, :, :])

    # 用二维码矩阵列表解密并整合成完整文件
    WriteToOriginFile(out)

if __name__ == '__main__':
    # 指定加密后包含加密后图片的文件夹
    decode('out')
    print("解密成功！！")
