import unittest

from app.views.base import app


class HomePageTestCase(unittest.TestCase):
    """ Test application home page """

    def setUp(self):
        """ Open home page before test load """

        # Use flask tools for tests
        self.app = app.test_client()
        self.home = self.app.get('/')

    def test_home_page_access(self):
        """ Check home page access """

        self.assertEqual(self.home.status_code, 200)

    def test_check_js_files(self):
        """ Check that all Javascript files exist on this page """

        js_files = ['jquery.min.js', 'wookmark.min.js', 'imageloaded.min.js',
                    'instagram.min.js', 'tumblr.min.js', 'main.js']
        home_page_data = self.home.data

        for js_file in js_files:
            self.assertIn(js_file, home_page_data)


if __name__ == '__main__':
    unittest.main()
