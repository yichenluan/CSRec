# -*- coding: utf-8 -*-
"""
Compute Gini

Author: JinKe
"""

from CSRec.DataView.ml_data import DivideData


def _base_gini(data):
    rank_count = {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
        }
    for line in data:
        rank = line[-1]
        rank_count[rank] += 1
    rank_total = float(sum(rank_count.values()))
    base_gini = 1
    if not rank_total:
        return base_gini, rank_total
    for i in range(1, 6):
        base_gini -= pow((rank_count[i] / rank_total), 2)
    return base_gini, rank_total


def compute_gini(num, data_list):
    gini = 0
    if not num:
        return gini
    for data in data_list:
        base_gini, data_num = _base_gini(data)
        gini += (data_num / num) * base_gini
    return gini


def compute_mini_gini(data, context_list):
    mini_gini = 1
    curr_choice = ''
    data_dict = dict()
    for context in context_list:
        num, context_data_dict = DivideData(data, context).divide()
        gini = compute_gini(num, context_data_dict.values())
        if gini < mini_gini:
            mini_gini = gini
            curr_choice = context
            data_dict = context_data_dict
    return curr_choice, data_dict
