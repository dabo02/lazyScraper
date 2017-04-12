from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup

# if query is not None:
#     url = url + '?s=' + query
#
# html = urlopen(url)
# first_traverse = BeautifulSoup(html, 'html.parser')
# all_links_page_1 = first_traverse.find_all('a')
# paginator_links = []
# links_needed_page_1 = []
# for link in all_links_page_1:
#     if link.get('rel') == ['bookmark']:
#         links_needed_page_1.append(link.get('href'))
#     elif link.get('href') is not None and link.get('title') and ('page' in link.get('href')):
#         paginator_links.append(link.get('href'))
#
# second_traverse = []
# for link in links_needed_page_1:
#     tmp = BeautifulSoup(urlopen(link), 'html.parser')
#     second_traverse.append(tmp)
#
# all_links_page_2 = []
# links_needed_page_2 = []
# for bsObject in second_traverse:
#     all_links_page_2 = bsObject.find_all('a')
#     title = bsObject.title.string
#     title = title.replace(" ", "") + '.pdf'
#     for link in all_links_page_2:
#         if link.get('target'):
#             if '.pdf' in link.get('href'):
#                 print("Downloading: " + title)
#                 urlretrieve(link.get('href'), '/home/dabo02/Downloads/MyShit/' + title)
#                 print(title + ": Downloaded")

class MyLazyBookScraper:

    def __init__(self, query, download_path):
        self.url = 'http://www.allitebooks.com/'
        self.download_path = download_path
        query = query.replace(" ", "&")
        if query is not None:
            url = self.url + '?s=' + query
        self.query = query
        self.html = urlopen(url)
        self.first_traverse = BeautifulSoup(self.html, 'html.parser')
        self.all_links_page_1 = self.first_traverse.find_all('a')
        self.paginator_links = []
        self.links_needed_for_page = []

    def first_traverse(self):
        for link in self.all_links_page_1:
            if link.get('rel') == ['bookmark']:
                self.links_needed_for_page.append(link.get('href'))
            elif link.get('href') is not None and link.get('title') and ('page' in link.get('href')):
                self.paginator_links.append(link.get('href'))
        return self.paginator_links
    
    def get_links(self, link):
        html = urlopen(link)
        traverse = BeautifulSoup(html, 'html.parser')
        return traverse.find_all('a')
    
    def set_links(self, links):
        for link in links:
            if link.get('rel') == ['bookmark']:
                self.links_needed_for_page.append(link.get('href'))
    
    def download_books(self, traverser):
        for bsObject in traverser:
            all_links_from_page = bsObject.find_all('a')
            title = bsObject.title.string
            title = title.replace(" ", "") + '.pdf'
            for link in all_links_from_page:
                if link.get('target'):
                    if '.pdf' in link.get('href'):
                        print("Downloading: " + title)
                        urlretrieve(link.get('href'), self.download_path + title)
                        print(title + ": Downloaded")

    def fix_paginator_links(self, pagination):
        last_link = pagination[len(pagination)-1]
        self.paginator_links = []
        for i in range(len(pagination)):
            if i == 0 or i == 1:
                pass
            elif i == len(pagination)-1:
                self.paginator_links.append(self.url +'page/' + str(i) + '?s=' + self.query)
                self.paginator_links.append(last_link)
            else:
                self.paginator_links.append(self.url +'page/' + str(i) + '?s=' + self.query)

    def all_traverses(self, links):
        self.traverser = []
        for link in links:
            tmp = BeautifulSoup(urlopen(link), 'html.parser')
            self.traverser.append(tmp)



if __name__ == '__main__':
    q = input("Enter Search Query: ")
    path = input("Enter Download Path: ")
    bd = MyLazyBookScraper(q, path)
    pag = bd.first_traverse()
    bd.fix_paginator_links(pag)
    for link in bd.paginator_links:
        links = bd.get_links(link)
        bd.set_links(links)
        bd.all_traverses(bd.links_needed_for_page)
        bd.download_books(bd.traverser)