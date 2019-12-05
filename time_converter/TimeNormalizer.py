import pickle
import regex as re
import arrow
import json
import os
from .log import Time_NLP_LOGGER

from .StringPreHandler import StringPreHandler
from .TimePoint import TimePoint
from .TimeUnit import TimeUnit


# 时间表达式识别的主要工作类
class TimeNormalizer:
    def __init__(self, is_prefer_future=True):
        self.isPreferFuture = is_prefer_future
        self.pattern, self.holi_solar, self.holi_lunar = self.init()

    # 这里对一些不规范的表达做转换
    def _filter(self, input_query):
        # 这里对于下个周末这种做转化 把个给移除掉
        input_query = StringPreHandler.number_translator(input_query)

        rule = u"[0-9]月[0-9]"
        pattern = re.compile(rule)
        match = pattern.search(input_query)
        if match is not None:
            index = input_query.find('月')
            rule = u"日|号"
            pattern = re.compile(rule)
            match = pattern.search(input_query[index:])
            if match is None:
                rule = u"[0-9]月[0-9]+"
                pattern = re.compile(rule)
                match = pattern.search(input_query)
                if match is not None:
                    end = match.span()[1]
                    input_query = input_query[:end] + '号' + input_query[end:]

        rule = u"月"
        pattern = re.compile(rule)
        match = pattern.search(input_query)
        if match is None:
            input_query = input_query.replace('个', '')

        # input_query = input_query.replace('中旬', '15号')
        input_query = input_query.replace('傍晚', '午后')
        input_query = input_query.replace('大年', '')
        input_query = input_query.replace('新年', '春节')
        # input_query = input_query.replace('五一', '劳动节')
        input_query = input_query.replace('白天', '早上')
        input_query = input_query.replace('：', ':')
        Time_NLP_LOGGER.debug(f'对一些不规范的表达做转换 {input_query}')
        return input_query

    def init(self):
        file_path = os.path.dirname(__file__) + '/resource/reg.pkl'
        try:
            with open(file_path, 'rb') as f:
                pattern = pickle.load(f)
        except Exception:
            with open(os.path.dirname(__file__) + '/resource/regex.txt',
                      'r',
                      encoding="utf-8") as f:
                content = f.read()
            p = re.compile(content)
            with open(file_path, 'wb') as f:
                pickle.dump(p, f)
            with open(file_path, 'rb') as f:
                pattern = pickle.load(f)

        with open(os.path.dirname(__file__) + '/resource/holi_solar.json',
                  'r',
                  encoding='utf-8') as f:
            holi_solar = json.load(f)
        with open(os.path.dirname(__file__) + '/resource/holi_lunar.json',
                  'r',
                  encoding='utf-8') as f:
            holi_lunar = json.load(f)
        return pattern, holi_solar, holi_lunar

    def parse(self, target, time_base=arrow.now('Asia/Shanghai')):
        """
        TimeNormalizer的构造方法，timeBase取默认的系统当前时间
        :param time_base: 基准时间点
        :param target: 待分析字符串
        :return: 时间单元数组
        """
        Time_NLP_LOGGER.debug(f"目标字符串: {target}")
        self.isTimeSpan = False
        self.invalidSpan = False
        self.timeSpan = ''
        self.target = self._filter(target)
        self.timeBase = arrow.get(time_base).format('YYYY-M-D-H-m-s')
        self.nowTime = time_base
        self.oldTimeBase = self.timeBase
        self.__preHandling()
        self.timeToken = self.__timeEx()
        dic = {}
        res = self.timeToken

        Time_NLP_LOGGER.debug(f'获得的时间点: {res}')
        # Time_NLP_LOGGER.debug(f'Type: {type(res)}')
        for i, x in enumerate(res):
            Time_NLP_LOGGER.debug(f'Class: {i, x, x.get_granularity()}')
            pass
        # self.granularity

        if self.isTimeSpan:
            if self.invalidSpan:
                # dic['类型'] = '非法'
                dic['error'] = 'Illegal time'

            else:
                # result = {}
                dic['error'] = 'Time delta'
                # dic['时间差'] = self.timeSpan
                # dic['error'] = '非时间点.'
                # Time_NLP_LOGGER.debug(f"timedelta: {dic['timedelta']}")
                # index = dic['timedelta'].find('days')

                # days = int(dic['timedelta'][:index - 1])
                # result['year'] = int(days / 365)
                # result['month'] = int(days / 30 - result['year'] * 12)
                # result['day'] = int(days - result['year'] * 365 -
                #                     result['month'] * 30)
                # index = dic['timedelta'].find(',')
                # time = dic['timedelta'][index + 1:]
                # time = time.split(':')
                # result['hour'] = int(time[0])
                # result['minute'] = int(time[1])
                # result['second'] = int(time[2])
                # dic['timedelta'] = result
        else:
            if len(res) == 0:
                # dic['类型'] = '无时间'
                dic['error'] = 'No time'
            elif len(res) == 1:
                # dic['类型'] = '时间点'
                dic['time_start'] = res[0].time.format("YYYY-MM-DD HH:mm:ss")
                dic['time_end'] = res[0].time.format("YYYY-MM-DD HH:mm:ss")
                dic['granularity'] = [res[0].get_granularity(),res[0].get_granularity()]
                dic['fuzzy'] = res[0].get_fuzzy()
            else:
                # dic['类型'] = '时间段'
                dic['time_start'] = res[0].time.format("YYYY-MM-DD HH:mm:ss")
                dic['time_end'] = res[1].time.format("YYYY-MM-DD HH:mm:ss")
                dic['granularity'] = [
                    res[0].get_granularity(), res[1].get_granularity()]
        return dic

    def __preHandling(self):
        """
        待匹配字符串的清理空白符和语气助词以及大写数字转化的预处理
        :return:
        """
        self.target = StringPreHandler.del_keyword(self.target,
                                                  u"\\s+")  # 清理空白符
        self.target = StringPreHandler.del_keyword(self.target,
                                                  u"[的]+")  # 清理语气助词
        self.target = StringPreHandler.number_translator(self.target)  # 大写数字转化
        Time_NLP_LOGGER.debug(f'清理空白符和语气助词以及大写数字转化的预处理 {self.target}')

    def __timeEx(self):
        """
        :return: TimeUnit[]时间表达式类型数组
        """
        start_line = -1
        end_line = -1
        r_pointer = 0
        temp = []

        match = self.pattern.finditer(self.target)
        Time_NLP_LOGGER.debug('=======')
        Time_NLP_LOGGER.debug('用正则提取关键字：')
        for m in match:
            Time_NLP_LOGGER.debug(m)
            start_line = m.start()
            if start_line == end_line:
                r_pointer -= 1
                temp[r_pointer] = temp[r_pointer] + m.group()
            else:
                temp.append(m.group())
            end_line = m.end()
            r_pointer += 1
        Time_NLP_LOGGER.debug('=======')

        res = []
        # 时间上下文： 前一个识别出来的时间会是下一个时间的上下文，用于处理：周六3点到5点这样的多个时间的识别，第二个5点应识别到是周六的。
        context_tmp = TimePoint()
        Time_NLP_LOGGER.debug(f"基础时间 {self.timeBase}")
        Time_NLP_LOGGER.debug(f'待处理的字段: {temp}')
        for i in range(0, r_pointer):
            # 这里是一个类嵌套了一个类
            Time_NLP_LOGGER.debug('Last TP:{}'.format(context_tmp))
            try:
                time_convert_result = TimeUnit(temp[i], self, context_tmp)
            except Exception as err:
                self.isTimeSpan = True
                self.invalidSpan = True
                break
            if time_convert_result.get_fuzzy()=='null':
                # Time_NLP_LOGGER.debug('Fuzzy Not rec')
                time_convert_result.norm_set_fuzzy_time(match_raw=self.target)
            res.append(time_convert_result)
            # res[i].tp.tunit[3] = -1

            # 上一个时间点 -- 改
            context_tmp = res[i].tp

            # contextTp = TimePoint()

        Time_NLP_LOGGER.debug(f'时间表达式类型数组 {res}')
        res = self.__filterTimeUnit(res)
        return res

    def __filterTimeUnit(self, tu_arr):
        """
        过滤timeUnit中无用的识别词。无用识别词识别出的时间是1970.01.01 00:00:00(fastTime=0)
        :param tu_arr:
        :return:
        """
        if (tu_arr is None) or (len(tu_arr) < 1):
            return tu_arr
        res = []
        for tu in tu_arr:
            if tu.time.timestamp != 0:
                res.append(tu)
        Time_NLP_LOGGER.debug(f'过滤timeUnit中无用的识别词 {res}')
        return res
