# -*- coding: utf-8 -*-
"""
Social Recommender System Experiments

Author: JinKe
"""
import random

from CSRec.DataView.filetrust_data import build_rating_data
from CSRec.DataView.filetrust_data import build_trust_data
from CSRec.DataView.filetrust_data import build_rating_matix
# from CSRec.DataView.filetrust_data import build_trust_matix
from CSRec.DataView.filetrust_data import build_trust_dict
from CSRec.DataView.filetrust_data import build_rating_dict

from CSRec.SocialRec.social_mf import social_mf
from CSRec.SocialRec.base_mf import matix_factorization

from CSRec.Experiment.evaluation import RMSE


rating_data_path = '/Users/hunter/repos/g_project/datasets/filmtrust/ratings.txt'
test_pencentage = 0.1

K = 10


def split_train_test(all_data):
    test_data = random.sample(
            all_data, int(test_pencentage * len(all_data))
            )
    train_data = all_data[:]
    for row in test_data:
        train_data.remove(row)
    return train_data, test_data


def compute_rmse(mf_res, test_data):
    res = list()
    for i in test_data:
        predict_res = mf_res[i[0]-1][i[1]-1]
        true_res = i[2]
        if predict_res < 1:
            predict_res = 1
        if predict_res > 5:
            predict_res = 5
        res.append((predict_res, true_res))
    rmse, err = RMSE(res)
    return rmse, err


def do_experiment(train_data, test_data):
    rating_matix = build_rating_matix(train_data)
    rating_dict = build_rating_dict(train_data)

    trust_data = build_trust_data()
    # trust_matix = build_trust_matix(trust_data)
    trust_dict = build_trust_dict(trust_data)

    mf_res = social_mf(rating_matix, rating_dict, trust_dict, K)
    rmse = compute_rmse(mf_res, test_data)
    return rmse


def experiment():
    all_data = build_rating_data(rating_data_path)
    train_data, test_data = split_train_test(all_data)
    print 'end split data'
    result, err = do_experiment(train_data, test_data)
    return result, err


if __name__ == '__main__':
    rmse, err = experiment()
    print rmse, err
