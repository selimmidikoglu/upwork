import threading
import schedule
from queue import Queue
from Spider import *
from LinkFormat import *
from ToolBox import *
from DataTransaction import DataTransaction
import time


#This class is the entry point of crawling

PROJECT_NAME = 'mynet_finans'
HOMEPAGE = 'http://finans.mynet.com/borsa/hisseler/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled_links.txt'
NUMBER_OF_THREADS = 8
link_queue = Queue()

#We create and set our spiders to crawl 5 different points of existing website
def initializeSpiders():
    homePageList = ['http://finans.mynet.com/borsa/hisseler/', 'http://finans.mynet.com/borsa/hisseler/c-e/',
                    'http://finans.mynet.com/borsa/hisseler/f-j/', 'http://finans.mynet.com/borsa/hisseler/k-q/',
                    'http://finans.mynet.com/borsa/hisseler/r-z/']

    for i in range(0,5):
        Spider(PROJECT_NAME,homePageList[i],DOMAIN_NAME)


    # HOMEPAGE1 = 'http://finans.mynet.com/borsa/hisseler/'
    # HOMEPAGE2 = 'http://finans.mynet.com/borsa/hisseler/c-e/'
    # HOMEPAGE3 = 'http://finans.mynet.com/borsa/hisseler/f-j/'
    # HOMEPAGE4 = 'http://finans.mynet.com/borsa/hisseler/k-q/'
    # HOMEPAGE5 = 'http://finans.mynet.com/borsa/hisseler/r-z/'
    #
    # Spider(PROJECT_NAME, HOMEPAGE1, DOMAIN_NAME)
    # Spider(PROJECT_NAME, HOMEPAGE2, DOMAIN_NAME)
    # Spider(PROJECT_NAME, HOMEPAGE3, DOMAIN_NAME)
    # Spider(PROJECT_NAME, HOMEPAGE4, DOMAIN_NAME)
    # Spider(PROJECT_NAME, HOMEPAGE5, DOMAIN_NAME)



# Create worker threads (will die when main exits)
def create_worker_spiders():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=spiders_shoot)
        t.daemon = True
        t.start()
def spiders_shoot():
    while True:
        url = link_queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        #spider_to_shoot=initializeSpiders()
        #print(spider_to_shoot)
        # for i in range(0,len(spider_to_shoot)):
        #     spider_to_shoot[i].crawl_page(threading.current_thread().name, url)
        link_queue.task_done()

# Each queued link is a new job
def targets_for_spiders():
    for link in file_to_set(QUEUE_FILE):
            link_queue.put(link)
    link_queue.join()
    crawlLinks()

# Check if there are items in the queue, if so crawl them
def crawlLinks():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        targets_for_spiders()

#Iterate through BIST 30 companies and get all the comments
def makeTransaction():
    transaction=DataTransaction('mynet_finans')
    transaction.visitPages()

#iterate through BIST 30 companies and control any new comments put if so change the existing files accordingly
def updateComments():
    transaction = DataTransaction('mynet_finans')
        append_to_file('mynet_finans/crawled_links.txt', 'http://finans.mynet.com/borsa/hisseler/petkm-petkim/')
        #append_to_file('myney_finans/crawled_links.txt', 'http://finans.mynet.com/borsa/hisseler/petkm-petkim/')
        print("Spiders found all the necessary links within: " + "--- %s seconds ---" % (time.time() - spider_system_start_time))

#Visit the links and get all the comments, will be base data of the system in json format
def bootCommentGetterSystem():
    comment_getter_system_start_time = time.time()
    makeTransaction()
    print("System boot completed within: " + "--- %s seconds ---" % (time.time() - comment_getter_system_start_time))

#Visit the pages again and control whether or not a new comment is posted and update the json files
def updateSystem():
    start_time2=time.time()
    updateComments()
    print('System update completed within: '+ "--- %s seconds ---" % (time.time() - start_time2))

timeout=60
#Update system will begin every 60 minutes
def applySchedule():
    schedule.every(timeout).minutes.do(updateSystem())

    while True:
        schedule.run_pending()
        time.sleep(1)

# bootSpiderSystem()
#bootCommentGetterSystem()
updateSystem()
