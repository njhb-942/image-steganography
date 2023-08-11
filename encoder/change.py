# coding:utf-8
import numpy as np
import restore
    
def reorder_index(ind_in):
# This function is used to reorder the index of element for a given index-vector,
# then return the reorder index
# N is a number, it represents the number of row and column for matrix
    N = ind_in.size
    if np.mod(N,2) == 0:
        M = N
    else:
        M = N - 1
    
    # 相邻位置交换，如[1,2,3,4,5,6,7,8,9,10]-->[2,1,4,3,6,5,8,7,10,9]
    ind1 = np.array(ind_in)
    for i in np.arange(0, M):
        if np.mod(i, 2) == 0:
            ind1[i] = ind_in[i + 1]
        else:
            ind1[i] = ind_in[i - 1]
    
    # 前半段的偶数位置与后半段奇数位置交换，[2,1,4,3,6,   5,8,7,10,9]-->[2,10,4,8,6    5,3,7,1,9]
    ind2 = ind1.copy()
    for i in np.arange(0, int(M / 2)):
        if np.mod(i, 2) == 1:
            ind2[i] = ind1[M - i - 1]
            ind2[M - i - 1] = ind1[i]
    
    # 将数组分为四段，第一三段镜像倒换
    ind3 = ind2.copy()
    for i in np.arange(0, int(M / 4)):
        j = 2 * int(M / 4) + i
        ind3[i] = ind2[j]
        ind3[j] = ind2[i]
    

    # 将数组分为两段，前后偶数位置互换
    ind4 = ind3.copy()
    for i in np.arange(0, int(M / 2)):
        if np.mod(i, 2) == 0:
            ind4[i] = ind3[M - i - 1]
            ind4[M - i - 1] = ind3[i]
    
    index = ind4.copy()
    # 将数组分为四段，第二四段镜像倒换
    for i in np.arange(0, int(M / 4)):
        index[i + int(M / 4)] = ind4[M - 1 - i]
        index[M - 1 - i] = ind4[i + int(M / 4)]

    
    sort_index =sorted(index)
    return index

if __name__ == '__main__':
    ind_in = np.arange(0, 10)
    for i in np.arange(0, 5):
        ind_in = reorder_index(ind_in)

    re_ind = restore.recover_index(ind_in)
    print(re_ind)


