# coding=utf-8
import unittest
import os
import time
from html_test_runner import HtmlTestRunner

# 设置报告文件保存路径
report_path = '/Users/lantianwei/Downloads/'
# 获取系统当前时间
now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))

# 设置报告名称格式
HtmlFile = report_path + now + "AmiHtmlreport.html"
fp = open(HtmlFile, "wb")

# 构建suite
suite = unittest.TestLoader().discover("../testsuits/",pattern='*.py')

if __name__ == '__main__':
    # 初始化一个HTMLTestRunner实例对象，用来生成报告
    runner = HtmlTestRunner(stream=fp, title=u"AMI项目测试报告", description=u"用例测试情况")
    # 开始执行测试套件
    runner.run(suite)
