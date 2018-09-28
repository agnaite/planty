# -*- coding: utf-8 -*-

from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import unittest

class IntegrationTests(unittest.TestCase):
    """Tests overall app functionality"""

    def setUp(self):
        self.driver = webdriver.PhantomJS()

    def test_webserver_works(self):
        self.driver.get("http://localhost:5000")
        self.assertNotEqual(self.driver.page_source, '')

    def test_homepage_loads(self):
        """Checks if homepage loads"""

        self.driver.get("http://localhost:5000")
        self.assertIn("planty", self.driver.title)

    def tearDown(self):
        self.driver.quit()

# runs the unit tests in the module
if __name__ == '__main__':
    unittest.main()
