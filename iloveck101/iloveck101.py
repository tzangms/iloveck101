import os
import sys
import re
from cStringIO import StringIO

import requests
from PIL import Image
from lxml import etree


def iloveck101(url):
    """
    download images from given ck101 URL
    """

    # find thread id
    m = re.match('thread-(\d+)-.*', url.rsplit('/', 1)[1])
    thread_id = m.group(1)

    # create image folder
    if not os.path.exists('images'):
        os.mkdir('images')

    # fetch html and find images
    resp = requests.get(url)
    if resp.status_code != 200:
        sys.exit('Oops')


    # parse html
    html = etree.HTML(resp.content)

    # title
    try:
        title = html.find('.//title').text.split(' - ')[0].strip()
    except AttributeError:
        sys.exit('There is no content, please try again.')

    # create target folder for saving images
    folder = os.path.join('images', "%s - %s" % (thread_id, title))
    if not os.path.exists(folder):
        os.mkdir(folder)

    # iterate and save images
    image_urls = html.xpath('//img/@file')
    for image_url in image_urls:
        filename = image_url.rsplit('/', 1)[1]

        # ignore useless image
        if not image_url.startswith('http'):
            continue

        # fetch image
        print 'Fetching %s ...' % image_url
        resp = requests.get(image_url)

        # ignore small images
        im = Image.open(StringIO(resp.content))
        width, height = im.size
        if width < 400 or height < 400:
            continue

        # save image
        with open(os.path.join(folder, filename), 'wb+') as f:
            f.write(resp.content)


def main():
    try:
        url = sys.argv[1]
    except IndexError:
        sys.exit('Please provide URL from ck101')

    iloveck101(url)


if __name__ == '__main__':
    main()
