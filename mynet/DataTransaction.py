# Programs that gather info from a website, find links and go other pages. Spiders as well
#Note that if you are using windows you cannot crawl js rendered pages using Pyqt5 or Pyqt4 s in the internet. Because there are some libraries are not supported
#by windows only on linux. You cannot even install pyqt 4 on windows.
#Only solution is to use Selenium


import time
from ToolBox import *
from selenium import webdriver
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import urllib.request
import requests


class DataTransaction:
    last_visited_company = 0
    visited_company_file_name=""
    json_file_name=""
    visited_update_company_file_name=""

    def __init__(self,system_target):
        self.system_target=system_target
        DataTransaction.visited_company_file_name='mynet_finans/visited_company_pages.txt'
        DataTransaction.json_file_name='mynet_finans/company_data.json'
        DataTransaction.visited_update_company_file_name='mynet_finans/updated_company_data.json'
        self.driver=None
        self._id=[]
        self.total_count=0
        self.company_names=[]
        self.company_abbreviations=[]
        self.main_page_data=[]
        self.user_names=[]
        self.user_comments=[]
        self.comment_dates = []
        self.comment_votes=[]
        self.data_fetching_dates=[]
        self.visited_company_pages=[]
        self.visited_update_company_pages=[]
        self.json_dictionary_list=[]
        self.updated_json_dictionary_list=[]
        self.all_updated_data=[]
        self.item_no=0
        create_data_files_for_transaction(system_target)
    @staticmethod
    def get_last_visited_company_index():
        inspect_company_main_pages=file_to_list(DataTransaction.visited_company_file_name)
        last_visited=0
        for  _ in range(0,len(inspect_company_main_pages)):
            last_visited+=1
        return last_visited
    #Initializing our selenium driver
    def get_item_no(self):
        return self.item_no
    @staticmethod
    def get_visited_company_file_name():
        return DataTransaction.visited_company_file_name

    @staticmethod
    def get_visited_update_company_file_name():
        return DataTransaction.visited_update_company_file_name
    @staticmethod
    def get_json_file_name():
        return  DataTransaction.json_file_name
    @staticmethod
    def init_driver():
        chromedriver = "browsers\\chromedriver.exe"
        os.environ["webdriver.chrome.driver"] = chromedriver
        driver = webdriver.Chrome(chromedriver)
        return driver

    #We filter out the unnecessary links belong to a company
    #Only main pages of companies
    def get_company_main_pages(self):
        company_main_pages=[]
        #Getting all the bist 30 companies
        inspect_companies=self.getCompanies()

        #Iterate through companies find the main page of particular company and add to list
        for i in range(0,len(inspect_companies)):
            main_page_of_company=self.get_main_page_of_company(inspect_companies[i])
            company_main_pages.append(main_page_of_company)

        return company_main_pages

    #We get all the pages belong to a BIST 30 company
    @staticmethod
    def getCompanies():
        bist_30_list = ['AKBANK', 'GARANTI BANKASI', 'BIM BIRLESIK MAGAZALAR', 'TUPRAS', 'TURKCELL',
                        'HACI OMER SABANCI HOLDING', 'TURKIYE IS BANKASI', 'EREGLI DEMIR VE CELIK FABRIKALARI',
                        'KOC HOLDING', 'HALKBANK',
                        'EMLAK KONUT GAYRIMENKUL YATIRIM ORTAK',
                        'TURK HAVA YOLLARI AO', 'ARCELIK', 'TURKIYE VAKIFLAR BANKASI', 'PETROKIMYA',
                        'YAPI VE KREDI BANKASI', 'TOFAS TURK OTOMOBIL FABRIKASI', 'TURKIYE SISE VE CAM FABRIKALARI',
                        'ASELSAN', 'ENKA SIRKETLER GRUBU', 'ULKER', 'TURK TELEKOM',
                        'TAV HAVALIMANLARI HOLDING', 'FORD OTOMOTIV SANAYI', 'SODA SANAYII', 'TEKFEN HOLDING',
                        'KARDEMIR KARABUK DEMIR CELIK SANAYI VE TICARET', 'MAVI', 'KOZA ALTIN ISLETMELERI',
                        'OTOKAR OTOMOTIV VE SAVUNMA SANAYII']


        return bist_30_list

    #Gets all pages belong to companies
    def get_all_company_pages(self):
        page_list = file_to_list(self.system_target + "/crawled_links.txt")
        return page_list

    #Get the main page of a particular company
    def get_main_page_of_company(self, company_name):
        inspect_pages = self.get_all_company_pages()
        company_abbr = self.getAbbreaviation(company_name)
        #We are lowering down the capital letters of abbreviation in order to search the company pages
        company_abbr_lower = company_abbr.lower()
        main_page_of_company = ""

        for i in range(0, len(inspect_pages)):
            if company_abbr_lower in inspect_pages[i]:
                main_page_of_company = inspect_pages[i]
                break
        return main_page_of_company

    def update_company_main_page(self,main_page_no,data,target_path):
        if main_page_no ==0:
            string_to_file(data,target_path)
            print('Data is written to file for the first time!')
        else:
            string_append_to_file(data,target_path)
            print('Data is appended to existing file!')

    def visitPages(self):
        # Bist companies to visit
        companies_to_visit = self.getCompanies()
        # Getting all main pages of companies
        main_page_of_companies = self.get_company_main_pages()
        # Getting the length of bist 30 main pages in our case it should be 30
        no_of_company_main_pages = len(main_page_of_companies)

        #We initialize our driver
        #Visit all 30 pages
        #Load all the comments belong to a particular BIST 30 company main page
        #Write them as a json file
        self.driver=self.init_driver()
        main_page_no =self.get_last_visited_company_index()
        #print(main_page_no)
        # Iterate through all links obtained by the spider
        while main_page_no < no_of_company_main_pages:
            company_to_visit=companies_to_visit[main_page_no]
            self.get_data_from_company_main_page(company_to_visit,main_page_of_companies[main_page_no],self.driver)
            visited_page=main_page_of_companies[main_page_no]
            print(visited_page)
            target_path = self.get_visited_company_file_name()
            self.visited_company_pages.append(visited_page)
            self.update_company_main_page(main_page_no,visited_page, target_path)
            # We write file the pages that we visited to keep track of where we left off
            main_page_no+=1
        json_record_path = self.get_json_file_name()
        # print(json_record_path)
        if fileExists(json_record_path):
            appendJson(self.json_dictionary_list, json_record_path)
            print(str(self.total_count)+ ' '+ 'items has been written as json format to an existing file: ' + json_record_path)
        else:
            writeJson(self.json_dictionary_list, json_record_path)
            print(str(self.total_count)+ ' '+ 'items has been written as json format for the first time to ' + json_record_path)
    def get_total_item_number(self):
        return self.total_count
    @staticmethod
    def closeAdvertisements(driver):
        # Close the advertisement windows for better tracking and possible interferes that can affect transaction
        try:
            # The banner button
            the_banner_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "skip-button")))
            the_banner_button = driver.find_element_by_id('skip-button')
            the_banner_button.click()

            # Do later button
            doLater_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "doLater")))
            doLater_button = driver.find_element_by_id('doLater')
            doLater_button.click()

            close_button_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "doLater")))
            close_button = driver.find_element_by_class_name('adm-close-btn-01')
            close_button.click()
        except:
            pass
        finally:
            print('Advertisements are destroyed!')

    def clickNextCommentButtonDynamic(self,driver):
    # Wait 3 seconds for comment section to exist
        the_comments_button = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "tipp-next-comment")))

        # Click comment button 300 times to go as deep as you can will be changed later
        #for i in range(0, 300):
        i=0
        while True:

            # Find the comment button
            the_comments_button = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "tipp-next-comment")))
            the_comments_button = driver.find_element_by_xpath('//*[@id="tipp-next-comment"]')

            time.sleep(0.5)
            # Scroll into comment button
            driver.execute_script("arguments[0].scrollIntoView();", the_comments_button)
            the_comments_button = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "tipp-next-comment")))
            recent_comment_button_height =the_comments_button.location['y']
            print(recent_comment_button_height)
            driver.execute_script('arguments[0].click();', the_comments_button)
            print('Clicked next comment button ' + str(i+1) + ' times')
            time.sleep(6)
            driver.execute_script("arguments[0].scrollIntoView();", the_comments_button)
            the_comments_button = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "tipp-next-comment")))

            current_comment_button_height=the_comments_button.location['y']
            print(current_comment_button_height)
            if recent_comment_button_height==current_comment_button_height:
                print('No more new data!')
                break
            else:
                i+=1
        time.sleep(1)
        self.extractValuableData(driver)

    def clickNextCommentButton(self,driver,company_to_visit,click_amount):

            # Wait 3 seconds for comment section to exist
            the_comments_button = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "tipp-next-comment")))
            for i in range(0, click_amount):
                # Find the comment button
                the_comments_button = driver.find_element_by_xpath('//*[@id="tipp-next-comment"]')
                time.sleep(0.5)
                # Scroll into comment button
                driver.execute_script("arguments[0].scrollIntoView();", the_comments_button)
                time.sleep(0.5)  # 918
                # Extracting data
                # Click to comment button
                driver.execute_script('arguments[0].click();', the_comments_button)
                print('Clicked next comment button ' + str((i + 1)) + ' times')

            if click_amount!=10:
                self.extractValuableData(driver)
            else:
                self.control_and_update(company_to_visit,driver)

    def get_recent_user_name(self):
        return self.user_names[len(self.user_names)-1]

    def get_recent_comment_date(self):
        return self.user_names[len(self.comment_dates)-1]

    def get_recent_comment_vote(self):
        return self.user_names[len(self.comment_votes)-1]

    def get_recent_user_comment(self):
        return self.user_names[len(self.user_comments)-1]

    def get_data_from_company_main_page(self,company_to_visit,main_page_of_company,driver):

            print('Started to extract data from: ' +company_to_visit)
            #click_amount=get_click_amount_for_company(company_to_visit)
            click_amount=150
            #Passing our driver main page url
            driver.get(main_page_of_company)

            #Closing the advertisement section
            #self.closeAdvertisements(driver)
            #Go to comment section to trigger javascript event
            driver.execute_script("window.scrollTo(0, (document.body.scrollHeight/2));")
            self.clickNextCommentButton(driver, company_to_visit, click_amount)
            time.sleep(1)
            driver.refresh()
            the_old_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tippani"]/div[2]/div/button[5]')))
            the_old_button = driver.find_element_by_xpath('//*[@id="tippani"]/div[2]/div/button[5]')
            time.sleep(1)
            driver.execute_script("arguments[0].scrollIntoView();", the_old_button)
            driver.execute_script('arguments[0].click();', the_old_button)
            print('Clicked old button!')
            self.clickNextCommentButton(driver,company_to_visit,click_amount)
            time.sleep(1)


        #Here we format the extracted data to json and get our json dictionary list
            self.format_to_json(company_to_visit)
            print(str(self.get_item_no())+' data found for '+company_to_visit)
        #print(self.json_dictionary_list)
        #We record our json data to file

    def extractValuableData(self,driver):
        try:
            time.sleep(1)
            # driver.execute_script("arguments[0].scrollIntoView();", the_old_button)
            # time.sleep(1)
            data=WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "tippani")))
            data = driver.find_element_by_xpath('//*[@id="tippani"]')
            #data=driver.find_element_by_xpath('//*[@id="yorum"]')
            html_code=data.get_attribute('outerHTML')
            soup = BeautifulSoup(html_code, "html.parser")

            #Find the list of usernames
            user_name_list = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "tipp-user-name")))
            user_name_list=soup.find_all("span",{"class":"tipp-user-name"})
            len_of_user_names=len(user_name_list)

            #Find the list of comment dates
            comment_date_list = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "tipp-com-time")))
            comment_date_list=soup.find_all("span",{"class":"tipp-com-time"})
            len_of_comment_dates=len(comment_date_list)

            #Find the list of comment votes
            comment_vote_list = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "tipp-vote")))
            comment_vote_list = soup.find_all("div", {"class": "tipp-vote"})
            len_of_comment_votes = len(comment_vote_list)
            #Find the list of all user comments
            user_comment_list = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "tipp-com-content")))
            driver.execute_script("arguments[0].scrollIntoView();", user_comment_list)
            #time.sleep(2)
            user_comment_list= soup.findAll("div", {"class": "tipp-com-content"})
            #time.sleep(1)
            len_of_user_comments = len(user_comment_list)
            print(len_of_user_comments)

            _data_ids = []
            _id_list=WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "tipp-com-content")))
            _id_list = soup.findAll("div", {"class": "tipp-com-content"})

            for item in _id_list:
                the_id = item.get('data-id')
                _data_ids.append(the_id)

            len_of_data_ids=len(_data_ids)
            #Let's fill our data arrays
            time.sleep(2)
            #Filling user names
            for i in range(0,len_of_user_names):
                self.user_names.append(user_name_list[i].string.strip())

            # Filling comment dates
            for i in range(0, len_of_comment_dates):
                self.comment_dates.append(comment_date_list[i].string.strip())

            # Filling comment votes
            for i in range(0, len_of_comment_votes):
                self.comment_votes.append(comment_vote_list[i].string.strip())
            #Filling user comments
            for i in range(0,len_of_user_comments):
                print(i)
                if user_comment_list[i].string is not None:
                    self.user_comments.append(user_comment_list[i].string.strip())

            #Filling data ids
            for i in range(0, len_of_data_ids):
                self._id.append(_data_ids[i])
        except:
            pass
        finally:
            print('Some transaction errors occurred due to server connection')

    #Gathers all data and format it into json
    def format_to_json(self,company_to_visit):
        company_name=company_to_visit
        company_abbrv=self.getAbbreaviation(company_name)
        user_names=self.get_user_names()
        user_comments=self.get_user_comments()
        comment_votes=self.get_comment_votes()
        comment_dates=self.get_comment_dates()
        _id=self.get_ids()
        print(len(user_names))
        print(len(user_comments))
        print(len(comment_votes))
        print(len(comment_dates))
        print(len(_id))
        fetching_date=time.strftime("%a")+ ' '+ time.strftime("%x")+ ' ' + time.strftime("%X")
        self.item_no=0
        for i in range(0,len(user_comments)):
            json_dict={"id":_id[i], "company_name":company_name,"company_abbreviation":company_abbrv,"user_name":user_names[i],"comment":user_comments[i],"vote":comment_votes[i],"comment_date":comment_dates[i],"fetching_date":fetching_date}
            self.json_dictionary_list.append(json_dict)
            self.item_no+=1
            self.total_count+=1


    @staticmethod
    def getAbbreaviation(company_name):
        if company_name == 'AKBANK':
            return 'AKBNK'
        elif company_name == 'GARANTI BANKASI':
            return 'GARAN'
        elif company_name == 'BIM BIRLESIK MAGAZALAR':
            return 'BIMAS'
        elif company_name == 'TUPRAS':
            return 'TUPRS'
        elif company_name == 'TURKCELL':
            return 'TCELL'
        elif company_name == 'HACI OMER SABANCI HOLDING':
            return 'SAHOL'
        elif company_name == 'TURKIYE IS BANKASI':
            return 'ISCTR'
        elif company_name == 'EREGLI DEMIR VE CELIK FABRIKALARI':
            return 'EREGL'
        elif company_name == 'KOC HOLDING':
            return 'KCHOL'
        elif company_name == 'HALKBANK':
            return 'HALKB'
        elif company_name == 'EMLAK KONUT GAYRIMENKUL YATIRIM ORTAK':
            return 'EKGYO'
        elif company_name == 'TURK HAVA YOLLARI AO':
            return 'THYAO'
        elif company_name == 'ARCELIK':
            return 'ARCLK'
        elif company_name == 'TURKIYE VAKIFLAR BANKASI':
            return 'VAKBN'
        elif company_name == 'PETROKIMYA':
            return 'PETKM'
        elif company_name == 'YAPI VE KREDI BANKASI':
            return 'YKBNK'
        elif company_name == 'TOFAS TURK OTOMOBIL FABRIKASI':
            return 'TOASO'
        elif company_name == 'TURKIYE SISE VE CAM FABRIKALARI':
            return 'SISE'
        elif company_name == 'ASELSAN':
            return 'ASELS'
        elif company_name == 'ENKA SIRKETLER GRUBU':
            return 'ENKA'
        elif company_name == 'ULKER':
            return 'ULKER'
        elif company_name == 'TURK TELEKOM':
            return 'TTKOM'
        elif company_name == 'TAV HAVALIMANLARI HOLDING':
            return 'TAVHL'
        elif company_name == 'FORD OTOMOTIV SANAYI':
            return 'FROTO'
        elif company_name == 'SODA SANAYII':
            return 'SODA'
        elif company_name == 'TEKFEN HOLDING':
            return 'TKFEN'
        elif company_name == 'KARDEMIR KARABUK DEMIR CELIK SANAYI VE TICARET':
            return 'KRDMD'
        elif company_name == 'MAVI':
            return 'MAVI'
        elif company_name == 'KOZA ALTIN ISLETMELERI':
            return 'KOZAL'
        elif company_name == 'OTOKAR OTOMOTIV VE SAVUNMA SANAYII':
            return 'OTKAR'
        else:
            print('Invalid value')
            return None

    def get_user_names(self):
        return self.user_names
    def get_comment_dates(self):
        return self.comment_dates
    def get_comment_votes(self):
        return self.comment_votes
    def get_user_comments(self):
        return self.user_comments
    def get_ids(self):
        return self._id

    def update_data(self):
        # Bist companies to visit
        companies_to_visit = self.getCompanies()
        # Getting all main pages of companies
        main_page_of_companies = self.get_company_main_pages()
        # Getting the length of bist 30 main pages in our case it should be 30
        no_of_company_main_pages = len(main_page_of_companies)

        # We initialize our driver
        # Visit all 30 pages
        # Load all the comments belong to a particular BIST 30 company main page
        # Write them as a json file
        self.driver = self.init_driver()
        main_page_no = 0
        # Iterate through all links obtained by the spider
        while main_page_no < no_of_company_main_pages:
            company_to_visit = companies_to_visit[main_page_no]
            self.gather_update_data(company_to_visit, main_page_of_companies[main_page_no], self.driver)
            visited_update_page = main_page_of_companies[main_page_no]
            self.visited_update_company_pages.append(visited_update_page)
            main_page_no += 1


        #target_path=self.get_visited_update_company_file_name()
        #self.update_company_main_page(self.visited_update_company_pages,target_path)

    def gather_update_data(self,company_to_visit,main_page_of_company,driver):
        print('Started to control update data from: ' + company_to_visit)
        click_amount = 10
        # Passing our driver main page url
        driver.get(main_page_of_company)

        # Closing the advertisement section
        #self.closeAdvertisements(driver)
        # Go to comment section to trigger javascript event
        driver.execute_script("window.scrollTo(0, (document.body.scrollHeight/2));")
        self.clickNextCommentButton(driver,company_to_visit,click_amount)
        time.sleep(1)

    def control_and_update(self,company_to_visit,driver):
        company_name = company_to_visit
        company_abbrv = self.getAbbreaviation(company_name)
        fetching_date = time.strftime("%a") + ' ' + time.strftime("%x") + ' ' + time.strftime("%X")
        users_to_control=[]
        votes_to_control=[]
        dates_to_control=[]
        comments_to_control=[]
        ids_to_control=[]

        control_json_dict_list = []

        data = driver.find_element_by_xpath('//*[@id="yorum"]')
        html_code = data.get_attribute('outerHTML')
        soup = BeautifulSoup(html_code, "html.parser")

        # Find the list of usernames
        user_name_list = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "tipp-user-name")))
        user_name_list = soup.find_all("span", {"class": "tipp-user-name"})
        len_of_user_names = len(user_name_list)

        # Find the list of comment dates
        comment_date_list = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CLASS_NAME, "tipp-com-time")))
        comment_date_list = soup.find_all("span", {"class": "tipp-com-time"})
        len_of_comment_dates = len(comment_date_list)

        # Find the list of comment votes
        comment_vote_list = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "tipp-vote")))
        comment_vote_list = soup.find_all("div", {"class": "tipp-vote"})
        len_of_comment_votes = len(comment_vote_list)

        # Find the list of all user comments
        user_comment_list = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CLASS_NAME, "tipp-com-content")))
        user_comment_list = soup.findAll("div", {"class": "tipp-com-content"})
        len_of_user_comments = len(user_comment_list)

        _data_ids = []
        _id_list = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "tipp-com-content")))
        _id_list = soup.findAll("div", {"class": "tipp-com-content"})

        for item in _id_list:
            the_id = item.get('data-id')
            _data_ids.append(the_id)

        len_of_data_ids = len(_data_ids)

        # Let's fill our data arrays
        time.sleep(1)
        # Filling user names to be controlled
        for i in range(0, len_of_user_names):
            users_to_control.append(user_name_list[i].string.strip())

        # Filling comment dates to be controlled
        for i in range(0, len_of_comment_dates):
            dates_to_control.append(comment_date_list[i].string.strip())

        # Filling comment votes to be controlled
        for i in range(0, len_of_comment_votes):
            votes_to_control.append(comment_vote_list[i].string.strip())

        # Filling user comments to be controlled
        for i in range(0, len_of_user_comments):
            comments_to_control.append(user_comment_list[i].string.strip())

        # Filling data ids to be controlled
        for i in range(0, len_of_data_ids):
            ids_to_control.append(_data_ids[i])
        current_data=jsonRead('mynet_finans/company_data.json')
        #Format control data
        for i in range(0, len(comments_to_control)):
            json_dict = {"id":ids_to_control[i], "company_name":company_name,"company_abbreviation":company_abbrv,"user_name":users_to_control[i],"comment":comments_to_control[i],"vote":votes_to_control[i],"comment_date":dates_to_control[i],"fetching_date":fetching_date}
            control_json_dict_list.append(json_dict)

        current_id_list=[]
        for i in range(0,len(current_data)):
            item=current_data[i]['id']
            current_id_list.append(item)
        updated=0

        updated_data=[]
        self.item_no=0
        for i in range(0,len(control_json_dict_list)):
            if control_json_dict_list[i]['id'] in current_id_list:
                continue
            else:
                self.all_updated_data.append(control_json_dict_list[i])
                updated_data.append(control_json_dict_list[i])
                self.item_no+=1
                updated=1

        if updated:
            print(str(self.get_item_no())+' update data found for '+company_name)
            print('Data write process has been initiated for: ' + company_name)
            appendJson(updated_data,self.get_json_file_name())
            if fileExists(self.get_visited_update_company_file_name()):
                appendJson(self.all_updated_data, self.get_visited_update_company_file_name())
            else:
                writeJson(self.all_updated_data, self.get_visited_update_company_file_name())
            #writeJson(updated_data,self.get_visited_update_company_file_name())
        else:
            print('No updates occurred in '+company_name)


    def generateID(company_name,company_abbreviation,user_name,comment,vote,comment_date):
        hash_str =(company_name + company_abbreviation + user_name + comment + vote + comment_date).replace(" ","")
        unique_id=''.join(str(ord(c)) for c in hash_str)
        return unique_id






