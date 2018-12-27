import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class TestPythonWebsite(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://www.python.org')

    def test_page_title(self):
        self.assertIn('Python', self.driver.title)

    def test_search_pycon(self):
        elem = self.driver.find_element_by_name('q')
        elem.clear()
        elem.send_keys('pycon')
        elem.send_keys(Keys.RETURN)
        self.assertNotIn('No results found.', self.driver.page_source)

    def tearDown(self):
        self.driver.close()
