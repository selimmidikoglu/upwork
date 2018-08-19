from pymongo import MongoClient
import mechanicalsoup
import os
import pandas as pd
from datetime import datetime,timedelta

from pymongo.errors import DuplicateKeyError
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

url = "http://www.fixelborsa.com/sembolDetay.html#"
client = MongoClient()
db = client['web']
collection = db['fixel']

br = mechanicalsoup.Browser()
br.addheaders = [('User-agent', 'PhantomJS')]
browser = webdriver.PhantomJS(executable_path='/Users/nihadazimli/PycharmProjects/quantsol-text/web-crawler/phantomjs')

timeout = 5
TYK = ['']
SonDurum = ['']
Tahmin = ['']
Tarih = ['']
Degerlendirme = ['']
addrs = ['']
_id = ['']


def get_data(browser, url):
    browser.get(url)
    elem = browser.find_element_by_id('predictionList')
    count = 0
    while count < 3:
        try:
            element_present = EC.presence_of_element_located((By.CLASS_NAME, 'up'))
            element_present2 = EC.presence_of_element_located((By.CLASS_NAME, 'down'))
            WebDriverWait(browser, timeout).until(element_present or element_present2)
            break
        except Exception:
            if count != 3:
                count += 1
            else:
                count = 0
                browser.refresh()
            print("Timed out waiting for page to load")

    address = browser.find_element_by_xpath('//*[@id="predictionList"]')


    return address


def make_data_dict(address):
    count = 0
    html = address.get_attribute('innerHTML').split('<')

    for x in html:
        if x[:6] == 'div id':
            newID = x.split(' ')[1].split('="')[1][:-2]
            _id.append(newID)
        elif x[:9] == 'div class':
            newID = x.split(' ')[2].split('="')[1][:-2]
            _id.append(newID)
    for x in html:
        if x[:3] == 'img':
            addrs.append(os.path.basename(x[9:]).split('.')[0])

    for x in address.text.split('\n'):
        if count == 0:
            count += 1
            if x != "İlgili tahmin bulunamadı.":
                TYK.append(x)
        elif count == 1:
            count += 1
        elif count == 2:
            count += 1
            SonDurum.append(x)
        elif count == 3:
            count += 1
        elif count == 4:
            count += 1
            Tahmin.append(x)
        elif count == 5:
            count += 1
            if (x == '-'):
                x = 'nötr'
            Degerlendirme.append(x)
        elif count == 6:

            count += 1
            count = 0
            x = x.split(',')[1]
            a = x.split(' ')

            if (a[2] == 'Ocak'):
                a[2] = '01'
            elif (a[2] == 'Şubat'):
                a[2] = '02'
            elif (a[2] == 'Mart'):
                a[2] = '03'
            elif (a[2] == 'Nisan'):
                a[2] = '04'
            elif (a[2] == 'Mayıs'):
                a[2] = '05'
            elif (a[2] == 'Haziran'):
                a[2] = '06'
            elif (a[2] == 'Temmuz'):
                a[2] = '07'
            elif (a[2] == 'Ağustos'):
                a[2] = '08'
            elif (a[2] == 'Eylül'):
                a[2] = '09'
            elif (a[2] == 'Ekim'):
                a[2] = '10'
            elif (a[2] == 'Kasım'):
                a[2] = '11'
            elif (a[2] == 'Aralık'):
                a[2] = '12'
            x = a[1] + " " + a[2] + " " + a[3] + " " + a[4]
            date = datetime.strptime(x, "%d %m %Y %H:%M")
            Tarih.append(date)
        else:
            count = 0

