# coding=utf-8
import time
from framework.browser_engine import BrowserEngine
from framework.logger import Logger
from pageobjects.ami_homepage import AmiHomePage
import unittest
import random,string
from datasourse.db import CommonDB

logger = Logger(logger="Substation").getlog()

class Substation(unittest.TestCase):
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

    #进入档案管理模块，打开档案管理页面分装成一个方法
    def openSubstation(self):
        homepage = AmiHomePage(self.driver)
        homepage.login('admin', 'inhemeter')
        homepage.click('name=>档案管理')
        homepage.click('name=>变电站档案')
        self.driver.switch_to_frame('fun_00601')

    def test_ami_substation_create_001(self):
        logger.info("建变电站测试用例开始执行>>>>>>")
        homepage = AmiHomePage(self.driver)
        self.openSubstation()
        homepage.click('id=>addBtn')#新建按钮
        time.sleep(1)
        self.driver.switch_to_frame('new-page')
        # string.ascii_letters  生成26个大小写英文字母，string.digits生成数字0123456789
        # random.choice （），随机选取字符串、列表等
        capta = ''
        words = ''.join((string.ascii_letters, string.digits))
        for i in range(6):
            capta += random.choice(words)
        # 输入变电站名称
        homepage.input_value('id=>DESCRIPTION', capta)
        # 点击分支机构输入框
        homepage.click('id=>BRANCH')
        self.driver.switch_to_default_content()
        # 分支机构弹出控件
        self.driver.switch_to_frame('mainModalIframe')
        # 点击第一层分支机构
        homepage.click('xpath=>//*[@id="tree"]/ul/li/span/a')
        # 点击第二层分支机构
        homepage.click('xpath=>//*[@id="tree"]/ul/li/ul/li/span/a')
        self.driver.switch_to_default_content()
        homepage.click('xpath=>//*[@id="mainModal_ok"]')#再次确认
        self.driver.switch_to_frame('fun_00601')
        self.driver.switch_to_frame('new-page')#回到变电站信息页面（新建或修改）
        homepage.click('xpath=>//*[@id="VOL_LEVEL"]/option[3]')  # 电压等级220kv
        homepage.input_value('xpath=>//*[@id="ADDRESS"]', 'xxxxxx')#地址
        homepage.input_value('id=>CAPACITY', '100')#容量
        homepage.click("xpath=>//html/body/div[3]/div/div/div[15]/div/div[2]/div[1]")#点击保存变电站信息
        # 实例化对象
        db = CommonDB()
        self.assertTrue(db.data_is_exist("select * from am_substation where DESCRIPTION='" + capta + "';"))
        self.assertTrue(db.exec_delete("delete from am_substation where DESCRIPTION='" + capta + "';"))
        logger.info("建变电站测试用例执行完毕>>>>>>")

    # 变电站名称为空
    def test_ami_substation_create_002(self):
        logger.info("建变电站名称为空测试用例开始执行>>>>>>")
        homepage = AmiHomePage(self.driver)
        self.openSubstation()
        homepage.click('id=>addBtn')
        time.sleep(1)
        self.driver.switch_to_frame('new-page')
        homepage.input_value('id=>DESCRIPTION', '  ')
        homepage.click('id=>BRANCH')
        self.driver.switch_to_default_content()
        self.driver.switch_to_frame('mainModalIframe')
        homepage.click('xpath=>//*[@id="tree"]/ul/li/span/a')
        time.sleep(1)
        homepage.click('xpath=>//*[@id="tree"]/ul/li/ul/li/span/a')
        self.driver.switch_to_default_content()
        homepage.click('xpath=>//*[@id="mainModal_ok"]')  # 再次确认
        self.driver.switch_to_frame('fun_00601')
        self.driver.switch_to_frame('new-page')
        homepage.click("xpath=>//html/body/div[3]/div/div/div[15]/div/div[2]/div[1]")  # 点击保存变电站信息>
        self.driver.switch_to_default_content()
        self.driver.switch_to_frame('fun_00601')
        # 断言验证测试结果是否通过
        str = homepage.find_element('class_name=>warn-text').text
        self.assertEqual(str, '变电站名称  :\n输入值不能为空！', '测试结果不通过，预期结果和实际不符合')
        homepage.logout()

    # 修改变电站
    def test_ami_substation_edit_003(self):
        logger.info('修改变电站测试用例开始执行----------------------')
        homepage = AmiHomePage(self.driver)
        self.openSubstation()
        try:
            homepage.click("xpath=>//*[@id='editBtn']")  # 点击修改
            self.driver.switch_to_frame('new-page')
            homepage.input_value('id=>DESCRIPTION', 'test1')
            homepage.click('xpath=>//*[@id="VOL_LEVEL"]/option[3]')  # 修改电压等级220kv
            homepage.input_value('xpath=>//*[@id="ADDRESS"]', 'test11111')
            homepage.input_value('id=>CAPACITY', '100')
            homepage.click('xpath=>/html/body/div[3]/div/div/div[15]/div/div[2]/div[1]')  # 点击保存
            self.driver.switch_to_default_content()
            self.driver.switch_to_frame('fun_00601')
            # 断言
            s = homepage.find_element('xpath=>//*[@id="dataList"]/div[2]/ul[1]/li[4]').text
            logger.info('>>>>>>>>>>>>>>>'+s.strip())
            logger.info('s = [' + s + ']')
            self.assertIn('test1', s, '修改变电站断言失败')
            time.sleep(1)
        except Exception as e:
            logger.error("执行出错 %s" % e)
            logger.info('修改变电站测试结果-----不通过')
            self.assertIs('None',True)
        logger.info('修改变电站测试用例执行完毕----------------------')

    # 取消新建变电站，取消按钮
    def test_ami_substation_cancel_004(self):
        logger.info("取消建变电站测试用例开始执行>>>>>>")
        homepage = AmiHomePage(self.driver)
        self.openSubstation()
        homepage.click('id=>addBtn')#新建按钮
        time.sleep(1)
        self.driver.switch_to_frame('new-page')
        capta = ''
        words = ''.join((string.ascii_letters, string.digits))
        for i in range(6):
            capta += random.choice(words)
        # 输入变电站名称
        homepage.input_value('id=>DESCRIPTION', capta)
        # 点击取消按钮
        homepage.click('x=>/html/body/div[3]/div/div/div[15]/div/div[2]/div[2]')
        # 验证是否无数据
        db = CommonDB()
        self.assertFalse(db.data_is_exist("select * from am_substation where DESCRIPTION='" + capta + "';"))
        logger.info("取消建变电站测试用例执行完毕>>>>>>")



