from xml.etree.ElementTree import Element, tostring, SubElement
from xml.etree import ElementTree
from xml.dom import minidom
from urlcrawler import UrlCrawler
from urllib.parse import urlparse
import argparse

# Parsing aguments

parser = argparse.ArgumentParser()
parser.add_argument('--url', action='store', default='', help='Type webstie URL, for example https://example.com')
parser.add_argument('--exclude', action='append', help="Type pattern which should be excluded from sitemap, for example \'example/about\' ")

args = parser.parse_args()
url = args.url.rstrip("/")


# UrlCrawler instance initialization

crawler = UrlCrawler(exclude=args.exclude, url=url)
    

# Start crawling

crawler.crawl(url)


# XML tree building

sitemap = Element('sitemap')

for key in crawler.visited.keys():
    link = SubElement(sitemap, 'url')
    loc = SubElement(link, 'loc')
    loc.text = key


# Parsing tree to string & encoding to UTF-8

mydata = tostring(sitemap, encoding='UTF-8')
dom = minidom.parseString(mydata)
pretty_xml_as_string = dom.toprettyxml()


# XML file creation

name = urlparse(url).netloc.replace('.', '_')

with open((name + '.xml'), 'w') as myfile:
    myfile.write(pretty_xml_as_string)


