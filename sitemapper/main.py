from xml.etree.ElementTree import Element, tostring, SubElement
from xml.etree import ElementTree
from xml.dom import minidom
from urlcrawler import UrlCrawler
from urllib.parse import urlparse
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--url', action='store', default='', help='Type webstie URL, for example https://example.com')
parser.add_argument('--exclude', action='append', help="Type pattern which should be excluded from sitemap, for example \'example/about\' ")

args = parser.parse_args()
url = args.url.rstrip("/")

print(args.exclude)

crawler = UrlCrawler(file_format=args.file_format, exclude=args.exclude, url=url)
    

crawler.crawl(url, crawler.uri)


sitemap = Element('sitemap')

for obj in crawler.visited.keys():
    link = SubElement(sitemap, 'url')
    loc = SubElement(link, 'loc')
    link = crawler.visited[obj]
    loc.text = link


name = urlparse(url).netloc.replace('.', '_')
print(name)

mydata = tostring(sitemap, encoding='UTF-8')
dom = minidom.parseString(mydata)
pretty_xml_as_string = dom.toprettyxml()

with open((name + '.xml'), 'w') as myfile:
    myfile.write(pretty_xml_as_string)


