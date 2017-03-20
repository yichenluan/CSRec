# -*- coding: utf-8 -*-

import numpy
import time


def mf(R, P, Q, K, steps=10000, alpha = 0.0002, beta=0.02):
    Q = Q.T
    for step in range(steps):
        for i in range(len(R)):
            for j in range(len(R[i])):
                if R[i][j] > 0:
                    eij = R[i][j] - numpy.dot(P[i, :], Q[:, j])
                    for k in range(K):
                        P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                        Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
        eR = numpy.dot(P, Q)
        e = 0
        for i in range(len(R)):
            for j in range(len(R[i])):
                if R[i][j] > 0:
                    e = e + pow(R[i][j] - numpy.dot(P[i, :], Q[:, j]), 2)
                    for k in range(K):
                        e = e + (beta/2) * (pow(P[i][k], 2) + pow(Q[k][j], 2))
        if e < 0.001:
            break
        if step % 1000 == 0:
            print e

    return P, Q.T


if __name__ == '__main__':

    R = [
            [5, 3, 0, 1],
            [4, 0, 0, 1],
            [1, 1, 0, 5],
            [1, 0, 0, 4],
            [0, 1, 5, 4],
            ]
    R = numpy.array(R)
    N = len(R)
    M = len(R[0])
    K = 2

    P = numpy.random.rand(N, K)
    Q = numpy.random.rand(M, K)

    begin_t = time.time()
    nP, nQ = mf(R, P, Q, K)
    end_t = time.time()
    nR = numpy.dot(nP, nQ.T)
    print nR
    print '---'
    print end_t-begin_t