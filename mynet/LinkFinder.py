from html.parser import HTMLParser
from urllib import parse

#This class has a method that finds the links that is called by gather_links when we call feed the html code automatically handle starttag method is called
#Basically we parse the HTML code and it finds its links
class LinkFinder(HTMLParser):

    def __init__(self, base_url, page_url):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()
        self.MAX_LIMIT=300

    # When we call HTMLParser feed() this function is called when it encounters an opening tag <a>
    def handle_starttag(self, tag, attrs):
            if tag == 'a':
                for (attribute, value) in attrs:
                    if attribute == 'href':
                        url = parse.urljoin(self.base_url, value)
                        self.links.add(url)
    #Return links
    def page_links(self):
        return self.links
    def error(self, message):
        pass




