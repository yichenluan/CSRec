# -*- coding: utf-8 -*-
"""
Context-Aware Recommender System Experiments

Author: JinKe
"""
from CSRec.DataView.ml_data import build_ml_data
from CSRec.DataView.ml_data import Record
from CSRec.ContextRec.random_forest import RandomForest

train_data_path = '/Users/hunter/repos/g_project/datasets/ml_100k/ua.base'
test_data_path = '/Users/hunter/repos/g_project/datasets/ml_100k/ua.test'

tree_num = 10
max_context = 3
max_depth = 2
context_list = ['sex', 'age', 'occupation', 'genre', 'time']


def do_experiment(rf, test_data):
    test_len = len(test_data)
    index = 1
    ex_res = list()
    for line in test_data:
        print index, test_len
        test_record = Record(line[0], line[1], line[2], line[3])
        test_record.build()
        rf_data_list = rf.run(test_record)
        #do_someting()


def experiment():
    train_data = build_ml_data(train_data_path)
    test_data = build_ml_data(test_data_path)
    random_forest = RandomForest(
            tree_num, max_context, max_depth, context_list, train_data
            )
    random_forest.build()

    result = do_experiment(random_forest, test_data)
    return result
