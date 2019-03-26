# coding=utf-8
from framework.base_page import BasePage


class HomePage(BasePage):
    input_box = "id=>kw"
    search_submit_btn = "xpath=>//*[@id='su']"

    def type_search(self, text):
        self.input_value(self.input_box, text)

    def send_submit_btn(self):
        self.click(self.search_submit_btn)
