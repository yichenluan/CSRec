# -*- coding: utf-8 -*-

import numpy as np
import time

from CSRec.DataView.filetrust_data import build_rating_data
from CSRec.DataView.filetrust_data import build_rating_matix


def matix_factorization(R, K):
    N = len(R)  # 用户数
    M = len(R[0])  # 项目数

    P = np.random.rand(N, K)
    Q = np.random.rand(M, K)

    new_P, new_Q = mf_handler(R, N, M, P, Q, K)
    # newR = np.dot(new_P, new_Q.T)
    new_R = np.dot(new_P, new_Q.T)
    return new_R


def mf_handler(R, N, M, P, Q, K, steps=5000, alpha=0.0002, beta=0.02):
    Q = Q.T

    loss = 0
    for step in xrange(steps):
        for i in xrange(N):
            for j in xrange(M):
                if R[i][j] <= 0:
                    continue
                eij = R[i][j] - np.dot(P[i, :], Q[:, j])
                for k in xrange(K):
                    P[i][k] += alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                    Q[k][j] += alpha * (2 * eij * P[i][k] - beta * Q[k][j])

        last_loss = loss
        loss = 0
        for i in xrange(N):
            for j in xrange(M):
                if R[i][j] <= 0:
                    continue
                loss += pow(R[i][j] - np.dot(P[i, :], Q[:, j]), 2)
                for k in xrange(K):
                    loss += (beta / 2) * (pow(P[i][k], 2) + pow(Q[k][j], 2))

        if abs(loss - last_loss) < 0.001:
            break
        print step

    return P, Q.T


if __name__ == '__main__':
    mac_path = '/Users/hunter/repos/g_project/datasets/filmtrust/'
    data_path = mac_path + 'ratings.txt'
    rating_data = build_rating_data(data_path)
    rating_matix = build_rating_matix(rating_data)
    print 'begin'

    begin = time.time()
    matix_factorization(rating_matix, 10)
    end = time.time()
    print begin-end
