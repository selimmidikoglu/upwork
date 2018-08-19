from pymongo import MongoClient
from datetime import datetime
import json
from pymongo.errors import DuplicateKeyError
import pandas as pd
import numpy as np
from datetime import datetime

client = MongoClient()
db = client['web']
collection = db['counter']

x = str(datetime.today().day) + " " + str(datetime.today().month) + " " + str(datetime.today().year)
today = datetime.strptime(x, "%d %m %Y")

df = pd.DataFrame(list(db.mynet.find({}))).sort_values("Date")
date_count=0
dates=[]

old_date=datetime.now()
for x in df['Date']:
    if old_date.day != x.day or old_date.month != x.month:
        app_str= str(x.day) + "-" + str(x.month) + "-" + str(x.year)
        app_date = datetime.strptime(app_str, "%d-%m-%Y")
        dates.append(app_date)
        date_count += 1
    old_date = x
print("date count is : " + str(date_count))

key = ['AKBNK', 'GARAN', 'BIMAS', 'TUPRS', 'TCELL', 'SAHOL', 'ISCTR', 'EREGL', 'KCHOL',
        'HALKB', 'EKGYO', 'THYAO', 'ARCLK', 'VAKBN', 'PETKIM', 'YKBNK',
        'TOASO', 'SISE', 'ASELS', 'ENKAI', 'ULKER', 'TTKOM', 'TAVHL',
        'FROTO', 'SODA', 'TKFEN', 'KRDMD', 'MAVI', 'KOZAL', 'DOHOL']

keyNum=np.zeros((date_count,30), dtype='int64')
counter = 0

for z in dates:
    start = datetime(z.year, z.month, z.day, 00, 00, 00)
    end = datetime(z.year, z.month, z.day, 23, 59, 59)
    df_one = pd.DataFrame(list(db.mynet.find({'Date':{'$lt': end, '$gt': start}})))
    print("it is df one ahahahahahhaha:")
    print(df_one)
    for x in key:
        for y in df_one['Company_Name']:

            if x == y:
                print(x)
                keyNum[counter][key.index(x)] += 1
    counter += 1


df_add = pd.DataFrame(columns=['Kurum ismi', 'Yorum sayisi', 'Date'])

counter=0
for counter in range(len(dates) ):
    for x in range(len (key)):
            db.counter.insert_one({'Kurum ismi' :key[x] , 'Yorum sayisi' : keyNum[counter][x].item(), 'Date': dates[counter]})

print(df_add)
