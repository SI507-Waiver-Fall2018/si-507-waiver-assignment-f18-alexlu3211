# Full Name: Alex Lu
# UMID     : 54523810

import requests
from bs4 import BeautifulSoup

url = "http://michigandaily.com"

def parse_source(soup):

    articles = []

    for link in soup.find("div", attrs={'class': 'view-most-read'}).find_all("a"):
        articles.append({'href': link.get('href'), 'title': link.contents[0]})

    return articles


def parse_author(article_soup):

    if article_soup.select("a[href*=author]") == []:
        author = article_soup.find("p", attrs={'class': 'info'}).contents[0]
        if author.lower().startswith("by"):
            return author[3:]
        else:
            return author
    else:
        return article_soup.select("a[href*=author]")[0].contents[0]


if __name__ == '__main__':

    print("Michigan Daily -- MOST READ")

    source = requests.get(url).text
    soup = BeautifulSoup(source, 'html.parser')

    most_read = parse_source(soup)

    for article in most_read:
        article_source = requests.get(url + article['href']).text
        article_soup = BeautifulSoup(article_source, 'html.parser')
        print(article['title'])
        print("\tBy %s" % parse_author(article_soup))