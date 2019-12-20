"""
@description: 配置时间点的信息
@author: GG Sasaki
@email: gg.pan@foxmail.com
@time: 2019-11-08
@version: 0.8.5
"""


# 范围时间的默认时间点
class RangeTimeEnum(object):
    """
    设置默认的时间点
    """
    day_break = 3  # 黎明
    early_morning = 6  # 早
    morning = 9  # 上午
    noon = 11  # 中午、午间
    afternoon = 12  # 下午、午后
    night = 18  # 晚上、傍晚
    lateNight = 22  # 晚、晚间
    midNight = 23  # 深夜


