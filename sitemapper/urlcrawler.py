import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


class UrlCrawler(object):
    def __init__(self, url, exclude=None):
        self.visited = {}
        self.visited[url] = url
        self.exclude = exclude
        self.uri = self.get_parsed_uri(url)
        self.crawl(url, self.uri)

        
    def crawl(self, url, uri):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, features="html.parser") 
        print(len(self.visited))
        
        for a in soup.find_all('a'):
            link = self.get_absolute_url(a['href'])
            if self.filter_url(link):
                self.add_url(link)
                print(self.visited[link])
                new_url = link
                try:
                    self.crawl(new_url, uri)
                except:
                    pass

    def filter_url(self, url):
        if self.visited.get(url):
            return False
        if self.uri not in url:
            return False
        for obj in self.exclude:
            if obj in url:
                return False
        else:
            return True

    def get_absolute_url(self, url):
        if self.uri not in url:
            if 'http' not in url and 'https' not in url  and "." not in url:
                link = self.uri + url
            else:
                return url
        else:
            link = url
        return link

    def add_url(self, url):
        self.visited[url] = url


    def get_parsed_uri(self, url):
        parsed_uri = urlparse(url)
        result = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
        return result

    