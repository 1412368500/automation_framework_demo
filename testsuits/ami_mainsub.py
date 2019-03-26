#coding=utf-8
import random
import string
import time
from framework.browser_engine import BrowserEngine
from framework.logger import Logger
from pageobjects.ami_homepage import AmiHomePage
import unittest
from datasourse.db import CommonDB


logger = Logger(logger="MainTransformer").getlog()

class MainTransformer(unittest.TestCase):
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

    def test_ami_maintm_001(self):
        logger.info("建变电站主变列表测试用例开始执行>>>>>>")
        homepage = AmiHomePage(self.driver)
        self.click_sub()
        self.driver.switch_to_default_content()
        self.driver.switch_to_frame('fun_00601')
        homepage.click('id=>cstBtn')
        self.driver.switch_to_frame('cst-page')
        capta = 'maintm'
        words = ''.join((string.ascii_letters, string.digits))
        for i in range(6):
            capta += random.choice(words)
        homepage.input_value('id=>NAME', capta)
        homepage.click('xpath=>/html/body/div[3]/div/div[1]/div[18]/div/div[2]/div[1]')  # 点击保存
        self.driver.switch_to_default_content()
        homepage.click('xpath=>//*[@id="alertModal"]/div/div/div[3]/button')  # 确认保存
        # 查询数据是否添加成功
        db = CommonDB()
        self.assertTrue(db.data_is_exist("select * from am_customer where NAME='" + capta + "'and TYPE=4;"))
        self.assertTrue(db.exec_delete("delete from am_customer where NAME= '" + capta + "' and TYPE=4;"))

    # 修改主变信息
    def test_ami_maintm_edit_002(self):
        homepage = AmiHomePage(self.driver)
        self.click_sub()
        # 点击修改
        homepage.click('x=>//*[@id="cstList"]/div[2]/ul[1]/li[2]/div/div[1]')
        self.driver.switch_to_frame('cst-page')
        name ='test'
        name += str(random.randint(0,9))
        homepage.input_value('id=>NAME', name)
        homepage.click('xpath=>/html/body/div[3]/div/div[1]/div[18]/div/div[2]/div[1]')  # 点击保存
        self.driver.switch_to_default_content()
        homepage.click('xpath=>//*[@id="alertModal"]/div/div/div[3]/button')  # 确认保存
        # 查看数据是否修改
        db = CommonDB()
        self.assertTrue(db.data_is_exist("select * from am_customer where NAME='" + name + "'and TYPE=4;"))

    #删除主变列表信息
    def test_ami_maintm_detele_003(self):
        homepage = AmiHomePage(self.driver)
        self.click_sub()
        # 获取第一行信息
        # str1 = homepage.find_element('x=>//*[@id="cstList"]/div[2]/ul[1]/li[7]').text
        # 点击删除
        homepage.click('x=>//*[@id="cstList"]/div[2]/ul[1]/li[2]/div/div[2]')
        self.driver.switch_to_default_content()
        homepage.click('id=>confirmModal_ok')
        time.sleep(1)
        self.driver.switch_to_frame('fun_00601')
        code = homepage.find_element('x=>//*[@id="cstList"]/div[2]/ul[1]/li[3]').text
        # 获取第一条记录的运行状态
        str2 = homepage.find_element('x=>//*[@id="cstList"]/div[2]/ul[1]/li[7]').text
        self.assertEqual(str2,'Stoped','删除失败')

        db = CommonDB()
        # 删除成功后改回运行状态
        db.exec_query("update am_customer set STATUS=0 where CODE='" + code + "' ;")
        # 断言
        self.assertEqual('0',db.exec_query("select STATUS from am_customer where CODE ='" + code + "' ;"))






