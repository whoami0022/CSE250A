import numpy as np
from sklearn.utils import shuffle
import matplotlib.pyplot as plt

def read_data(file, label):
    f = open(file, 'r')
    raw_data = [item.strip('\n') for item in f.readlines()]
    X = []
    y = []
    for row in raw_data:
        row = [float(i) for i in row.split()]
        X.append(row)
        y.append(label)
    return X, y


def sigmoid(x):
    return 1.0 / (1 + np.exp(-x))


def initialize_weights(n_features):
    limit = np.sqrt(1 / n_features)
    w = np.random.uniform(-limit, limit, (n_features, 1))
    return w


def gradient_descent(x, y, alpha, MAX_EPOCH):
    x_m = np.mat(x)
    y_m = np.mat(y).transpose()
    m, n = np.shape(x_m)
    l = np.sqrt(1 / n)
    w = np.random.uniform(-l, l, (n, 1))

    mse = []
    for i in range(MAX_EPOCH):
        error = y_m - sigmoid(np.dot(x_m, w))
        if (i % 10 == 0):
            mse.append(float(np.sum(np.power(error, 2)))/len(error))
        #print(i, mse)
        w += alpha * x_m.transpose() * error

    return w, np.array(mse)


def predict(x, y, w):
    size = len(y)
    count = 0
    y_predict = []

    for i in range(size):
        if sum([x[i][j] * w[j] for j in range(len(w))]) > 0:
            y_predict.append(1)
        else:
            y_predict.append(0)
        if y_predict[i] == y[i]:
            count += 1

    print(count / float(size))
    return count / float(size)

MAX_EPOCH = 5000
X3, y3 = read_data('new_train3.txt', 0)
X5, y5 = read_data('new_train5.txt', 1)

X = np.array(X3 + X5)
y = np.array(y3 + y5)
X, y = shuffle(X, y)

w, mse = gradient_descent(X, y, 0.001, MAX_EPOCH)
print(w.reshape(8, 8))

plt.title('train error')
plt.xlabel('iter')
plt.ylabel('MSE')
epoch = range(0, MAX_EPOCH, 10)
plt.plot(epoch, mse)
plt.show()

X3_test, y3_test = read_data('new_test3.txt', 0)
X5_test, y5_test = read_data('new_test5.txt', 1)
X_test = np.array(X3_test + X5_test)
y_test = np.array(y3_test + y5_test)
accuracy = predict(X_test, y_test, w)



