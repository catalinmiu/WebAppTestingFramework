import unittest

class TestPythonTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://www.python.org')

    def test1(self):
        self.assertIn('Python', self.driver.title)

    def test2(self):
        elem = self.driver.find_element_by_name('q')
        elem.clear()
        elem.send_keys('pycon')
        elem.send_keys(Keys.RETURN)
        self.assertNotIn('No results found.', self.driver.page_source)

    def tearDown(self):
        self.driver.close()

class TestPythonTest2(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://www.python.org')

    def test3(self):
        self.assertIn('Python', self.driver.title)

    def tearDown(self):
        self.driver.close()
