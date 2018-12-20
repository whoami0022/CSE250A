f = open('state.txt','r')
data = [i.strip('\n') for i in f.readlines()]

s = []
s.append(int(data[0]))
for k in range(1, len(data)):
    if data[k] != data[k - 1]:
        s.append(int(data[k]))

import matplotlib.pyplot as plt
import numpy as np
#%matplotlib inline
# x = np.arange(0, len(data))
# y = np.asarray(data)
# plt.plot(x, y)
# plt.show()
res = ''
for k in s:
    if k + 97 < 123:
        res += chr(k + 97)
    else:
        res += ' '
print(res)