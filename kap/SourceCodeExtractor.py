import threading

import time

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class MyThread(threading.Thread):
    """This thread is used to extract source code of notifications"""

    def __init__(self, thread_id, begin, end):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.begin = begin
        self.end = end

    def run(self):
        get_source_code(self.begin, self.end)


def get_source_code(begin, end):
    """Threads call method to get source code of notifications
       This method will extract all notifications with _ids between begin and end, both inclusive"""

    # this proxy usually works
    # if it doesn't, you can find free proxies on "https://free-proxy-list.net/"
    # European country proxies works better
    # PROXY = "37.120.250.132:8080"  # IP:PORT or HOST:PORT
    # PROXY = "88.99.149.188:31288"  # IP:PORT or HOST:PORT
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--proxy-server=%s' % PROXY)
    # isVPN = False
    # VPNcount = 0

    print("Getting source code..")
    driver = webdriver.Chrome()

    # connecting to MongoDB
    client = MongoClient()
    db = client.web
    collection = db.tmp

    ctime = time.time()
    items = list()
    for i in range(begin, end + 1):

        # if isVPN:
        #     VPNcount += 1
        #     if VPNcount > 15:
        #         driver.quit()
        #         driver = webdriver.Chrome()
        #         isVPN = False
        #         VPNcount = 0

        if i % 20 == 0:
            driver.delete_all_cookies()
        if i != begin and i % 200 == 0:
            for item in items:
                try:
                    collection.insert_one(item)
                except DuplicateKeyError:
                    print(item["_id"], "----This element already exists----")
                    collection.delete_one({"_id": item["_id"]})
                    collection.insert_one(item)
            items.clear()

        driver.get("https://www.kap.org.tr/tr/Bildirim/" + str(i))

        count = 0
        item = dict()
        while True:
            try:
                source_code = WebDriverWait(driver, 5).until(
                    expected_conditions.presence_of_element_located(
                        (By.ID, "disclosureContent"))).get_attribute("innerHTML")

                if len(items):
                    if source_code == items[-1]["source_code"]:
                        print("---", i)
                        raise TimeoutException()

                item["_id"] = i
                item["source_code"] = source_code
                items.append(item)
                print(i, int((i - begin) * 100 / (end - begin + 1)), "%")

                break
            except TimeoutException:
                print(i, "timeout")
                if count == 7:
                    break

                # if not isVPN:
                #     driver.quit()
                #     driver = webdriver.Chrome(chrome_options=chrome_options)
                #     isVPN = True
                #     VPNcount = 0

                driver.delete_all_cookies()
                driver.get("https://www.kap.org.tr/tr/Bildirim/" + str(i))
                count += 1
                continue
            except StaleElementReferenceException:
                continue

    driver.quit()
    print("Time1:", time.time() - ctime)

    for item in items:
        try:
            collection.insert_one(item)
        except DuplicateKeyError:
            print(item["_id"], "----This element already exists----")
            # pprint.pprint(item)
            collection.delete_one({"_id": item["_id"]})
            collection.insert_one(item)
    print("Getting source code is done!")


def get_source_code_thread(begin, end):
    """This method creates threads and uses them to call get_source_code method"""
    num_of_threads = 1
    length = end - begin + 1
    part_length = int(length / num_of_threads)

    print(part_length)
    threads = []
    for i in range(0, num_of_threads):
        print(begin + i * part_length)
        if i == num_of_threads - 1:
            print(end)
            threads.append(MyThread(i + 1, begin + i * part_length, end))
        else:
            threads.append(MyThread(i + 1, begin + i * part_length, begin + (i + 1) * part_length))
            print(begin + (i + 1) * part_length)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

if __name__ == '__main__':
    get_source_code_thread(620000, 620974)  # 402313 #581190 # 582500 - 583500 done
