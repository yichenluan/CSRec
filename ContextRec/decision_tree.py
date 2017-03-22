# -*- coding: utf-8 -*-
"""
Build Decision Tree

Author: JinKe
"""
import time

from surprise import Dataset
from surprise import Reader
from surprise import SVD

from CSRec.ContextRec.gini import compute_mini_gini
"""
Inuput:
    1. 深度阈值
    2. 上下文信息
    3. data
"""


class DecisionNode():

    def __init__(self):
        self.divide_context = None
        self.data = None
        # self.func = None
        self.child_dict = dict()
        self.algo = None


class Matix():

    def __init__(self, data):
        self.data = data
        self.users = list()
        self.items = list()


class DecisionTree():

    def __init__(self, max_depth, context_list, data):
        self.max_depth = max_depth
        self.context_list = context_list
        self.data = data

        self.root = None

    def build(self):
        tree = self.__build_handler(self.data, self.context_list, 1)
        tree = self._build_predict(tree)
        self.root = tree

    def _build_predict(self, tree):
        leaf_nodes = list()
        self._get_leaf_node(tree, leaf_nodes)
        for leaf in leaf_nodes:
            print 'begin'
            self._train_predict(leaf)
            print 'end'
        return tree

    def _train_predict(self, node):
        file_name = 'file/%s.dat' % time.time()
        with open(file_name, 'w') as f:
            f.writelines(
                    ['%s\t%s\t%s\t%s\n' % (line[0], line[1], line[2], line[3])
                        for line in node.data]
                    )
        reader = Reader(line_format='user item rating timestamp', sep='\t')
        surprise_data = Dataset.load_from_file(file_name, reader=reader)
        train_set = surprise_data.build_full_trainset()
        algo = SVD()
        algo.train(train_set)
        node.algo = algo

    def _get_leaf_node(self, root, leafs):
        if not root.child_dict:
            leafs.append(root)
        for node in root.child_dict.values():
            self._get_leaf_node(node, leafs)

    def __build_handler(self, node_data, node_context, depth):
        root = DecisionNode()
        root.data = node_data
        if depth >= self.max_depth:
            return root
        if not node_context:
            return root
        choosed_context, data_dict = compute_mini_gini(node_data, node_context)
        root.divide_context = choosed_context
        for key, value in data_dict.iteritems():
            child_context = node_context[:]
            child_context.remove(choosed_context)
            child_node = self.__build_handler(value, child_context, depth+1)
            root.child_dict[key] = child_node
        return root

    def run(self, record):
        node = self.root
        while node.child_dict:
            curr_divide_context = node.divide_context
            divide_res = record.get_res(curr_divide_context)
            node = node.child_dict[divide_res]
        uid = str(record.user_id)
        iid = str(record.item_id)
        r_ui = record.rating
        predict_r = node.algo.predict(uid, iid, r_ui, verbose=True)
        return predict_r
