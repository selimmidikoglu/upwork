import urllib.request
import datetime
from datetime import datetime,timedelta
import mechanicalsoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium import webdriver
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import threading

# client = MongoClient()
# db = client['web']
# collection = db['fixel']
# br = mechanicalsoup.Browser()
# br.addheaders = [('User-agent', 'PhantomJS')]
# browser = webdriver.PhantomJS()

class myThread (threading.Thread):

   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
   def run(self):
       main_func(self.counter)

site= "http://www.hisse.net/topluluk/showthread.php?t=6&page=16"
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

#url = "http://www.fixelborsa.com/sembolDetay.html#"
client = MongoClient()
db = client['web']
collection = db['hissenet']


def get_total_page(browser,url):
    browser.get(url)
    print("url is" + str(url))
    total = browser.find_element_by_xpath('//*[@id="yui-gen6"]')
    total_page = int(float(total.get_attribute('innerHTML').split('/')[1]))
    print("Total page I got is " + str(total_page))
    return total_page


def get_browser():
    br = mechanicalsoup.Browser()
    br.addheaders = [('User-agent', 'PhantomJS')]
    browser = webdriver.PhantomJS('/Users/nihadazimli/PycharmProjects/quantsol-text/web-crawler ')
    return browser

def get_data(browser,url,company):
    browser.get(url)

    # find total page count


    # get all comment info and comment
    allDivs = browser.find_elements_by_xpath('//*[@class="postbit postbitim postcontainer old"]')
    print()

    for x in range(8):
        one_object = allDivs[x].get_attribute('innerHTML')
        print("############################")
        number = allDivs[x].find_element_by_class_name('nodecontrols').get_attribute('innerHTML').split('<a name="post')[1][:10].split('"')[0]
        post_comment = "post_message_" + str(number)
        post_date = "post_" + str(number)
        print(post_comment)
        print(post_date)
        date = allDivs[x].find_element_by_xpath('//*[@id="%s"]/div[1]/div[1]/span[1]/span'% post_date ).text
        username = one_object.split('<strong>')[1].split('</strong>', 1)[0]
        comment = allDivs[x].find_element_by_xpath('//*[@id="%s"]/blockquote' % post_comment).text
        if date[:5] == "Bugün":
            date_y = time.strftime("%d-%m-%Y")
            print(type(date_y))
            date = date_y + date[-7:]
        elif date[:3] == "Dün":
            yesterday = datetime.today() - timedelta(1)
            date_y = yesterday.strftime('%d-%m-%Y')
            date = date_y + date[-7:]

        date_time = datetime.strptime(date, "%d-%m-%Y, %H:%M")

        print(username)
        print(date)
        print(comment)

        try:
            db.hissenet.insert_one({'_id': number,'username': username, 'date': date_time, 'comment': comment,
                                    'company name': company})
        except DuplicateKeyError:
            print("Duplicate value cannot insert")

    #print(last)


def main_func(counter):
    company_list = ["http://www.hisse.net/topluluk/showthread.php?t=6&page=",
                    'http://www.hisse.net/topluluk/showthread.php?t=142&page=',
                    'http://www.hisse.net/topluluk/showthread.php?t=23&page=',
                    'http://www.hisse.net/topluluk/showthread.php?t=295&page=',
                    'http://www.hisse.net/topluluk/showthread.php?t=323&page=',
                    'http://www.hisse.net/topluluk/showthread.php?t=279&page=',
                    'http://www.hisse.net/topluluk/showthread.php?t=209&page=',
                    'http://www.hisse.net/topluluk/showthread.php?t=152&page=',
                    'http://www.hisse.net/topluluk/showthread.php?t=196&page=',
                    'http://www.hisse.net/topluluk/showthread.php?t=176&page=',
                    'http://www.hisse.net/topluluk/showthread.php?t=318&page=',
                    'http://www.hisse.net/topluluk/showthread.php?t=6722&page=',
                    'http://www.hisse.net/topluluk/showthread.php?t=18&page=',
                    'http://www.hisse.net/topluluk/showthread.php?t=355&page=',
                    'http://www.hisse.net/topluluk/showthread.php?t=245&page=',
                    'http://www.hisse.net/topluluk/showthread.php?t=336&page=',
                    'http://www.hisse.net/topluluk/showthread.php?t=310&page=',
                    'http://www.hisse.net/topluluk/showthread.php?t=268&page=',
                    'http://www.hisse.net/topluluk/showthread.php?t=5331&page=',
                    'http://www.hisse.net/topluluk/showthread.php?t=154&page=',
                    'http://www.hisse.net/topluluk/showthread.php?t=291&page=',
                    'http://www.hisse.net/topluluk/showthread.php?t=303&page=',
                    'http://www.hisse.net/topluluk/showthread.php?t=326&page=',
                    'http://www.hisse.net/topluluk/showthread.php?t=143&page=',
                    'http://www.hisse.net/topluluk/showthread.php?t=263&page=',
                    'http://www.hisse.net/topluluk/showthread.php?t=316&page=',
                    'http://www.hisse.net/topluluk/showthread.php?t=8611&page=',
                    'http://www.hisse.net/topluluk/showthread.php?t=7070&page=',
                    'http://www.hisse.net/topluluk/showthread.php?t=235&page=',
                    'http://www.hisse.net/topluluk/showthread.php?t=91&page=']

    keywords = ['AKBNK', 'GARAN', 'BIMAS', 'TUPRS', 'TCELL', 'SAHOL', 'ISCTR', 'EREGL',
                'KCHOL','HALKB', 'EKGYO','THYAO', 'ARCLK', 'VAKBN', 'PETKM', 'YKBNK',
                'TOASO', 'SISE', 'ASELS', 'ENKAI', 'ULKER', 'TTKOM', 'TAVHL','FROTO',
                'SODA', 'TKFEN', 'KRDMD', 'MAVI', 'KOZAL','DOHOL']

    for y in range(int(len(keywords)/10)):
        index = y*10+counter
        company_url = company_list[index]+"1"
        browser=get_browser()
        print("Company name is: " + keywords[index]+ "\nLinks of companies: " +company_list[index] )
        ranger = get_total_page(browser,company_list[index])
        print("Total Page Number is : " + str(ranger))
        for x in range(1,ranger):
            company_url = company_list[index]+str(x)
            get_data(browser,company_url,keywords[index])



#count_comment()
thread1 = myThread(1, "Thread-1", 0)
thread2 = myThread(2, "Thread-2", 1)
thread3 = myThread(3, "Thread-3", 2)
thread4 = myThread(4, "Thread-4", 3)
thread5 = myThread(5, "Thread-5", 4)
thread6 = myThread(6, "Thread-6", 5)
thread7 = myThread(7, "Thread-7", 6)
thread8 = myThread(8, "Thread-8", 7)
thread9 = myThread(9, "Thread-9", 8)
thread10 = myThread(10, "Thread-10", 9)

# Start new Threads
thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread5.start()
thread6.start()
thread7.start()
thread8.start()
thread9.start()
thread10.start()
