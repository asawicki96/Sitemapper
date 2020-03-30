import sys, getopt
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from xml.etree.ElementTree import Element, tostring, SubElement
from xml.etree import ElementTree
from xml.dom import minidom


visited = {}

def main():
    try:
        options, args = getopt.getopt(sys.argv[1:], 'hu:f:')
    except getopt.GetoptError:
        print('main.py -u <site_url>')
        sys.exit()

    for option, arg in options:
        if option == '-h':
            print('main.py -u <site_url> -f <output_file_format>')
            sys.exit()

        elif option == '-u':
            url = arg
            sitemap = Sitemap(None, url)
      
        elif option == '-f':
            if arg.lower() in ('xml', 'txt', 'json'):
                file_format = arg
            else:
                print('Invalid output file format. Choose from: xml, txt.')


class Sitemap(object):
    def __init__(self, file_format, url):
        self.file_format = file_format
        self.visited = {}
        self.url = url
        self.base_uri = self.get_parsed_uri(url)
        self.get_hrefs(self.url, self.base_uri)
        self.create_xml_file(self.visited)

    def get_hrefs(self, url, base_uri):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, features="html.parser") 

        for a in soup.find_all('a'):
            link = self.get_absolute_url(a['href'])

            if not link in visited and base_uri in link[:(len(base_uri)+8)]:
                #print("Found the url:", link)
                #print(len(visited))

                self.visited[link] = link
                new_url = link
                try:
                    self.get_hrefs(new_url, base_url)
                except:
                    pass
    

    def get_absolute_url(self, url):
        if 'https://' not in url and 'http://' not in url:
            link = self.base_uri + url
        else:
            link = url
        return link


    def get_parsed_uri(self, url):
        parsed_uri = urlparse(url)
        result = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
        print(result)
        return result

    def create_xml_file(self, visited):
        sitemap = Element('sitemap')

        for node in visited:
            url = SubElement(sitemap, 'url')
            loc = SubElement(url, 'loc')
            loc.text = visited[node]

        name = 'blog_miduel'

        mydata = tostring(sitemap, encoding="unicode")
        dom = minidom.parseString(mydata)
        pretty_xml_as_string = dom.toprettyxml()
        myfile = open((name+'.xml'), 'w')
        myfile.write(pretty_xml_as_string)
        myfile.close()





######################################################
if __name__ == "__main__":
    main()
####################################################
