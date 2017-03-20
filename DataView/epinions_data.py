# -*- coding: utf-8 -*-
import time
import numpy as np

from CSRec.DataView.common import read_file

mac_path = '/Users/hunter/repos/g_project/datasets/Epinions/'
forhead_path = mac_path


def build_rating_data(data_path):
    f_content = read_file(data_path)[1:-1]
    rating_data = [[int(i) for i in line.split(' ')] for line in f_content]
    return rating_data


def build_trust_data():
    f_path = forhead_path + 'trust_data.txt'
    f_content = read_file(f_path)[1:-1]
    trust_data = [[int(i) for i in line[1:].split(' ')] for line in f_content]
    return trust_data


def build_rating_matix(rating_data):
    matix = np.zeros((49289, 139738))
    for line in rating_data:
        matix[line[0]-1][line[1]-1] = line[2]
    return matix


if __name__ == '__main__':
    data_path = forhead_path + 'ratings_data.txt'
    data_begin = time.time()
    rating_data = build_rating_data(data_path)
    # trust_data = build_trust_data()
    data_end = time.time()
    print 'data: ' + str(data_end - data_begin)

    matix_begin = time.time()
    matix = build_rating_matix(rating_data)
    matix_end = time.time()
    print 'matix: ' + str(matix_end - matix_begin)
