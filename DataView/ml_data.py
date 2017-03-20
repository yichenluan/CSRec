# -*- coding: utf-8 -*-

import time

from CSRec.DataView.common import read_file

mac_path = '/Users/hunter/repos/g_project/datasets/ml_100k/'
forhead_path = mac_path


def build_ml_data(data_path):
    f_content = read_file(data_path)
    ml_data = [[int(i) for i in line.split('\t')] for line in f_content]
    return ml_data


def build_user_data():
    f_path = forhead_path + 'u.user'
    f_content = read_file(f_path)
    user = [line.split('|')[:-1] for line in f_content]

    def format_user_data(line):
        line[0] = int(line[0])
        line[1] = int(line[1])
        return line

    user_data = map(format_user_data, user)
    return user_data


def build_occupation_data():
    f_path = forhead_path + 'u.occupation'
    f_content = read_file(f_path)
    occupation = [line[:-1] for line in f_content]
    return occupation


def build_item_data():
    f_path = forhead_path + 'u.item'
    f_content = read_file(f_path)
    item = [line.split('|') for line in f_content]

    def format_item_data(line):
        line[-1] = line[-1].strip()
        genre = [int(g) for g in line[5:]]
        line = line[:3]
        line.append(genre)
        return line
    
    item_data = map(
            format_item_data,
            item
            )
    return item_data


def build_genre_dict():
    f_path = forhead_path + 'u.genre'
    f_content = read_file(f_path)
    genre = [line.split('|') for line in f_content]
    for g in genre:
        g[-1] = int(g[-1][:-1])
    genre_dict = dict([g[-1], g[0]] for g in genre)
    return genre_dict


"""
Context:
    1. Genre 电影类别
    2. Occupation 职业
    3. Sex 性别
    4. Age 年龄
    5. Time 打分时间
"""


def get_age_index(age):
    age_divide = {
            1: 24,
            2: 55,
            3: 100
            }
    if age <= age_divide[1]:
        return 1
    if age <= age_divide[2]:
        return 2
    return 3


def get_occupation_index(occupation):
    occupation_divide = {
            1: ['artist', 'writer', 'entertainment', 'scientist']
            2: ['salesman', 'marketing', 'engineer', 'technician', 'programmer', 'administrator', 'executive'],
            3: ['librarian', 'doctor', 'healthcare', 'educator', 'lawyer'],
            4: ['none', 'other', 'retired', 'homemaker', 'student'],
            }
    if occupation in occupation_divide[1]:
        return 1
    if occupation in occupation_divide[2]:
        return 2
    if occupation in occupation_divide[3]:
        return 3
    if occupation in occupation_divide[4]:
        return 4


def get_genre_index(genre):
    genre_divide = {
            1: ['Documentary', 'Musical', 'Drama', 'unknown'],
            2: ['Crime', 'Film-Noir', 'Horror', 'Thriller'],
            3: [],
            }
    genre_dict = build_genre_dict()
    item_g = list()
    for i in range(len(genre)):
        if genre[i] == 1:
            g = genre_dict[i]
            item_g.append(g)
    if set(item_g) & set(genre_divide[1]):
        return 1
    if set(item_g) & set(genre_divide[2]):
        return 2
    return 3


def get_time_index(time):
    time_ = time.gmtime(time)
    time_gm = time_.tm_hour
    if time_gm >= 7 and time_gm <12:
        return 1
    if time_gm >= 12 and time_gm <= 19:
        return 2
    return 3


class DivideData():

    def __init__(self, data, context):
        self.data = data
        self.context = context

        self.user_data = build_user_data()
        self.item_data = build_item_data()

    def by_sex(self):
        male_data = list()
        female_data = list()
        for line in self.data:
            user_id = line[0]
            user_sex = self.user_data[user_id-1][2]
            if user_sex == 'M':
                male_data.append(line)
            else:
                female_data.append(line)
        sex_data = {
                'M': male_data,
                'F': female_data,
                }
        return len(self.data), sex_data

    def by_age(self):
        age_data = {
                1: list(),
                2: list(),
                3: list(),
                }
        for line in self.data:
            user_id = line[0]
            user_age = self.user_data[user_id-1][1]
            age_index = get_age_index(user_age)
            age_data[age_index].append(line)
        return len(self.data), age_data

    def by_occupation(self):
        occupation_data = {
                1: list(),
                2: list(),
                3: list(),
                4: list(),
                }
        for line in self.data:
            user_id = line[0]
            user_occupation = user_matix[user_id-1][3]
            occupation_index = get_occupation_index(user_occupation)
            occupation_data[occupation_index].append(line)
        return len(self.data), occupation_data

    def by_genre(self):
        genre_data = {
                1: list(),
                2: list(),
                3: list(),
                }
        for line in self.data:
            item_id = line[1]
            item_genre = self.item_data[item_id-1][-1]
            genre_index = get_genre_index(item_genre)
            genre_data[genre_index].append(line)
        return len(self.data), genre_data

    def by_time(self):
        time_data = {
                1: list(),
                2: list(),
                3: list(),
                }
        for line in self.data:
            time = line[-1]
            time_index = get_time_index(time)
            time_data[time_index].append(line)
        return len(self.data), time_data

    def divide(self):
        if self.context == 'sex':
            return self.by_sex()
        if self.context == 'age':
            return self.by_age()
        if self.context == 'occupation':
            return self.by_occupation()
        if self.context == 'genre':
            return self.by_genre()
        if self.context == 'time':
            return self.by_time()


class Record():

    def __init__(self, user_id, item_id, rating, time):
        self.user_id = user_id
        self.item_id = item_id
        self.rating = rating
        self.time = time
        self.sex = None
        self.age = None
        self.occupation = None
        self.genre = None

        self.item_data = build_item_data()
        self.user_data = build_user_data()

    def build(self):
        user_sex = self.user_data[self.user_id-1][2]
        self.sex = user_sex

        user_age = self.user_data[self.user_id-1][1]
        self.age = get_age_index(user_age)

        user_occupation = self.user_matix[self.user_id-1][3]
        self.occupation = get_occupation_index(user_occupation)

        item_genre = self.item_data[self.item_id-1][-1]
        self.genre = get_genre_index(item_genre)

        self.time = get_time_index(self.time)

    def get_res(self, context):
        if context == 'sex':
            return self.sex
        if context == 'age':
            return self.age
        if context == 'occupation':
            return self.occupation
        if context == 'genre':
            return self.genre
        if context == 'time':
            return self.time
