
from urllib.parse import urlparse

# Get domain name (example.com)
def get_domain_name(url):
    try:
        results = get_sub_domain_name(url).split('.')
        return results[-2] + '.' + results[-1]
    except:
        return ''
#When we pass an url it eleminates the unwanted directories

def returnformat(url):
    results=url[0:39]
    return results

#Our base url that we start crawling
def formaturl():
        results="http://finans.mynet.com/borsa/hisseler/"
        return results

#Controlling whether or not the current url belongs to BIST 30 lists
def contains(url):
    bist_30_set = {'akbnk', 'garan', 'bimas', 'tuprs', 'tcell', 'sahol', 'isctr', 'eregl', 'kchol', 'halkb', 'ekgyo',
                   'thyao', 'arclk', 'vakbn', 'petkim', 'ykbnk', 'toaso', 'sise', 'asels', 'enka', 'ulker', 'ttkom',
                   'tavhl', 'froto', 'soda', 'tkfen', 'krdmd', 'mavi', 'kozal', 'otkar','c-e','f-j','k-q','r-z'}
    #print(url[39:44])
    if url[39:44] in bist_30_set:
        return 1
    if url[39:43] in bist_30_set:
        return 1
    if url[39:42] in bist_30_set:
        return 1
    else:
        return 0

# Get sub domain name (name.example.com)
def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc

    except:
        return ''
