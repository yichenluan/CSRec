# -*- coding: utf-8 -*-
"""
Build Random Forest

Author: JinKe
"""
import random

from CSRec.ContextRec.decision_tree import DecisionTree

DataRate = 0.8


class RandomForest():

    def __init__(
            self, tree_num, max_context, max_depth, context_list, data
            ):
        self.max_depth = max_depth
        self.context_list = context_list
        self.data = data

        self.tree_num = tree_num
        self.max_context = max_context

        self.trees = list()

    def build(self):
        for i in range(self.tree_num):
            tree_data = self.__get_tree_data()
            tree_context = self.__get_tree_context()
            tree = self.build_decision_tree(tree_data, tree_context)
            self.trees.append(tree)

    def build_decision_tree(self, tree_data, tree_context):
        decision_tree = DecisionTree(self.max_depth, tree_data, tree_context)
        decision_tree.build()
        return decision_tree

    def __get_tree_data(self):
        tree_data_num = int(len(self.data) * DataRate)
        tree_data = random.sample(self.data, tree_data_num)
        return tree_data

    def __get_tree_context(self):
        tree_context_num = int(len(self.context_list) * self.max_context)
        tree_context = random.sample(self.context_list, tree_context_num)
        return tree_context

    def run(self, record):
        res = list()
        for tree in self.trees:
            res.append(tree.run())
        return res
