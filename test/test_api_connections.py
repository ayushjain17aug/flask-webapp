# -*- coding: utf-8 -*-
import unittest

from tumblpy import Tumblpy
from instagram.client import InstagramAPI

from config import settings


# Constatns
BASE_TAG = 'fun'
TEST_DATA_LIMIT = 2


# Base APIs authentication functions
def tumblr_connect():
    return Tumblpy(settings.TUMBLR_OAUTH_KEY, settings.TUMBLR_SECRET_KEY)

def instagram_connection():
    return InstagramAPI(client_id=settings.INSTAGRAM_CLIENT_ID,
                        client_secret=settings.INSTAGRAM_CLIENT_SECRET)


# Test APIs before run application
class ApiConnectiondTestCase(unittest.TestCase):
    """ Test connections on Tumblr and Instagram """

    def test_tumblr_connection(self):
        """ Test authentication on Tumblr """

        tumblr = tumblr_connect()
        auth_token = tumblr.get_authentication_tokens()
        token = auth_token['oauth_token']

        # Need check that authorization token exist
        self.assertTrue(isinstance(token, str))
        self.assertTrue(len(token) > 0)

    def test_get_tumblr_posts_and_photos(self):
        """ Get posts from tumblr and check photos in posts """

        tumblr = tumblr_connect()
        tumblr.get_authentication_tokens()
        posts = tumblr.get('tagged', params={'limit': TEST_DATA_LIMIT,
                                             'tag': BASE_TAG})

        # Check that result is correct
        self.assertEqual(len(posts), TEST_DATA_LIMIT)

        # All photos on page get from parametr "photos"
        for post in posts:
            # Note: Can crash if no photos in post
            self.assertTrue('photos' in post)

    def test_instagram_connection(self):
        """ Test authentication on Instagram """

        # Get crash if something wrong
        instagram_connection()


    def test_get_instagram_photos(self):
        """ Get photos from Instagram """

        instagram = instagram_connection()
        photos_ids = instagram.tag_recent_media(tag_name=BASE_TAG,
                                                count=TEST_DATA_LIMIT)[0]

        # Check that data exist in request
        self.assertEqual(len(photos_ids), TEST_DATA_LIMIT)


if __name__ == '__main__':
    unittest.main()
