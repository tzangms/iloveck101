# coding: utf-8

import unittest

from iloveck101.utils import parse_url


class CK101Test(unittest.TestCase):
    def setUp(self):
        self.url = 'http://ck101.com/thread-2818521-1-1.html'

    def test_parse_url(self):
        title, image_urls = parse_url(self.url)
        self.assertEqual(title, u'蔡依林+心凌的綜合體？！19歲「無名時代的正妹」陳敬宣現在正翻了......')
        self.assertEqual(len(image_urls), 39)


if __name__ == '__main__':
    unittest.main()
