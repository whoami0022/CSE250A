#coding: utf-8
import random
import numpy as np
import matplotlib.pyplot as plt

def sample_distribution(p):
    if random.uniform(0, 1) < p:
        return '0'
    else:
        return '1'


def binary2decimal(key):
    decimal = 0
    for k in range(len(key)):
        decimal += int(key[k]) * (2 ** (len(key) - k - 1))
    return decimal


def calculate_weight(decimal, alpha, z):
    return (alpha ** abs(z - decimal)) * (1 - alpha)/(1 + alpha)


def sample_data(dic, p, n, alpha, z):
    binary = ''
    for j in range(n):
        sub_key = sample_distribution(p)
        binary += sub_key
    decimal = binary2decimal(binary)
    weight = calculate_weight(decimal, alpha, z)

    if binary in dic:
        dic[binary] += weight
    else:
        dic[binary] = weight
    return dic


def compute_target(dic, i, sum_all, sum_sub):
    for k in dic:
        sum_all += dic[k]
        if k[i] == '1':
            sum_sub += dic[k]
    return float(sum_sub)/sum_all


if __name__ == '__main__':
    N = 10
    ALPHA = 0.2
    Z = 128
    sample_amount = 200
    P = 0.5

    sum_all = 0
    sum_sub = [0 for _ in range(11)]
    dic = {}
    x = np.arange(1, sample_amount + 1)
    result2 = []
    result4 = []
    result6 = []
    result8 = []
    result10 = []

    for k in range(0, sample_amount):
        sample_data(dic, P, N, ALPHA, Z)
        #print(compute_target(dic, 2, sum_all, sum_sub))
        result2.append(compute_target(dic, N - 2, sum_all, sum_sub[2]))
        result4.append(compute_target(dic, N - 4, sum_all, sum_sub[4]))
        result6.append(compute_target(dic, N - 6, sum_all, sum_sub[6]))
        result8.append(compute_target(dic, N - 8, sum_all, sum_sub[8]))
        result10.append(compute_target(dic, N - 10, sum_all, sum_sub[10]))

    plt.figure(1)

    plt.plot(x, result2)
    plt.plot(x, result4)
    plt.plot(x, result6)
    plt.plot(x, result8)
    plt.plot(x, result10)

    print(result2[-1])
    print(result4[-1])
    print(result6[-1])
    print(result8[-1])
    print(result10[-1])

    plt.show()


