#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time_converter import TimeNormalizer  # 引入包
from time_converter.log import Time_NLP_LOGGER
# Time_NLP_LOGGER.setLevel(10)
tn = TimeNormalizer(isPreferFuture=False)


def gao():
    tn = TimeNormalizer()

    with open('test_old.txt', 'r+', encoding='utf-8') as f:
        for line in f:
            res = tn.parse(target=line.strip()) # target为待分析语句，timeBase为基准时间默认是当前时间
            print('Sentence:',line)
            print('Result:',res)

def test():
    tn = TimeNormalizer()

    while True:
        x = input()
        res = tn.parse(target=x)
        print(res)

if __name__ == "__main__":
    gao()
    # test()
