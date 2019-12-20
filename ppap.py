#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time_converter import TimeNormalizer  # 引入包
from time_converter.log import Time_NLP_LOGGER
import arrow

Time_NLP_LOGGER.setLevel(10)

def main():
    tn = TimeNormalizer()
    tmp = arrow.now('Asia/Shanghai')
    print(tmp)
    ans = arrow.get(tmp, "YYYY-M-D-H-m-s")
    print(ans)
    ans = arrow.get('2019-12-11T22:09:14.579581+08:00', "YYYY-M-D-H-m-s")
    print(ans)


if __name__ == "__main__":
    main()