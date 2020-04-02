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


# Crawls website & returns dictionary (key=url, value=1)

    def crawl(self, url: str) -> dict:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, features="html.parser") 
        
        for a in soup.find_all('a', href=True):
            link = self.get_absolute_url(a['href'])
            if self.filter_url(link):
                self.add_url(link)
                print(self.visited[link])
                new_url = link
                try:
                    self.crawl(new_url)
                except:
                    pass


# Checks the following contitions:
# 1: if url has already been visited 
# 2: if url belongs to the original crawled website
# 3: if url has excluded regex patterns

    def filter_url(self, url: str) -> bool:
        if self.visited.get(url):
            return False
        if self.uri not in url:
            return False
        for obj in self.exclude:
            if obj in url:
                return False
        else:
            return True


# Returns absolute url if relative given

    def get_absolute_url(self, url: str) -> str:
        if self.uri not in url:
            if 'http' not in url and 'https' not in url  and "." not in url:
                link = self.uri + url
            else:
                return url
        else:
            link = url
        return link


# Adds url to dictionary

    def add_url(self, url: str) -> None:
        self.visited[url] = 1


# Returns uri when url given 

    def get_parsed_uri(self, url: str) -> str:
        parsed_uri = urlparse(url)
        result = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
        return result

    