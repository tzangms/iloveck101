import sys
import requests
from requests.exceptions import MissingSchema

from lxml import etree

url = sys.argv[1]

resp = requests.get(url)

html = etree.HTML(resp.content)
image_urls = html.xpath('//img/@file')

for image_url in image_urls:
    filename = image_url.rsplit('/', 1)[1]

    try:
        resp = requests.get(image_url)
    except MissingSchema:
        continue

    with open(filename, 'wb+') as f:
        f.write(resp.content)
