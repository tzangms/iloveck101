# coding: utf-8

import os
import unittest

from iloveck101.utils import parse_url, get_image_info
from iloveck101.iloveck101 import iloveck101
from httmock import urlmatch, HTTMock


class CK101Test(unittest.TestCase):
    def setUp(self):
        self.url = 'http://ck101.com/thread-2818521-1-1.html'

    def test_iloveck101(self):

        @urlmatch(netloc=r'(.*\.)?ck101\.com$')
        def ck101_mock(url, request):
            return 'Feeling lucky, punk?'

        with HTTMock(ck101_mock):
            iloveck101(self.url)
        

class UtilsTest(unittest.TestCase):
    def setUp(self):
        self.url = 'http://ck101.com/thread-2818521-1-1.html'


    def test_parse_url(self):
        title, image_urls = parse_url(self.url)
        self.assertEqual(title, u'蔡依林+心凌的綜合體？！19歲「無名時代的正妹」陳敬宣現在正翻了......')
        self.assertEqual(len(image_urls), 39)


    def test_image_info(self):
        image = os.path.join('fixtures', 'jYY7oMF.jpg')
        test_dir = os.path.abspath(os.path.join(__file__, '..'))

        with open(os.path.join(test_dir, image)) as f:
            content_type, width, height = get_image_info(f.read())

        self.assertEqual(content_type, 'image/jpeg')
        self.assertEqual(width, 612)
        self.assertEqual(height, 612)


if __name__ == '__main__':
    unittest.main()
