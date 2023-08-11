# coding:utf-8
import numpy as np
    
def recover_index(ind_in):
    N = ind_in.size
    if np.mod(N, 2) == 0:
        M = N
    else:
        M = N - 1

    ind1 = np.array(ind_in)
    # 将数组分为四段，第二四段镜像倒换
    for i in np.arange(0, int(M / 4)):
        ind1[i + int(M / 4)] = ind_in[M - 1 - i]
        ind1[M - 1 - i] = ind_in[i + int(M / 4)]

    # 将数组分为两段，前后偶数位置互换
    ind2 = ind1.copy()
    for i in np.arange(0, int(M / 2)):
        if np.mod(i, 2) == 0:
            ind2[i] = ind1[M - i - 1]
            ind2[M - i - 1] = ind1[i]

    # 将数组分为四段，第一三段镜像倒换
    ind3 = ind2.copy()
    for i in np.arange(0, int(M / 4)):
        j = 2 * int(M / 4) + i
        ind3[i] = ind2[j]
        ind3[j] = ind2[i]

    # 前半段的偶数位置与后半段奇数位置交换
    ind4 = ind3.copy()
    for i in np.arange(0, int(M / 2)):
        if np.mod(i, 2) == 1:
            ind4[i] = ind3[M - i - 1]
            ind4[M - i - 1] = ind3[i]

    # 相邻位置交换，如[1,2,3,4,5,6,7,8,9,10]-->[2,1,4,3,6,5,8,7,10,9]
    index = ind4.copy()
    for i in np.arange(0, M):
        if np.mod(i, 2) == 0:
            index[i] = ind4[i + 1]
        else:
            index[i] = ind4[i - 1]

    return index
    
if __name__ == '__main__':
    ind_in = np.arange(0, 10)
    recover_index(ind_in)