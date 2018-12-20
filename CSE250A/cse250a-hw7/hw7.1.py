import sys

def read_file(filename):
    f = open(filename, 'r')
    data = []
    for line in f.readlines():
        line = line.strip('\n')
        line = line.split('\t')
        temp = []
        if len(line) == 1:
            items = line[0].split(' ')

            for k in items:
                temp.append(float(k))
        else:
            for k in line:
                temp.append(float(k))
        if len(temp) == 1:
            data.append(temp[0])
        else:
            data.append(temp)

    return data

transition_matrix = read_file('hw7_transitionMatrix.txt')
emission_matrix = read_file('hw7_emissionMatrix.txt')
initial_state = read_file('hw7_initialStateDistribution.txt')
observations = read_file('hw7_observations.txt')[0]

import math
M = len(transition_matrix)
N = len(observations)

temp = []
for i in range(M):
    temp.append(math.log(initial_state[i]) + math.log(emission_matrix[i][int(observations[0])]))

l = []
l.append(temp)

index_all = []
for i in range(1, N):
    temp = []
    index = [0] * M
    for j in range(M):
        max = float('-inf')
        for k in range(M):
            if l[i - 1][k] + math.log(transition_matrix[k][j]) > max:
                max = l[i - 1][k] + math.log(transition_matrix[k][j])
                index[j] = k
        temp.append(max + math.log(emission_matrix[j][int(observations[i])]))

    index_all.append(index)

    l.append(temp)

#backtrack
max = float('-inf')
index = 0
for i in range(M):
    if l[N - 1][i] > max:
        max = l[N - 1][i]
        index = i

S = [index]

for i in range(N - 2, -1, -1):
    index = index_all[i][index]
    S = [index] + S

output = open('state.txt', 'w')
for i in range(len(S)):
    output.write('%d\n' % (S[i]))






