# coding:utf-8
import os, sys

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, path)
import unittest
from core import HTMLTestRunner
from parameterized import parameterized
from core import logger
import inspect
from core.tools import p


def cacl(a, b):
    return a + b


class MyCacl2(unittest.TestCase):
    def setUp(self):
        pass
        # print('测试用例开始执行...')

    def tearDown(self):
        pass
        # print('测试用例执行完成...')

    @parameterized.expand(
        [
            ("fushujiaxiaoshu", -1, 1.5, 0.5),  # 负数加小数
            ("xiaoshujiaxiaoshu", 1.1, 2.2, 3.3),  # 小数相加

        ]
    )
    def test_cacl(self, a, b, c, d):  # 此处a不能省略
        try:
            res = cacl(b, c)
        except TypeError as e:
            res = '类型错误'
        self.assertEqual(res, d)

