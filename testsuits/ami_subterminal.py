# coding=utf-8
import time
from framework.browser_engine import BrowserEngine
from framework.logger import Logger
from pageobjects.ami_homepage import AmiHomePage
import unittest
import random,string
from datasourse.db import CommonDB

logger = Logger(logger="SubTerminal").getlog()

class SubTerminal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        测试固件的setUp()的代码，主要是测试的前提准备工作
        :return:
        """
        browse = BrowserEngine(cls)
        cls.driver = browse.open_browser(cls)

    @classmethod
    def tearDownClass(cls):
        """
        测试结束后的操作，这里基本上都是关闭浏览器
        :return:
        """
        cls.driver.quit()

    # 建主变前选择一条变电站记录
    def click_sub(self):
        homepage = AmiHomePage(self.driver)
        homepage.login('admin', 'inhemeter')
        homepage.click('name=>档案管理')
        homepage.click('name=>变电站档案')
        print(self.driver.find_element_by_name('档案管理'))
        self.driver.switch_to_frame('fun_00601')
        homepage.click('xpath=>//*[@id="dataList"]/div[2]/ul[1]/li[3]')  # 选中第一条变电站记录

    def test_ami_subterminal_create_001(self):
        homepage = AmiHomePage(self.driver)
        self.click_sub()
        # 点击采集终端列表
        homepage.click('id=>group-tab')
        time.sleep(1)
        homepage.click('id=>cstBtn2')
        self.driver.switch_to_frame('cst-page')
        capta = '07550'
        words = ''.join(string.digits)
        for i in range(4):
            capta += random.choice(words)
        homepage.input_value('id=>DEVICE_NUM',capta)
        homepage.input_value('id=>DESCRIPTION',capta)
        # 点击保存
        homepage.click('x=>/html/body/div[3]/div/div/div[21]/div/div[2]/div[1]')
