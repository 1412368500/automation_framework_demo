#coding=utf-8
import time
from framework.browser_engine import BrowserEngine
from framework.logger import Logger
from pageobjects.ami_homepage import AmiHomePage
import unittest
import random,string
from datasourse.db import CommonDB

logger = Logger(logger="Line").getlog()

class Line(unittest.TestCase):
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

    def line_open(self):
        homepage = AmiHomePage(self.driver)
        homepage.login('admin','inhemeter')
        homepage.click('name=>档案管理')
        time.sleep(1)
        homepage.click('name=>线路档案')
        self.driver.switch_to_frame('fun_00602')

    def test_line_create_001(self):
        homepage = AmiHomePage(self.driver)
        self.line_open()
        homepage.click('id=>addBtn')
        self.driver.switch_to_frame('new-page')
        capta = ''
        words = ''.join((string.ascii_letters, string.digits))
        for i in range(6):
            capta += random.choice(words)
        # 输入线路名称
        homepage.input_value('id=>DESCRIPTION', capta)

        # 电压等级35kv
        homepage.click('xpath=>//*[@id="VOL_LEVEL"]/option[4]')
        # 输入电流
        homepage.input_value('id=>CURRENT', '100')
        # 点击分支机构输入框
        homepage.click('id=>BRANCH')
        self.driver.switch_to_default_content()
        self.driver.switch_to_frame('mainModalIframe')
        # 选择分支机构，第一条记录
        homepage.click('x=>//*[@id="brchBranchList"]/div[2]/ul[@index=0]')
        self.driver.switch_to_default_content()
        homepage.click('id=>mainModal_ok')
        # 选择变电站
        self.driver.switch_to_frame('fun_00602')
        self.driver.switch_to_frame('new-page')
        homepage.click('id=>STATION')
        self.driver.switch_to_default_content()
        self.driver.switch_to_frame('mainModalIframe')
        # 勾选一条变电站记录
        homepage.click('name=>chkField')
        self.driver.switch_to_default_content()
        homepage.click('id=>mainModal_ok')
        # 点击保存
        self.driver.switch_to_frame('fun_00602')
        self.driver.switch_to_frame('new-page')
        homepage.click('x=>/html/body/div[3]/div/div/div[19]/div/div[2]/div[1]')
        db = CommonDB()
        self.assertTrue(db.data_is_exist("select * from am_line where DESCRIPTION='" + capta + "';"))
        db.exec_delete("delete from am_line where DESCRIPTION='" + capta + "';")

