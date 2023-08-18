from pygooglenews import GoogleNews

def getPublisher(title):
    title_length = len(title)
    publisher = ""
    for i in range(title_length - 1, -1, -1):
        if title[i] == "-":
            if title[i + 1] == " ":
                publisher = publisher[1::]
                break
        publisher = title[i] + publisher
    return publisher

def getArticles(topic):
    articles = []
    gn = GoogleNews(country = 'US')
    search = gn.search(topic)
    newsitems = search['entries']
    for item in newsitems:
        publisher = getPublisher(item.title)
        article = {
            'title': item.title,
            'link' : item.link,
            'publisher' : publisher,
            'selected': False
        }
        articles.append(article)
    return articles