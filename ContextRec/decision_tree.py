# -*- coding: utf-8 -*-
"""
Build Decision Tree

Author: JinKe
"""
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


class DecisionTree():

    def __init__(self, max_depth, context_list, data):
        self.max_depth = max_depth
        self.context_list = context_list
        self.data = data

        self.root = None

    def build(self):
        tree = self.__build_handler(self.data, self.context_list, 1)
        self.root = tree

    def __build_handler(self, node_data, node_context, depth):
        root = DecisionNode()
        root.data = node_data
        if depth >= self.max_depth:
            return root
        if not node_context:
            return root
        choosed_context, data_dict = compute_mini_gini(node_context, node_data)
        # root.func = something
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
        return node.data
