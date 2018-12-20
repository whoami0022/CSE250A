def read_file(filename):
    file = open(filename, 'r')
    num = []
    for line in file.readlines():
        line = line.strip(' \n').split('\t')
        if len(line) == 1:
            line = line[0].split(' ')
        if len(line) > 1:
            num.append(list(map(float, line)))
        else:
            num.append(float(line[0]))
    return num
from math import log

a = read_file('hw7_transitionMatrix.txt')
b = read_file('hw7_emissionMatrix.txt')
initialP = read_file('hw7_initialStateDistribution.txt')
o = read_file('hw7_observations.txt')[0]
o = list(map(int, o))

l = []
base = [0] * 26
for i in range(26):
    base[i] = log(initialP[i]) + log(b[i][o[0]])
l.append(base)

T = len(o)
phi = []
for t in range(1, T):
    lline = [0] * 26
    phiTmp = [0] * 26
    for j in range(26):
        maxTmp = l[t-1][0] + log(a[0][j])
        for i in range(1, 26):
            if l[t-1][i] + log(a[i][j]) > maxTmp:
                maxTmp = l[t-1][i] + log(a[i][j])
                phiTmp[j] = i
        lline[j] = maxTmp + log(b[j][o[t]])
    phi.append(phiTmp)
    print(lline)
    l.append(lline)

maxTmp = l[T-1][0]
index = 0
for i in range(1, 26):
    if l[T-1][i] > maxTmp:
        maxTmp = l[T-1][i]
        index = i

S = [index]
i = T-2
while (i >= 0):
    index = phi[i][index]
    S = [index] + S
    i -= 1
output = open('state.txt', 'w')
for i in range(len(S)):
    output.write('%d\n' % (S[i]))