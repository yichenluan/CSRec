# -*- coding: utf-8 -*-
import time
import numpy as np

from CSRec.DataView.common import read_file


mac_path = '/Users/hunter/repos/g_project/datasets/filmtrust/'
forhead_path = mac_path


def build_rating_data(data_path):
    f_content = read_file(data_path)
    rating_data = list()
    for line in f_content:
        line_data = line.split(' ')
        rating_data.append(
                [int(line_data[0]), int(line_data[1]), float(line_data[2])]
                )
    return rating_data


def build_trust_data():
    f_path = forhead_path + 'trust.txt'
    f_content = read_file(f_path)
    trust_data = [[int(i) for i in line.split(' ')] for line in f_content]
    return trust_data


def build_rating_matix(rating_data):
    matix = np.zeros((1508, 2071))
    for line in rating_data:
        matix[line[0]-1][line[1]-1] = line[2]
    return matix


def build_rating_dict(rating_data):
    rating_dict = dict()
    for line in rating_data:
        if (line[0]-1) not in rating_dict:
            rating_dict[line[0]-1] = [line[1]-1]
        else:
            rating_dict[line[0]-1].append(line[1]-1)
    return rating_dict


def build_trust_dict(trust_data):
    trust_dict = dict()
    for line in trust_data:
        if line[0] > 1508 or line[1] > 1508:
            continue
        if (line[0]-1) not in trust_dict:
            trust_dict[line[0]-1] = [line[1]-1]
        else:
            trust_dict[line[0]-1].append(line[1]-1)
    return trust_dict


def build_trust_matix(trust_data):
    matix = np.zeros((1508, 1508))
    for line in trust_data:
        if line[0] > 1508 or line[1] > 1508:
            continue
        matix[line[0]-1][line[1]-1] = line[2]
    return matix


if __name__ == '__main__':
    data_path = forhead_path + 'ratings.txt'
    data_begin = time.time()
    rating_data = build_rating_data(data_path)
    trust_data = build_trust_data()
    data_end = time.time()
    print 'data: ' + str(data_end - data_begin)
    print rating_data[0], rating_data[-1]
    print trust_data[0], trust_data[-1]

    matix_begin = time.time()
    matix = build_rating_matix(rating_data)
    matix_end = time.time()
    print 'matix: ' + str(matix_end - matix_begin)
    print matix[0][6]
