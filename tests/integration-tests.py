# -*- coding: utf-8 -*-

from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import unittest


class IntegrationTests(unittest.TestCase):
    """Tests overall app functionality"""

    def setUp(self):
        self.driver = webdriver.PhantomJS()
        self.driver.get("http://localhost:5000")

    def test_homepage_loads(self):
        """Checks if homepage loads"""

        driver = self.driver

        self.assertIn("planty", driver.title)

    def test_search_for_plant(self):
        """Checks if able to search for a plant by name"""

        driver = self.driver

        element = driver.find_element_by_name("plant-name")
        element.send_keys("orchid")
        element.send_keys(Keys.RETURN)

        assert "Orchid Plant" in driver.page_source
        assert "No plants found." not in driver.page_source
        links = driver.find_elements_by_link_text('Orchid')

        links[0].click()
        assert "Orchidaceae" in driver.page_source

    def tearDown(self):
        self.driver.quit()


# runs the unit tests in the module
if __name__ == '__main__':
    unittest.main()
