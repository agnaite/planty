from unittest import TestCase
from server import app
from model import Plant, connect_to_db, db, example_data


class FlaskTestsRoutes(TestCase):
    """Test Flask route functionality"""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def tearDown(self):
        pass

    def test_index(self):
        """Test homepage page."""

        result = self.client.get("/")
        self.assertIn("Search", result.data)

    def test_new_plant_form(self):
        """Tests that route /new_plant loads."""

        result = self.client.get("/new_plant")
        self.assertIn("Add a new plant", result.data)

# runs the unit tests in the module
if __name__ == '__main__':
    unittest.main()
