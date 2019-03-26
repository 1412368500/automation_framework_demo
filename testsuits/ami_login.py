#coding=utf-8
import csv
import unittest
from framework.browser_engine import BrowserEngine
from framework.logger import Logger
from pageobjects.ami_homepage import AmiHomePage
import time
logger = Logger(logger="AmiLogin").getlog()
class AmiLogin(unittest.TestCase):
    name = 'admin'
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

    #执行登录测试用例
    def test_ami_login_001(self):
        logger.info("登陆测试用例开始执行>>>>>>")
        homepage = AmiHomePage(self.driver)
        loginFile = open('../test_case_excel/login_testcase.csv','r',encoding='utf-8')
        loginFileResult = open('../test_case_excel/login_testcase_result.csv','w',encoding='utf-8')
        user_login_list = csv.reader(loginFile)
        failNum = 0
        totalNum = 0
        x = 1
        for user in user_login_list:
            if x == 1:
                x = x+1
                #写标题
                loginFileResult.write('%s,%s,%s,%s,%s,%s,%s\n'%(user[0],user[1],user[2],user[3],user[4],user[5],user[6]))
                continue
            print("--testcase:%s--"%user[0])#打印测试用例标题user[0]
            errInfo = ''
            if user[3]=='TRUE':
                homepage.login(user[1], user[2])
                userlogin = homepage.find_element('xpath=>/html/body/div[3]/aside/section/div[1]/div[2]/p').text
                if userlogin == user[4]:
                    testResult = "PASS"

                else:
                    testResult = 'FAIL'
                    failNum +=1
                homepage.logout()
            #登录错误
            else:

                homepage.loginerr(user[1],user[2])
                errInfo = homepage.find_element('x=>/html/body/div[2]/table/tbody/tr/td/div').text
                if user[4] == errInfo:
                    testResult = "PASS"
                else:
                    testResult = 'FAIL'
                    failNum += 1
                homepage.relogin()
            totalNum += 1
            loginFileResult.write('%s,%s,%s,%s,%s,%s,%s\n'%(user[0],user[1],user[2],user[3],user[4],testResult,errInfo))
        loginFile.close()
        loginFileResult.close()
        self.assertEqual(failNum,0,'总用例数：%d，失败用例数%d'%(totalNum,failNum))

    #登录执行正确后返回登录
    def test_ami_login_002(self):
        homepage = AmiHomePage(self.driver)
        #try:
        homepage.input_value('id=>USERNAME','admin')
        homepage.input_value('id=>PASSWORD','inhemeter')
        homepage.find_element('xpath=>//*[@value="登录"]').click()
        homepage.click('xpath=>//*[@value="返回"]')
        verify = homepage.find_element('xpath=>//*[@value="登录"]').get_attribute('value')
        # verify = homepage.find_element('xpath=>/html/body/div/div[4]/div/div[3]/form/input').get_attribute('value')
        # print("66666666666" +verify)
        self.assertEqual(verify,'登录','执行测试失败---FAIL')

    #登录错误后点击重新登录
    def test_ami_login_003(self):
        homepage = AmiHomePage(self.driver)
        homepage.loginerr('admin','inhe')
        homepage.relogin()
        verify = homepage.find_element('xpath=>/html/body/div/div[4]/div/div[3]/form/input').get_attribute('value')
        self.assertEqual(verify, '登录', '执行测试失败---FAIL')
























