# Created with Python AI

# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 22:21:09 2020

@author: yuyuyu
"""

import numpy as np
import math
import matplotlib.pyplot as plt

def European_implicit(r, sigma, S_0,top, T, M, N):
    ds = top/M
    dt = T/N

    # 将 a_j, b_j, c_j 写为3个函数。
    a = lambda j: 0.5*r*j*dt-0.5*sigma*sigma*j*j*dt
    b = lambda j: 1+r*dt+sigma*sigma*j*j*dt
    c = lambda j: -0.5*r*j*dt-0.5*sigma*sigma*j*j*dt

    # f1 和 f2 为两列用来迭代计算的期权价格。
    f1 = [0]*(M+1);
    for i in range(M+1):
        if (i*ds < 40):
            f1[i] = 2
        elif (i*ds <= 60 and i*ds >=40):
            f1[i] = min(max(i*ds-50,0),2)
        elif (i*ds > 60):
            f1[i] = 5
    #print(f1)
    #print(len(f1))
    f2 = [None for i in range(M+1)]
    # coeffs 为上文中的 M 系数矩阵。
    coeffs = np.zeros((M-1, M-1))

    flag = 1
    for i in range(N-1, -1, -1):
        f2 = list(f1)
        coeffs[0][0] = b(1)
        coeffs[0][1] = c(1)
        coeffs[M-2][M-2] = b(M-1)
        coeffs[M-2][M-3] = a(M-1) 
        for j in range(2, M-1, 1):
            coeffs[j-1][j-2] = a(j)
            coeffs[j-1][j-1] = b(j)
            coeffs[j-1][j] = c(j)
        # 参数矩阵求逆。
        coeffs_inv = np.linalg.inv(coeffs)
        F2 = f2[1:-1]
        #print(f2)
        #print(len(f2))
        #print(F2)
        #print(len(F2))
        F2[0] -= a(1)*f1[0]
        F2[M-2] -= c(M-2)*f1[M]
        F1 = np.matmul(coeffs_inv, F2)
        f1[1:M] = F1
        f1[0] = 2*math.e**(-r/N*flag)
        f1[M] = 5*math.e**(-r/N*flag)
        flag += 1
        # 判断是否执行美式看跌期权。
        #f1 = np.maximum(f1, K-np.linspace(0, M, M+1)*dS)
        #print(f1)
    pos = int(S_0/ds)
    put_price = f1[pos] + (f1[pos+1]-f1[pos])/ds*(S_0-pos*ds)

    return put_price,f1

def plot_delta(f1,M,top,addr):
    ds = top/M
    delta = [0]*(len(f1)-2)
    S = [0]*(M-1)
    for i in range(len(f1)-2):
        delta[i] = (f1[i+1]-f1[i])/ds
        S[i] = i*ds
    #print(f1)
    #print(S)
    #print(delta)
    #print(len(S))
    #print(len(delta))    
    plt.figure()
    plt.xlabel('S')
    plt.ylabel('delta')
    plt.title('Delta of option price versus stock price')
    plt.plot(S,delta,color='r')
    plt.show()
    plt.savefig(addr)
    

# 计算例子。
if __name__ == "__main__":
    put_price,f1 = European_implicit(0.05, 0.4, 50, 150, 1.0, 300,300)
    print("European option price: {0:0.5f}".format(put_price))
    addr = ('C:/Users/yuyuyu/Desktop/option.png')    
    plot_delta(f1,300,150,addr)
