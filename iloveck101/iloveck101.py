import os
import sys
import re

import gevent
from gevent import monkey

monkey.patch_all()

import requests
from lxml import etree
from utils import get_image_info
from more_itertools import chunked

REQUEST_HEADERS = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'}
BASE_URL = 'http://ck101.com/'
CHUNK_SIZE = 3


def iloveck101(url):
    """
    Determine the url is valid. And check if the url contains any thread link or it's a thread.
    """

    if 'ck101.com' in url:
        if 'thread' in url:
            retrieveThread(url)
        else:
            for thread in retrieveThreadList(url):
                if thread is not None:
                    retrieveThread(thread)
    else:
        sys.exit('This is not ck101 url')


def retrieveThreadList(url):
    """
    The url may contains many thread links. We parse them out.
    """

    resp = requests.get(url, headers=REQUEST_HEADERS)

    # parse html
    html = etree.HTML(resp.content)

    links = html.xpath('//a/@href')
    if links:
        for link in links:
            yield link
    else:
        yield None


def retrieveThread(url):
    """
    download images from given ck101 URL
    """

    # check if the url has http prefix
    if not url.startswith('http'):
        url = BASE_URL + url

    # find thread id
    m = re.match('thread-(\d+)-.*', url.rsplit('/', 1)[1])
    if not m:
        return

    print '\nVisit %s' % (url)

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
        resp = requests.get(image_url, headers=REQUEST_HEADERS)

        # ignore small images
        content_type, width, height = get_image_info(resp.content)
        if width < 400 or height < 400:
            print "image is too small"
            return

        # save image
        with open(os.path.join(folder, filename), 'wb+') as f:
            f.write(resp.content)

    for chunked_image_urls in chunked(image_urls, CHUNK_SIZE):
        jobs = [gevent.spawn(process_image_worker, image_url)
                for image_url in chunked_image_urls]
        gevent.joinall(jobs)


def main():
    try:
        url = sys.argv[1]
    except IndexError:
        sys.exit('Please provide URL from ck101')

    iloveck101(url)


if __name__ == '__main__':
    main()
