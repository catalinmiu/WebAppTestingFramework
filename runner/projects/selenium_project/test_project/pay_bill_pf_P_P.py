import sys, os
import unittest
sys.path.append("ib")

from parameterized import parameterized

from selenium import webdriver

class PayBillPfPP(unittest.TestCase):
    LINE_START_TEST = 2

    # LINE_END_TEST = 91
    LINE_END_TEST = 92

    @parameterized.expand([
        ["3123123foo", "1"],
        ["23123123bar", "2"],
        ["123123lee", "3"],
    ])
    def test_pay_bill_pf_p_p(self, name, i):
        print(name)
        self.driver = webdriver.Chrome()
        self.driver.get("www.google.com")

