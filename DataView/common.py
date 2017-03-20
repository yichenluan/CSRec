# -*- coding: utf-8 -*-


def read_file(file_path):
    f_content = list()
    with open(file_path, 'r') as f:
        for f_line in f:
            f_content.append(f_line)
    return f_content
