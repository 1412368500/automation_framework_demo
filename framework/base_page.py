# coding=utf-8
import configparser
import time
from selenium.common.exceptions import NoSuchElementException
import os.path

from framework.browser_engine import BrowserEngine
from framework.logger import Logger

# create a logger instance
logger = Logger(logger="BasePage").getlog()


class BasePage(object):
    """
    定义一个页面基类，让所有页面都继承这个类，封装一些常用的页面操作方法到这个类
    """
    img_path = None
    def __init__(self, driver):
        self.driver = driver
        self.to_home_url()
        # self.driver.switch_to_default_content()


        # quit browser and end testing

    def quit_browser(self):
        # self.driver.click('xpath=>//*[@title="退出"]')
        # self.driver.click('id=>confirmModal_ok')
        self.driver.quit()

        # 浏览器前进操作

    def to_home_url(self):
        self.driver.get(BrowserEngine.base_url)

    def forward(self):
        self.driver.forward()
        logger.info("Click forward on current page.")

        # 浏览器后退操作

    def back(self):
        self.driver.back()
        logger.info("Click back on current page.")

        # 隐式等待

    def wait(self, seconds):
        self.driver.implicitly_wait(seconds)
        logger.info("wait for %d seconds." % seconds)

        # 点击关闭当前窗口

    def close(self):
        try:
            self.driver.close()
            logger.info("Closing and quit the browser.")
        except NameError as e:
            logger.error("Failed to quit the browser with %s" % e)

            # 保存图片

    def get_windows_img(self):
        if BasePage.img_path is None:
            config = configparser.ConfigParser()
            path = os.path.dirname(os.path.abspath('.')) + '/config/config.ini'
            config.read(path)
            BasePage.img_path = config.get("img", "screenshots")
        file_path = BasePage.img_path
        rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        screen_name = file_path + rq + '.png'
        try:
            self.driver.get_screenshot_as_file(screen_name)
            logger.info("Had take screenshot and save to folder : /screenshots")
        except NameError as e:
            logger.error("Failed to take screenshot! %s" % e)
            self.get_windows_img()

            # 定位元素方法

    def find(self, selector_by,selector_value):
        if not selector_by.strip():#空值
            return self.find_element(selector_value)
        else:
            return self.find_element(selector_by + '=>' + selector_value)

    def find_element(self, selector):
        """
         这个地方为什么是根据=>来切割字符串，请看页面里定位元素的方法
         submit_btn = "id=>su"
         login_lnk = "xpath => //*[@id='u1']/a[7]"  # 百度首页登录链接定位
         如果采用等号，结果很多xpath表达式中包含一个=，这样会造成切割不准确，影响元素定位
        :param selector:
        :return: element
        """
        element = ''
        print(selector + "是否包含=>标志分隔符： "+'=>' not in selector)
        if '=>' not in selector:
            return self.driver.find_element_by_id(selector)
        selector_by = selector.split('=>')[0]
        selector_value = selector.split('=>')[1]

        if selector_by == "i" or selector_by == 'id':
            try:
                element = self.driver.find_element_by_id(selector_value)
                logger.info("Had find the element \' %s \' successful "
                            "by %s via value: %s " % (element.text, selector_by, selector_value))
            except NoSuchElementException as e:
                logger.error("NoSuchElementException: %s" % e)
                self.get_windows_img()  # take screenshot
        elif selector_by == "n" or selector_by == 'name':
            element = self.driver.find_element_by_name(selector_value)
        elif selector_by == "c" or selector_by == 'class_name':
            element = self.driver.find_element_by_class_name(selector_value)
        elif selector_by == "l" or selector_by == 'link_text':
            element = self.driver.find_element_by_link_text(selector_value)
        elif selector_by == "p" or selector_by == 'partial_link_text':
            element = self.driver.find_element_by_partial_link_text(selector_value)
        elif selector_by == "t" or selector_by == 'tag_name':
            element = self.driver.find_element_by_tag_name(selector_value)
        elif selector_by == "x" or selector_by == 'xpath':
            try:
                element = self.driver.find_element_by_xpath(selector_value)
                logger.info("Had find the element \' %s \' successful "
                            "by %s via value: %s " % (element.text, selector_by, selector_value))
            except NoSuchElementException as e:
                logger.error("NoSuchElementException: %s" % e)
                self.get_windows_img()
        elif selector_by == "s" or selector_by == 'selector_selector':
            element = self.driver.find_element_by_css_selector(selector_value)
        else:
            raise NameError("Please enter a valid type of targeting elements.")

        return element

        # 输入

    def input_value(self, selector, text):

        el = self.find_element(selector)
        el.clear()
        try:
            el.send_keys(text)
            logger.info("Had type \' %s \' in inputBox" % text)
        except NameError as e:
            logger.error("Failed to type in input box with %s" % e)
            self.get_windows_img()

            # 清除文本框

    def clear(self, selector):

        el = self.find_element(selector)
        try:
            el.clear()
            logger.info("Clear text in input box before typing.")
        except NameError as e:
            logger.error("Failed to clear in input box with %s" % e)
            self.get_windows_img()

            # 点击元素

    def click(self, selector):

        el = self.find_element(selector)
        try:
            # logger.info("The element \' %s \' was clicked." % el.text)
            el.click()
        except NameError as e:
            logger.error("Failed to click the element with %s" % e)

            # 或者网页标题

    def get_page_title(self):
        logger.info("Current page title is %s" % self.driver.title)
        return self.driver.title

    def implicitly_wait(self,time):
        self.driver.implicitly_wait(time)
    @staticmethod
    def sleep(seconds):
        time.sleep(seconds)
        logger.info("Sleep for %d seconds" % seconds)