def append_to_data_frame():
    df = pd.DataFrame(columns=['_id', 'Tahmin Yapan Kurum', 'Tahmin yapilan kurum', 'Son durumu',
                               'Gelecek Tahmin', 'Değerlendirme'])

    se = pd.Series(_id[1:])
    df['_id'] = se

    se = pd.Series(addrs[1:])
    df['Tahmin Yapan Kurum'] = se

    se = pd.Series(TYK[1:])
    df['Tahmin yapilan kurum'] = se

    se = pd.Series(SonDurum[1:])
    df['Son durumu'] = se

    se = pd.Series(Tahmin[1:])
    df['Gelecek Tahmin'] = se

    se = pd.Series(Degerlendirme[1:])
    df['Değerlendirme'] = se

    se = pd.Series(Tarih[1:])
    df['Tahmin Tarihi'] = se
    df = df.set_index(pd.DatetimeIndex(df['Tahmin Tarihi']))
    df.sort_values(by='Tahmin Tarihi')

    header = ['Identification','Tahmin Yapan Kurum', 'Tahmin yapilan kurum', 'Son durumu', 'Gelecek Tahmin',
              'Değerlendirme']

    outJson = df.to_json(orient='records',force_ascii=False)

    open('myJson.js','w',encoding='utf-8').write(outJson)
    exception_coun=0
    for x in range(len(df)):
        try:
            db.collection.insert_one({'_id':df['_id'][x],'Son durumu':df['Son durumu'][x],'Gelecek Tahmin':df['Gelecek Tahmin'][x],'Tahmin Yapan Kurum':df['Tahmin Yapan Kurum'][x],
                              'Tahmin Tarihi': df['Tahmin Tarihi'][x],'Değerlendirme':df['Değerlendirme'][x],'Tahmin yapilan kurum':df['Tahmin yapilan kurum'][x]})
        except DuplicateKeyError:
            print("Duplicate value cannot insert")
            exception_coun+=1
            pass
    print ("Exception count is : "+str(exception_coun) )
    return df


def update_data():
    print("asas")

    df = pd.DataFrame(list(db.collection.find()))

    keywords = ['AKBNK', 'GARAN', 'BIMAS', 'TUPRS', 'TCELL', 'SAHOL', 'ISCTR', 'EREGL', 'KCHOL',
                'HALKB', 'EKGYO', 'THYAO', 'ARCLK', 'VAKBN', 'PETKM', 'YKBNK',
                'TOASO', 'SISE', 'ASELS', 'ENKAI', 'ULKER', 'TTKOM', 'TAVHL',
                'FROTO', 'SODA', 'TKFEN', 'KRDMD', 'MAVI', 'KOZAL']
    num=0
    browser = webdriver.PhantomJS(executable_path='/Users/nihadazimli/PycharmProjects/quantsol-text/web-crawler/phantomjs')
    for x in range(5):
        for i in keywords[num:num+6]:
            i += ".E.BIST"
            print(i)
            urlnew = url + i
            print(urlnew)
            address = get_data(browser, urlnew)
            html = address.get_attribute('innerHTML').split('<')
            new_id=['']
            for x in html:
                if x[:6] == 'div id':
                    newID = x.split(' ')[1].split('="')[1][:-2]
                    new_id.append(newID)
                elif x[:9] == 'div class':
                    newID = x.split(' ')[2].split('="')[1][:-2]
                    new_id.append(newID)
            if new_id[0] == df['_id'][0]:
                print("everyting is up-to-date because new_id = " +new_id[0]+
                      " is equal to " + df['_id'][0] )
            else:
                try:
                    print("new id :" + new_id[0])
                    print("old id :" + df['_id'][0])
                    make_data_dict(address)
                    for x in _id:
                        print('a')
                except DuplicateKeyError:
                    print("Duplicate value cannot insert")
                    pass


        num+=6
        browser.close()
        br = mechanicalsoup.Browser()
        br.addheaders = [('User-agent', 'PhantomJS')]
        browser = webdriver.PhantomJS(executable_path='/Users/nihadazimli/PycharmProjects/quantsol-text/web-crawler/phantomjs')


def retrieve_data(browser):
    keywords = ['AKBNK', 'GARAN', 'BIMAS', 'TUPRS', 'TCELL', 'SAHOL', 'ISCTR', 'EREGL', 'KCHOL',
                'HALKB', 'EKGYO','THYAO', 'ARCLK', 'VAKBN', 'PETKM', 'YKBNK',
                'TOASO', 'SISE', 'ASELS', 'ENKAI', 'ULKER', 'TTKOM', 'TAVHL',
                'FROTO', 'SODA', 'TKFEN', 'KRDMD', 'MAVI', 'KOZAL']
    num=0
    for x in range(5):
        for i in keywords[num:num+6]:
            i += ".E.BIST"
            print(i)
            urlnew = url + i
            print(urlnew)
            make_data_dict(get_data(browser, urlnew))
        num+=6
        browser.close()
        br = mechanicalsoup.Browser()
        br.addheaders = [('User-agent', 'PhantomJS')]
        browser = webdriver.PhantomJS(executable_path='/Users/nihadazimli/PycharmProjects/quantsol-text/web-crawler/phantomjs')
    print(append_to_data_frame())


def mainz():
    retrieve_data(browser= browser)

