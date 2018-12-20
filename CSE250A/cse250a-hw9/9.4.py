import numpy as np


def load_rewards(file_name):
    f = open(file_name, 'r')
    rewards = [int(line.strip('\n')) for line in f.readlines()]
    return rewards


def load_matrix(file_name):
    matrix = np.zeros((81, 81))
    f = open(file_name, 'r')
    for i in f.readlines():
        i = i.split()
        matrix[int(i[0]) - 1][int(i[1]) - 1] = float(i[2])
    return matrix


rewards = load_rewards('rewards.txt')
rewards = np.matrix(rewards).reshape(81, 1)

m1 = load_matrix('prob_a1.txt')
m2 = load_matrix('prob_a2.txt')
m3 = load_matrix('prob_a3.txt')
m4 = load_matrix('prob_a4.txt')


# for k in range(len(m1) - 1):
#     print(sum(m1[k]))

action_all = [m1, m2, m3, m4]

N = len(m1[0])

decay = 0.99


def max_value_and_action(action, s, prev_v):
    max_v = float('-inf')
    max_a = -1
    for i in range(4):
        vp = 0
        for k in range(N):
            vp += action[i][s][k] * prev_v[k]
        if vp > max_v:
            max_v = vp
            max_a = i
    return max_v, max_a


p = np.zeros(N)
value = np.zeros(N)

for _ in range(20):
    pp = np.zeros((N, N))
    for i in range(N):
        a = p[i]
        pp[i] = action_all[int(a)][i]

    prev_v = np.matrix(np.identity(N) - decay * pp).getI() * rewards

    for i in range(N):
        max_v, max_a = max_value_and_action(action_all, i, prev_v)
        value[i] = rewards[i][0] + decay * max_v
        p[i] = max_a

#value, p

k = 0
pic = np.zeros((9, 9))
for i in range(9):
    for j in range(9):
        pic[i, j] = value[k].item(0)
        k += 1

pic = pic.T

#
# p = p.T
# print(p)