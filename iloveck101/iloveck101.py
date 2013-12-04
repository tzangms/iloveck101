import os
import sys
import re

import gevent
from gevent import monkey

monkey.patch_all()

import requests
from lxml import etree
from utils import get_image_info

REQUEST_HEADERS = {'User-agent': 'Mozilla/5.0'}

def iloveck101(url):
    """
    download images from given ck101 URL
    """

    # find thread id
    m = re.match('thread-(\d+)-.*', url.rsplit('/', 1)[1])
    if not m:
        sys.exit('URL pattern should be something like this: http://ck101.com/thread-2593278-1-1.html')

    thread_id = m.group(1)

    # create `iloveck101` folder in ~/Pictures
    home = os.path.expanduser("~")
    base_folder = os.path.join(home, 'Pictures/iloveck101')
    if not os.path.exists(base_folder):
        os.mkdir(base_folder)


    # fetch html and find images
    for attemp in range(3):
        resp = requests.get(url, headers=REQUEST_HEADERS)
        if resp.status_code != 200:
            print 'Retrying ...'
            continue

        # parse html
        html = etree.HTML(resp.content)

        # title
        try:
            title = html.find('.//title').text.split(' - ')[0].replace('/', '').strip()
            break
        except AttributeError:
            print 'Retrying ...'
            continue

    # create target folder for saving images
    folder = os.path.join(base_folder, "%s - %s" % (thread_id, title))
    if not os.path.exists(folder):
        os.mkdir(folder)

    # iterate and save images
    image_urls = html.xpath('//img/@file')

    def process_image_worker(image_url):
        filename = image_url.rsplit('/', 1)[1]

        # ignore useless image
        if not image_url.startswith('http'):
            return

        # fetch image
        print 'Fetching %s ...' % image_url
        resp = requests.get(image_url)

        # ignore small images
        content_type, width, height = get_image_info(resp.content)
        if width < 400 or height < 400:
            return

        # save image
        with open(os.path.join(folder, filename), 'wb+') as f:
            f.write(resp.content)

    jobs = [gevent.spawn(process_image_worker, image_url)
            for image_url in image_urls]
    gevent.joinall(jobs)


def main():
    try:
        url = sys.argv[1]
    except IndexError:
        sys.exit('Please provide URL from ck101')

    iloveck101(url)


if __name__ == '__main__':
    main()
