# -*- coding: utf-8 -*-

import numpy as np
import time
from math import sqrt

from CSRec.DataView.filetrust_data import build_rating_data
from CSRec.DataView.filetrust_data import build_rating_matix


def social_mf(R, T, K):
    N = len(R)
    M = len(R[0])

    P = np.random.rand(N, K)
    Q = np.random.rand(M, K)

    new_P, new_Q = mf_handler(R, T, N, M, P, Q, K)
    return np.dot(new_P, new_Q.T)


def sim_pearson(prefs, p1, p2):
    si = dict()
    item_num = len(prefs[p1])
    for i in xrange(item_num):
        if prefs[p1][i] and prefs[p2][i]:
            si[i] = 1

    if not si:
        return 0

    n = len(si)

    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])

    sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])

    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])

    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1, 2) / 2) * (sum2Sq - pow(sum2, 2) / n))

    if den == 0:
        return 0

    return num / den


def social_regular(R, T, P, k, i):
    i_trust = list()
    for j in T[i]:
        if j:
            i_trust.append(j)

    res = 0.0
    for friend in i_trust:
        sim_friend = sim_pearson(R, i, friend)
        diff_friend = P[i][k] - P[friend][k]
        res += sim_friend * diff_friend

    return res


def mf_handler(
        R, T, N, M, P, Q, K, steps=5000, alpha=0.0002, beta=0.02, gamma=0.01
        ):
    Q = Q.T

    for step in xrange(steps):
        for i in xrange(N):
            for j in xrange(M):
                if R[i][j] <= 0:
                    continue
                eij = R[i][j] - np.dot(P[i, :], Q[:, j])
                for k in xrange(K):
                    P[i][k] += alpha * (2 * eij * Q[k][j] - beta * P[i][k]) + \
                        gamma * social_regular(R, T, P, k, i)
                    Q[k][j] += alpha * (2 * eij * P[i][k] - beta * Q[k][j])

        loss = 0
        for i in xrange(N):
            for j in xrange(M):
                if R[i][j] <= 0:
                    continue
                loss += pow(R[i][j] - np.dot(P[i, :], Q[:, j]), 2)
                for k in xrange(K):
                    loss += (beta / 2) * (pow(P[i][k], 2) + pow(Q[k][j], 2))

        if loss < 0.001:
            break
        print loss, np.dot(P[0, :], Q[:, 6])

    return P, Q.T
