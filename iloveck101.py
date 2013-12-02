import os
import sys
import re
from cStringIO import StringIO

import requests
from PIL import Image
from lxml import etree

url = sys.argv[1]

m = re.match('thread-(\d+)-.*', url.rsplit('/', 1)[1])
thread_id = m.group(1)

if not os.path.exists('images'):
    os.mkdir('images')

folder = os.path.join('images', thread_id)
if not os.path.exists(folder):
    os.mkdir(folder)


resp = requests.get(url)
html = etree.HTML(resp.content)
image_urls = html.xpath('//img/@file')

for image_url in image_urls:
    filename = image_url.rsplit('/', 1)[1]

    try:
        resp = requests.get(image_url)
    except requests.exceptions.MissingSchema:
        continue

    im = Image.open(StringIO(resp.content))
    width, height = im.size
    if width < 400 or height < 400:
        continue

    with open(os.path.join(folder, filename), 'wb+') as f:
        f.write(resp.content)
