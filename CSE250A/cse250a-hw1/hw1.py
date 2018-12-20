#coding:utf-8
import random


def read_data(filename):
    f = open(filename,'r')
    raw_data = [i.strip('\n') for i in f.readlines()]
    data = {}
    for i in raw_data:
        data[i.split(' ')[0]] = int(i.split(' ')[1])
    return data


def compute_prior_prob(data):
    total = sum(data.values())
    prior_prob = {}
    for key, value in data.items():
        prior_prob[key] = float(value / total)
    return prior_prob


def compute_posterior_prob(present_string, absent_list, prior_prob):
    sorted_prior_prob = sorted(prior_prob.items(),
                                      key=lambda item: item[1], reverse=True)
    posterior_prob = {}
    total = 0
    for item in sorted_prior_prob:
        flag = 0
        for k in range(len(item[0])):
            if item[0][k] != present_string[k] \
                    and present_string[k] != '_':
                flag = 1
                break
        if flag == 1:
            continue

        for k in range(len(item[0])):
            if (item[0][k] in absent_list or item[0][k] in present_string) \
                    and present_string[k] == '_':
                flag = 1
                break
        if flag == 1:
            continue
        posterior_prob[item[0]] = item[1]
        total += item[1]
    for key, value in posterior_prob.items():
        posterior_prob[key] = value / total
    return posterior_prob


def compute_next_guess(posterior_prob):
    sorted_posterior_prob = sorted(posterior_prob.items(),
                                          key=lambda item: item[1], reverse= True)
    alphabet = [chr(i) for i in range(65, 91)]

    res = {}
    for i in alphabet:
        res[i] = 0
        if i not in present and i not in absent:
            for item in sorted_posterior_prob:
                if i in item[0]:
                    res[i] += item[1]
    res = sorted(res.items(), key=lambda item: item[1], reverse=True)
    return res

def print_first_15(prior_prob):
    sorted_prior_prob = sorted(prior_prob.items(),
                                      key=lambda item: item[1], reverse=True)
    print("The fifteen most frequent 5-letter words")
    for i in range(15):
        print(str(i + 1) + ' : ' + sorted_prior_prob[i][0])
    print('\n')


def print_last_14(prior_prob):
    sorted_prior_prob = sorted(prior_prob.items(),
                                      key=lambda item: item[1], reverse=True)
    print("The fourteen least frequent 5-letter words")
    n = len(sorted_prior_prob)
    for i in range(n - 1, n - 15, -1):
        print(str(i + 1) + ' : ' + sorted_prior_prob[i][0])
    print('\n')


if __name__ == '__main__':

    data = read_data('hw1_word_counts_05.txt')
    prior_prob = compute_prior_prob(data)
    print_first_15(prior_prob)
    print_last_14(prior_prob)

    present = '_U___'
    absent = ['A','E','I','O','S']
    posterior_prob = compute_posterior_prob(present, absent, prior_prob)
    res = compute_next_guess(posterior_prob)
    for k in res:
        print(k)