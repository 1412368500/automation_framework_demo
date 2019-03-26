# coding=utf-8
import time

from selenium.webdriver.chrome import webdriver

from framework.base_page import BasePage

class AmiHomePage(BasePage):
    input_box_one = "id=>USERNAME"
    input_box_two="PASSWORD"  #默认id
    search_submit_btn = "xpath=>//*[@value='登录']"
    search_submit_btn_two = "xpath=>//*[@value='进入系统']"
    #登陆
    def login(self, username,psd):
        self.input_value(self.input_box_one, username)
        self.input_value(self.input_box_two, psd)
        self.click(self.search_submit_btn)  #点击登陆
        self.implicitly_wait(1)
        self.click(self.search_submit_btn_two)#点击进入系统

    #退出登陆
    def logout(self):
        self.driver.switch_to_default_content()
        self.click('xpath=>//*[@title="退出"]')
        self.click('id=>confirmModal_ok')

    def loginerr(self, username, psd):
        self.input_value(self.input_box_one, username)
        self.input_value(self.input_box_two, psd)
        self.click(self.search_submit_btn)  # 点击登陆
    def relogin(self):
        self.click('xpath=>/html/body/div[3]/input')#提示用户名或密码错误后点击重新登陆



