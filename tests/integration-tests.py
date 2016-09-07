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


    def test_search_for_plant(self):
        """Checks if able to search for a plant by name"""

        self.driver.get("http://localhost:5000")

        element = self.driver.find_element_by_name("plant-name")
        element.send_keys("orchid")
        element.send_keys(Keys.RETURN)

        self.assertIn("Orchid Plant", self.driver.page_source)
        self.assertNotIn("No plants found.", self.driver.page_source)
        links = self.driver.find_elements_by_link_text('Orchid')

        links[0].click()
        self.assertIn("Orchidaceae", self.driver.page_source)


    def tearDown(self):
        self.driver.quit()


# runs the unit tests in the module
if __name__ == '__main__':
    unittest.main()
