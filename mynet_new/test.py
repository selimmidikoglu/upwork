import requests
import json
import re
import urllib

url = 'http://finanspano.mynet.com/index/index/?config[service]=finanspano&config[moderation]=1&config[item_alias]=f89e64e27edc887b8ed3314fe8562eb2&config[item_category]=Ym9yc2E=&config[item_title]=R0FSQU4=&config[item_ ]=aHR0cDovL2ZpbmFucy5teW5ldC5jb20vYm9yc2EvaGlzc2VsZXIvZ2FyYW4tZ2FyYW50aS1iYW5rYXNpLw==&config[profile]=0&config[share_email]=1&config[share_fb]=1&config[share_tw]=1&config[profile_pattern]=Iw==&config[pagination]=1&config[pagination_pattern]=aHR0cDovL2ZpbmFuc3Bhbm8ubXluZXQuY29tL2NsaWVudC5waHA/cGFnZT17UEFHRX0=&config[comment_per_page]=5&config[page]=2&config[reply_count]=2&config[title]=yorumlar&config[hash]=e80cdd0e7a3dd9f4bbc393517386781c&data[orderBy]=c.created&data[ordering]=desc&orderChanged=1'

data = requests.get('http://finanspano.mynet.com/index/index/?config[service]=finanspano&config[moderation]=1&config[item_alias]=f89e64e27edc887b8ed3314fe8562eb2&config[item_category]=Ym9yc2E=&config[item_title]=R0FSQU4=&config[item_ ]=aHR0cDovL2ZpbmFucy5teW5ldC5jb20vYm9yc2EvaGlzc2VsZXIvZ2FyYW4tZ2FyYW50aS1iYW5rYXNpLw==&config[profile]=0&config[share_email]=1&config[share_fb]=1&config[share_tw]=1&config[profile_pattern]=Iw==&config[pagination]=1&config[pagination_pattern]=aHR0cDovL2ZpbmFuc3Bhbm8ubXluZXQuY29tL2NsaWVudC5waHA/cGFnZT17UEFHRX0=&config[comment_per_page]=5&config[page]=2&config[reply_count]=2&config[title]=yorumlar&config[hash]=e80cdd0e7a3dd9f4bbc393517386781c&data[orderBy]=c.created&data[ordering]=desc&orderChanged=1')
json_type_string = re.findall('({.*})', data.text)[0]
json_data = json.loads(json_type_string)

print(json_data)
print('\n\n\n')
data = urllib.request.urlopen(url).read().decode('utf-8')
json_type_string = re.findall('({.*})', data)[0]
json_data = json.loads(json_type_string)
total_page = json_data['data']['totalPage']
print(json_data)