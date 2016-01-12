"""
This doesnt work since the links to the articles are not in the html
file. Really, they aren't there.
"""


PROJECT = "http://techcrunch.com/search/microsoft#stq=microsoft&stp="

from bs4 import BeautifulSoup
from random import randint
import requests
from urllib2 import urlopen
import time
import os


custom_headers = {'content-encoding': 'gzip', 
                'User-Agent': 'My User Agent 0.1',
                'From': 'thinkxl@gmail.com'}

# this code is from github
# used to get all pages for microsoft search
def get_years_available(url):
    results = []
    
    def populate_results(count):
        new_url = url + str(count)
        r = requests.get(new_url, headers=custom_headers)
        if r.status_code == 200 and count <= 20:
            results.append(new_url)

            time.sleep(randint(0,4))
            populate_results(count + 1)
        else:
            pass

    populate_results(1)
    return results

# this is a cheap function used instead of the above one
# it generates urls
def get_urls(url):
    urls = []
    for i in range(1, 21):
        urls.append(url + str(i))
        print(url + str(i))
    return urls


# This method tries to do IO and get all the final URLs
def collect(urls):
    # this removes text.txt
    try:
        os.remove('text.txt')
    except OSError:
        pass
    
    #this remakes text.txt
    f = open('text.txt', 'w+')
    f.close()
    
    articles = []
    
    # open the html files
    for url in urls:
        html = urlopen(url)
        soup = BeautifulSoup(html, "html.parser")
    # this opens the file, filters, sorts, and puts the final URLs into
    # the text.txt file
    with open('text.txt', 'r+w+') as f:
        for link in soup.find_all('a'):
            articles.append(str(link.get('href')))
#        articles = filter(articles)
        sorted_urls = sort(articles)
        for link in sorted_urls:
            f.write(str(link[0]) + "\n")

# method to sort
def sort(links):
    # 21-25) is years
    years = []
    months = []
    for link in links:
        years.append(link[21:25])
        # 26-28) is month
        months.append(link[26: 28])
    url_tuples = zip(links, years, months)
    # sort using year then by month
    sort_year = sorted(url_tuples, key = lambda url: url[1])
    sort_month = sorted(sort_year, key = lambda url: url[2])
    return sort_month

# this filters the data to the stuff we want
def filter(links):
    articles = []
    for link in links:
        # Note that all we keep are stuff with microsoft and techcrunch
        # so no ads
        if ("microsoft" in link) and ("techcrunch.com/" in link):
            articles.append(link)
    return articles

def main():
    collect(get_urls(PROJECT))

if __name__ == '__main__':
    main()


