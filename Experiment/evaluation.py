# -*- coding: utf-8 -*-
"""
Recommender System Evaluation Standard

Author: JinKe
"""
from math import sqrt


def RMSE(res):
    '''
    row: [predict_res, true_res]
    '''
    sumSq = 0
    error_num = 0
    for row in res:
        if row[0] < 1:
            error_num += 1
        else:
            sumSq += pow(row[0]-row[1], 2)
    rmse = sqrt(sumSq / (len(res)-error_num))
    return rmse, error_num
