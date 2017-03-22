# -*- coding: utf-8 -*-
"""
Context-Aware Recommender System Experiments

Author: JinKe
"""
from CSRec.DataView.ml_data import build_ml_data
from CSRec.DataView.ml_data import Record
from CSRec.ContextRec.random_forest import RandomForest
from CSRec.Experiment.evaluation import RMSE

train_data_path = '/Users/hunter/repos/g_project/datasets/ml_100k/ua.base'
test_data_path = '/Users/hunter/repos/g_project/datasets/ml_100k/ua.test'

tree_num = 5
max_context = 3
max_depth = 2
context_list = ['sex', 'age', 'occupation', 'genre', 'time']


def compute_rf_predict(predicts):
    rating_predicts = list()
    for p in predicts:
        if p.details['was_impossible'] is False:
            rating_predicts.append(p.est)
    if not rating_predicts:
        return -1
    predict_res = sum(rating_predicts) / len(rating_predicts)
    return predict_res


def do_experiment(rf, test_data):
    test_len = len(test_data)
    index = 1
    eval_res = list()
    for line in test_data:
        print index, test_len
        test_record = Record(line[0], line[1], line[2], line[3])
        test_record.build()
        rf_predicts = rf.run(test_record)
        predict_res = compute_rf_predict(rf_predicts)
        eval_res.append((predict_res, test_record.rating))
        index += 1
    rmse, err = RMSE(eval_res)
    return rmse, err


def experiment():
    train_data = build_ml_data(train_data_path)
    test_data = build_ml_data(test_data_path)
    random_forest = RandomForest(
            tree_num, max_context, max_depth, context_list, train_data
            )
    random_forest.build()

    rmse, err = do_experiment(random_forest, test_data)
    return rmse, err


if __name__ == '__main__':
    rmse, err = experiment()
    print rmse, err
