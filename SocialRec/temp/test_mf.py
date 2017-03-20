# -*- coding: utf-8 -*-

import time
import numpy as np


def mf(R, P, Q, N, M, K, step=10000, alpha=0.0002, beta=0.02):
    for s in xrange(step):
        for i in range(N):
            for j in range(M):
                if R[i][j] > 0:
                    error = R[i][j]
                    for k in range(K):
                        error -= P[i][k] * Q[k][j]
                    for k in range(K):
                        P[i][k] += alpha * (2 * error * Q[k][j] - beta * P[i][k])
                        Q[k][j] += alpha * (2 * error * P[i][k] - beta * Q[k][j])
        loss = 0.0
        for i in range(N):
            for j in range(M):
                if R[i][j] > 0:
                    error = 0
                    for k in range(K):
                        error += P[i][k] * Q[k][j]
                    loss += pow(R[i][j]-error, 2)
                    for k in range(K):
                        loss += (beta/2) * (pow(P[i][k], 2) + pow(Q[k][j], 2))

        if loss < 0.001:
            break
        if (s % 1000 == 0):
            print loss


if __name__ == '__main__':
    R = [
            [5, 3, 0, 1],
            [4, 0, 0, 1],
            [1, 1, 0, 5],
            [1, 0, 0, 4],
            [0, 1, 5, 4],
            ]

    # P = [
            # [3, 5],
            # [3, 5],
            # [5, 3],
            # [5, 3],
            # [3, 5],
            # ]

    # Q = [
            # [3, 3, 5, 5],
            # [3, 5, 5, 5],
            # ]

    P = np.random.rand(5, 2)
    Q = np.random.rand(2, 4)
    P = P.tolist()
    Q = Q.tolist()

    begin_t = time.time()
    mf(R, P, Q, 5, 4, 2)
    end_t = time.time()
    print P
    print Q
    new_p = np.array(P)
    new_q = np.array(Q)
    new_r = np.dot(new_p, new_q)
    print new_r
    print '---'
    print end_t-begin_t
