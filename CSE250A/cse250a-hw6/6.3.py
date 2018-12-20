import numpy as np
import math

def read_X(file):
    f = open(file, 'r')
    X = []
    data = [line.strip('\n') for line in f.readlines()]
    for i in data:
        i = i.split(" ")
        cur = []
        for j in i:
            cur.append(int(j))
        X.append(cur)
    return X


def read_Y(file):
    f = open(file, 'r')
    Y = []
    data = [line.strip('\n') for line in f.readlines()]
    for i in data:
        Y.append(int(i))
    return Y


def noise_OR(x, y, p):
    part = 1
    for i in range(len(x)):
        part *= math.pow(1 - p[i], x[i])
    if y == 1:
        v = 1 - part
    else:
        v = part
    return v


def likelihood(x, y, p, iter):
    cur = 0
    flag = 0
    for i in range(len(x)):
        cur += math.log(noise_OR(x[i], y[i], p))
        if y[i] == 1 and noise_OR(x[i], y[i], p) <= 0.5:
            flag += 1
        if y[i] == 0 and 1 - noise_OR(x[i], y[i], p) >= 0.5:
            flag += 1
    print("iter : " + str(iter) + "\tnumber of mistakes M : " + str(flag))
    return float(cur) / len(x)


def EM(x, y, p):
    cur = np.zeros(len(p))
    cnt = np.zeros(len(p))
    for i in range(len(x)):
        for j in range(len(p)):
            if x[i][j] == 1:
                cnt[j] += 1
            cur[j] += y[i] * x[i][j] * p[j] / noise_OR(X[i], Y[i], p)
    cur /= cnt
    return cur


X = read_X('spectX.txt')
Y = read_Y('spectY.txt')

p = [1.0 / 23 for _ in range(len(X[0]))]

iter = {0, 1, 2, 4, 8, 16, 32, 64, 128, 256}
for i in range(257):
    if i in iter:
        print("iter : " + str(i) + "\tlog-likelihood : " + str(likelihood(X, Y, p, i)))
        print('=====================================================')
    p = EM(X, Y, p)
