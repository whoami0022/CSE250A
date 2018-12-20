import math
import numpy as np
T = 269

def read_file(filename):
    f = open(filename, 'r')
    data = []
    for line in f.readlines():
        line = line.strip('\n').split()
        if len(line) == 1:
            data.append(line[0])
        else:
            data.append(line)

    return data

rating = read_file('hw8_ratings_fa18.txt')
title = read_file('hw8_movieTitles_fa18.txt')
pid = read_file('hw8_studentPIDs_fa18.txt')

movie_popularity = {}
for i in range(len(title)):
    movie_popularity[title[i]] = 0
    amount = 0
    for j in range(len(rating)):
        if rating[j][i] != '?':
            amount += 1
        if rating[j][i] == '1':
            movie_popularity[title[i]] += 1
    movie_popularity[title[i]] /= float(amount)

movie_popularity = sorted(movie_popularity.items(), key=lambda item: item[1])
print(len(movie_popularity))
for k in movie_popularity:
    print(k)

def read_file_EM(filename):
    f = open(filename, 'r')
    data = []
    for line in f.readlines():
        line = line.strip('\n').split()
        line = list(map(float, line))
        if len(line) == 1:
            data.append(line[0])
        else:
            data.append(line)

    return data

init_z = read_file_EM('hw8_probZ_init.txt')
init_z_given_r = read_file_EM('hw8_probRgivenZ_init.txt')

print(init_z)
print(init_z_given_r)

Iter = 128

p = init_z
conditional_p = init_z_given_r

def compute_likelihood(p, conditional_p, rating_t, index=0):
    l = 0
    ind = 0
    for i in range(len(p)):
        cur = p[i]
        for j in range(len(rating_t)):
            if rating_t[j] == '1':
                cur *= conditional_p[j][i]
            if rating_t[j] == '0':
                cur *= (1 - conditional_p[j][i])
        l += cur
        if i == index:
            ind = cur
    return (l, ind)


def compute_log_likelihood(p, conditional_p, rating):
    res = 0
    for t in range(T):
        res += math.log(compute_likelihood(p, conditional_p, rating[t], 0)[0])
    return res/float(T)


def compute_posterior(p, conditional_p, rating):
    post = np.zeros((len(rating), len(p)))
    for i in range(len(p)):
        for t in range(len(rating)):
            cur, ind = compute_likelihood(p, conditional_p, rating[t], i)
            post[t][i] = ind / cur
    return post

compute_log_likelihood(p, conditional_p, rating)


def EM(p, conditional_p, rating):
    post = compute_posterior(p, conditional_p, rating)
    for i in range(len(p)):
        total = sum(list(post[:, i]))
        p[i] = total / len(rating)
        for j in range(len(conditional_p)):
            conditional_p_cur = []
            for r in rating[:, j]:
                if r == '?':
                    conditional_p_cur.append(conditional_p[j][i])
                else:
                    conditional_p_cur.append(int(r))
            conditional_p_cur = np.array(conditional_p_cur)
            conditional_p[j][i] = np.dot(post[:, i], conditional_p_cur)/total
    return p, conditional_p

iter = 129
k = 0
rating = np.array(rating)
t = 0
print('iter 0' + ': %.4f' % compute_log_likelihood(p, conditional_p, rating))
while k < iter:
    if k == pow(2, t):
        print('iter ' + str(k) + ': %.4f' % compute_log_likelihood(p, conditional_p, rating))
        t += 1

    p, conditional_p = EM(p, conditional_p, rating)
    k += 1

###########
print(pid[140])

id = 140
guess_list = {}
for i in range(len(rating[0])):
    if rating[id][i] == '?':
        guess = 0
        for t in range(4):
            cur, ind = compute_likelihood(p, conditional_p, rating[id], t)
            guess += conditional_p[i][t] * ind / cur
        guess_list[title[i]] = guess

guess_list = sorted(guess_list.items(), key=lambda item:item[1], reverse=True)
for k in guess_list:
    print(k)