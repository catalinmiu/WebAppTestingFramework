import unittest
from selenium.webdriver import Chrome
from selenium.webdriver.firefox.options import Options


class TestDuck(unittest.TestCase):
    def setUp(self):
        # opts = Options()
        # opts.set_headless()
        # assert opts.headless  # Operating in headless mode
        # self.browser = Chrome(options=opts)
        self.browser = Chrome()

    def test_search_input_homepage(self):
        """test1"""
        self.browser.get('https://duckduckgo.com')

        search_form = self.browser.find_element_by_id('search_form_input_homepage')
        search_form.send_keys('real python')
        search_form.submit()

        results = self.browser.find_elements_by_class_name('result')
        print(results[0].text)

    def tearDown(self):
        self.browser.close()
