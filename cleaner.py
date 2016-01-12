import os, errno

def filter(year):
    articles = []

    with open("test.txt", "r+w+") as f:
        links = f.read().splitlines()
        for link in links:
            if ("techcrunch.com/" + year) in str(link):
                articles.append(str(link))
        for article in articles:
            if "#" in article:
                articles.remove(article)
    
        articles = articles[::2]
        f.seek(0)
        f.truncate()
        for article in articles:
            f.write(article + "\n")
   

    return articles

filter('2009')
