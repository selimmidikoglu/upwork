import pandas as pd
import time
import token_bucket
from urllib.request import urlopen, Request
import json, re
import urllib
from pymongo import MongoClient
import requests
from pymongo.errors import DuplicateKeyError
from datetime import datetime
import threading

class myThread (threading.Thread):

    def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
    def run(self):
       main_func(self.counter)

url_list = ['http://finanspano.mynet.com/index/index/?config[service]=finanspano&config[moderation]=1&config[item_alias]=6784eb9d038057a0821a7c905fd5f263&config[item_category]=Ym9yc2E=&config[item_title]=QUtCTks=&config[item_url]=aHR0cDovL2ZpbmFucy5teW5ldC5jb20vYm9yc2EvaGlzc2VsZXIvYWtibmstYWtiYW5rLw==&config[profile]=0&config[share_email]=1&config[share_fb]=1&config[share_tw]=1&config[profile_pattern]=Iw==&config[pagination]=1&config[pagination_pattern]=aHR0cDovL2ZpbmFuc3Bhbm8ubXluZXQuY29tL2NsaWVudC5waHA/cGFnZT17UEFHRX0=&config[comment_per_page]=5&config[page]=2&config[reply_count]=2&config[title]=yorumlar&config[hash]=5a8cadfa04b533f95ae83f0b9e530091&data[orderBy]=c.created&data[ordering]=desc&orderChanged=1',
            'http://finanspano.mynet.com/index/index/?config[service]=finanspano&config[moderation]=1&config[item_alias]=f89e64e27edc887b8ed3314fe8562eb2&config[item_category]=Ym9yc2E=&config[item_title]=R0FSQU4=&config[item_ ]=aHR0cDovL2ZpbmFucy5teW5ldC5jb20vYm9yc2EvaGlzc2VsZXIvZ2FyYW4tZ2FyYW50aS1iYW5rYXNpLw==&config[profile]=0&config[share_email]=1&config[share_fb]=1&config[share_tw]=1&config[profile_pattern]=Iw==&config[pagination]=1&config[pagination_pattern]=aHR0cDovL2ZpbmFuc3Bhbm8ubXluZXQuY29tL2NsaWVudC5waHA/cGFnZT17UEFHRX0=&config[comment_per_page]=5&config[page]=2&config[reply_count]=2&config[title]=yorumlar&config[hash]=e80cdd0e7a3dd9f4bbc393517386781c&data[orderBy]=c.created&data[ordering]=desc&orderChanged=1',
            'http://finanspano.mynet.com/index/index/?config[service]=finanspano&config[moderation]=1&config[item_alias]=a613786b1a34fdc6e3ac3a537cc6cffd&config[item_category]=Ym9yc2E=&config[item_title]=QklNQVM=&config[item_url]=aHR0cDovL2ZpbmFucy5teW5ldC5jb20vYm9yc2EvaGlzc2VsZXIvYmltYXMtYmltLW1hZ2F6YWxhci8=&config[profile]=0&config[share_email]=1&config[share_fb]=1&config[share_tw]=1&config[profile_pattern]=Iw==&config[pagination]=1&config[pagination_pattern]=aHR0cDovL2ZpbmFuc3Bhbm8ubXluZXQuY29tL2NsaWVudC5waHA/cGFnZT17UEFHRX0=&config[comment_per_page]=5&config[page]=2&config[reply_count]=2&config[title]=yorumlar&config[hash]=b565a503aa193cd5cccb3a9c6ec5429f&data[orderBy]=c.created&data[ordering]=desc&orderChanged=1',
            'http://finanspano.mynet.com/index/index/?config[service]=finanspano&config[moderation]=1&config[item_alias]=8dfea560d7e1cb1ff727a50f90f72557&config[item_category]=Ym9yc2E=&config[item_title]=VFVQUlM=&config[item_url]=aHR0cDovL2ZpbmFucy5teW5ldC5jb20vYm9yc2EvaGlzc2VsZXIvdHVwcnMtdHVwcmFzLw==&config[profile]=0&config[share_email]=1&config[share_fb]=1&config[share_tw]=1&config[profile_pattern]=Iw==&config[pagination]=1&config[pagination_pattern]=aHR0cDovL2ZpbmFuc3Bhbm8ubXluZXQuY29tL2NsaWVudC5waHA/cGFnZT17UEFHRX0=&config[comment_per_page]=5&config[page]=2&config[reply_count]=2&config[title]=yorumlar&config[hash]=a09e25e6ab14a9ea58e753187e3f838b&data[orderBy]=c.created&data[ordering]=desc&orderChanged=1',
            'http://finanspano.mynet.com/index/index/?config[service]=finanspano&config[moderation]=1&config[item_alias]=f11390105edc91b23380c80d32d0cbc5&config[item_category]=Ym9yc2E=&config[item_title]=VENFTEw=&config[item_url]=aHR0cDovL2ZpbmFucy5teW5ldC5jb20vYm9yc2EvaGlzc2VsZXIvdGNlbGwtdHVya2NlbGwv&config[profile]=0&config[share_email]=1&config[share_fb]=1&config[share_tw]=1&config[profile_pattern]=Iw==&config[pagination]=1&config[pagination_pattern]=aHR0cDovL2ZpbmFuc3Bhbm8ubXluZXQuY29tL2NsaWVudC5waHA/cGFnZT17UEFHRX0=&config[comment_per_page]=5&config[page]=2&config[reply_count]=2&config[title]=yorumlar&config[hash]=a401898304bba0923572a75c76f73060&data[orderBy]=c.created&data[ordering]=desc&orderChanged=1',
            'http://finanspano.mynet.com/index/index/?config[service]=finanspano&config[moderation]=1&config[item_alias]=a5e6a64ce1e21cc7b97639a280cebe28&config[item_category]=Ym9yc2E=&config[item_title]=U0FIT0w=&config[item_url]=aHR0cDovL2ZpbmFucy5teW5ldC5jb20vYm9yc2EvaGlzc2VsZXIvc2Fob2wtc2FiYW5jaS1ob2xkaW5nLw==&config[profile]=0&config[share_email]=1&config[share_fb]=1&config[share_tw]=1&config[profile_pattern]=Iw==&config[pagination]=1&config[pagination_pattern]=aHR0cDovL2ZpbmFuc3Bhbm8ubXluZXQuY29tL2NsaWVudC5waHA/cGFnZT17UEFHRX0=&config[comment_per_page]=5&config[page]=2&config[reply_count]=2&config[title]=yorumlar&config[hash]=31839176e01870e378e41a3d1500d62f&data[orderBy]=c.created&data[ordering]=desc&orderChanged=1',
            'http://finanspano.mynet.com/index/index/?config[service]=finanspano&config[moderation]=1&config[item_alias]=ff48255a916edc7e4e825778b6d1948a&config[item_category]=Ym9yc2E=&config[item_title]=SVNDVFI=&config[item_url]=aHR0cDovL2ZpbmFucy5teW5ldC5jb20vYm9yc2EvaGlzc2VsZXIvaXNjdHItaXMtYmFua2FzaS1jLw==&config[profile]=0&config[share_email]=1&config[share_fb]=1&config[share_tw]=1&config[profile_pattern]=Iw==&config[pagination]=1&config[pagination_pattern]=aHR0cDovL2ZpbmFuc3Bhbm8ubXluZXQuY29tL2NsaWVudC5waHA/cGFnZT17UEFHRX0=&config[comment_per_page]=5&config[page]=2&config[reply_count]=2&config[title]=yorumlar&config[hash]=a61331fc1d4882cf87f63ed248bc5dc8&data[orderBy]=c.created&data[ordering]=desc&orderChanged=1'
            'http://finanspano.mynet.com/index/index/?config[service]=finanspano&config[moderation]=1&config[item_alias]=2e68aac3f21251a76c61cfb2820cfb34&config[item_category]=Ym9yc2E=&config[item_title]=RVJFR0w=&config[item_url]=aHR0cDovL2ZpbmFucy5teW5ldC5jb20vYm9yc2EvaGlzc2VsZXIvZXJlZ2wtZXJlZ2xpLWRlbWlyLWNlbGlrLw==&config[profile]=0&config[share_email]=1&config[share_fb]=1&config[share_tw]=1&config[profile_pattern]=Iw==&config[pagination]=1&config[pagination_pattern]=aHR0cDovL2ZpbmFuc3Bhbm8ubXluZXQuY29tL2NsaWVudC5waHA/cGFnZT17UEFHRX0=&config[comment_per_page]=5&config[page]=2&config[reply_count]=2&config[title]=yorumlar&config[hash]=ada68e54404ccf90d9caa5aeda0c38aa&data[orderBy]=c.created&data[ordering]=desc&orderChanged=1',
            'http://finanspano.mynet.com/index/index/?config[service]=finanspano&config[moderation]=1&config[item_alias]=065481b395526e496bbfd48e94ec1959&config[item_category]=Ym9yc2E=&config[item_title]=S0NIT0w=&config[item_url]=aHR0cDovL2ZpbmFucy5teW5ldC5jb20vYm9yc2EvaGlzc2VsZXIva2Nob2wta29jLWhvbGRpbmcv&config[profile]=0&config[share_email]=1&config[share_fb]=1&config[share_tw]=1&config[profile_pattern]=Iw==&config[pagination]=1&config[pagination_pattern]=aHR0cDovL2ZpbmFuc3Bhbm8ubXluZXQuY29tL2NsaWVudC5waHA/cGFnZT17UEFHRX0=&config[comment_per_page]=5&config[page]=2&config[reply_count]=2&config[title]=yorumlar&config[hash]=1801ae24ea5cf28c6ccd762f31b6f08b&data[orderBy]=c.created&data[ordering]=desc&orderChanged=1',
            'http://finanspano.mynet.com/index/index/?config[service]=finanspano&config[moderation]=1&config[item_alias]=e03225fa5d385f1f77e1741f5a9e1f5a&config[item_category]=Ym9yc2E=&config[item_title]=SEFMS0I=&config[item_url]=aHR0cDovL2ZpbmFucy5teW5ldC5jb20vYm9yc2EvaGlzc2VsZXIvaGFsa2ItdC1oYWxrLWJhbmthc2kv&config[profile]=0&config[share_email]=1&config[share_fb]=1&config[share_tw]=1&config[profile_pattern]=Iw==&config[pagination]=1&config[pagination_pattern]=aHR0cDovL2ZpbmFuc3Bhbm8ubXluZXQuY29tL2NsaWVudC5waHA/cGFnZT17UEFHRX0=&config[comment_per_page]=5&config[page]=2&config[reply_count]=2&config[title]=yorumlar&config[hash]=8ec1a4f4a5ff03312dd852ce873e56b7&data[orderBy]=c.created&data[ordering]=desc&orderChanged=1',
            'http://finanspano.mynet.com/index/index/?config[service]=finanspano&config[moderation]=1&config[item_alias]=8673d2ce84a9bdb757aedca0b2b97d5b&config[item_category]=Ym9yc2E=&config[item_title]=RUtHWU8=&config[item_url]=aHR0cDovL2ZpbmFucy5teW5ldC5jb20vYm9yc2EvaGlzc2VsZXIvZWtneW8tZW1sYWsta29udXQtZ215by8=&config[profile]=0&config[share_email]=1&config[share_fb]=1&config[share_tw]=1&config[profile_pattern]=Iw==&config[pagination]=1&config[pagination_pattern]=aHR0cDovL2ZpbmFuc3Bhbm8ubXluZXQuY29tL2NsaWVudC5waHA/cGFnZT17UEFHRX0=&config[comment_per_page]=5&config[page]=2&config[reply_count]=2&config[title]=yorumlar&config[hash]=5f53ce918a989c8429863d8268fab478&data[orderBy]=c.created&data[ordering]=desc&orderChanged=1',
            'http://finanspano.mynet.com/index/index/?config[service]=finanspano&config[moderation]=1&config[item_alias]=5c2adcb6a08c0df67f86bedd58fb18db&config[item_category]=Ym9yc2E=&config[item_title]=VEhZQU8=&config[item_url]=aHR0cDovL2ZpbmFucy5teW5ldC5jb20vYm9yc2EvaGlzc2VsZXIvdGh5YW8tdHVyay1oYXZhLXlvbGxhcmkv&config[profile]=0&config[share_email]=1&config[share_fb]=1&config[share_tw]=1&config[profile_pattern]=Iw==&config[pagination]=1&config[pagination_pattern]=aHR0cDovL2ZpbmFuc3Bhbm8ubXluZXQuY29tL2NsaWVudC5waHA/cGFnZT17UEFHRX0=&config[comment_per_page]=5&config[page]=2&config[reply_count]=2&config[title]=yorumlar&config[hash]=72668e2082dd85870740e80f758873b7&data[orderBy]=c.created&data[ordering]=desc&orderChanged=1',
            'http://finanspano.mynet.com/index/index/?config[service]=finanspano&config[moderation]=1&config[item_alias]=03949762b2cd534b76e1df7deb398f5a&config[item_category]=Ym9yc2E=&config[item_title]=QVJDTEs=&config[item_url]=aHR0cDovL2ZpbmFucy5teW5ldC5jb20vYm9yc2EvaGlzc2VsZXIvYXJjbGstYXJjZWxpay8=&config[profile]=0&config[share_email]=1&config[share_fb]=1&config[share_tw]=1&config[profile_pattern]=Iw==&config[pagination]=1&config[pagination_pattern]=aHR0cDovL2ZpbmFuc3Bhbm8ubXluZXQuY29tL2NsaWVudC5waHA/cGFnZT17UEFHRX0=&config[comment_per_page]=5&config[page]=2&config[reply_count]=2&config[title]=yorumlar&config[hash]=11143dcebd79f842e88cf47ceac5e0c5&data[orderBy]=c.created&data[ordering]=desc&orderChanged=1',
            'http://finanspano.mynet.com/index/index/?config[service]=finanspano&config[moderation]=1&config[item_alias]=085d4a42237e5dc2c5db5a07f3b85b34&config[item_category]=Ym9yc2E=&config[item_title]=VkFLQk4=&config[item_url]=aHR0cDovL2ZpbmFucy5teW5ldC5jb20vYm9yc2EvaGlzc2VsZXIvdmFrYm4tdmFraWZsYXItYmFua2FzaS8=&config[profile]=0&config[share_email]=1&config[share_fb]=1&config[share_tw]=1&config[profile_pattern]=Iw==&config[pagination]=1&config[pagination_pattern]=aHR0cDovL2ZpbmFuc3Bhbm8ubXluZXQuY29tL2NsaWVudC5waHA/cGFnZT17UEFHRX0=&config[comment_per_page]=5&config[page]=2&config[reply_count]=2&config[title]=yorumlar&config[hash]=c46df9cd2da89857b4c73a88a10991a4&data[orderBy]=c.created&data[ordering]=desc&orderChanged=1',
            'http://finanspano.mynet.com/index/index/?config[service]=finanspano&config[moderation]=1&config[item_alias]=f0048e1a5e5aae6c3e1318a4200b5f9e&config[item_category]=Ym9yc2E=&config[item_title]=UEVUS00=&config[item_url]=aHR0cDovL2ZpbmFucy5teW5ldC5jb20vYm9yc2EvaGlzc2VsZXIvcGV0a20tcGV0a2ltLw==&config[profile]=0&config[share_email]=1&config[share_fb]=1&config[share_tw]=1&config[profile_pattern]=Iw==&config[pagination]=1&config[pagination_pattern]=aHR0cDovL2ZpbmFuc3Bhbm8ubXluZXQuY29tL2NsaWVudC5waHA/cGFnZT17UEFHRX0=&config[comment_per_page]=5&config[page]=2&config[reply_count]=2&config[title]=yorumlar&config[hash]=3d6564c09076235298e2af404d36b60d&data[orderBy]=c.created&data[ordering]=desc&orderChanged=1',
            'http://finanspano.mynet.com/index/index/?config[service]=finanspano&config[moderation]=1&config[item_alias]=fb8c33a882af88294664ae9998894892&config[item_category]=Ym9yc2E=&config[item_title]=WUtCTks=&config[item_url]=aHR0cDovL2ZpbmFucy5teW5ldC5jb20vYm9yc2EvaGlzc2VsZXIveWtibmsteWFwaS12ZS1rcmVkaS1iYW5rLw==&config[profile]=0&config[share_email]=1&config[share_fb]=1&config[share_tw]=1&config[profile_pattern]=Iw==&config[pagination]=1&config[pagination_pattern]=aHR0cDovL2ZpbmFuc3Bhbm8ubXluZXQuY29tL2NsaWVudC5waHA/cGFnZT17UEFHRX0=&config[comment_per_page]=5&config[page]=2&config[reply_count]=2&config[title]=yorumlar&config[hash]=8cee00e99e37844b9c90033c2e5198b0&data[orderBy]=c.created&data[ordering]=desc&orderChanged=1',
            'http://finanspano.mynet.com/index/index/?config[service]=finanspano&config[moderation]=1&config[item_alias]=9f6f14fa45041b3e47d23ea50568107b&config[item_category]=Ym9yc2E=&config[item_title]=VE9BU08=&config[item_url]=aHR0cDovL2ZpbmFucy5teW5ldC5jb20vYm9yc2EvaGlzc2VsZXIvdG9hc28tdG9mYXMtb3RvLWZhYi8=&config[profile]=0&config[share_email]=1&config[share_fb]=1&config[share_tw]=1&config[profile_pattern]=Iw==&config[pagination]=1&config[pagination_pattern]=aHR0cDovL2ZpbmFuc3Bhbm8ubXluZXQuY29tL2NsaWVudC5waHA/cGFnZT17UEFHRX0=&config[comment_per_page]=5&config[page]=2&config[reply_count]=2&config[title]=yorumlar&config[hash]=0cf48012351fece3a450ded17a1f235c&data[orderBy]=c.created&data[ordering]=desc&orderChanged=1',
            'http://finanspano.mynet.com/index/index/?config[service]=finanspano&config[moderation]=1&config[item_alias]=635ac23996de86acd047c110f796a920&config[item_category]=Ym9yc2E=&config[item_title]=U0lTRQ==&config[item_url]=aHR0cDovL2ZpbmFucy5teW5ldC5jb20vYm9yc2EvaGlzc2VsZXIvc2lzZS1zaXNlLWNhbS8=&config[profile]=0&config[share_email]=1&config[share_fb]=1&config[share_tw]=1&config[profile_pattern]=Iw==&config[pagination]=1&config[pagination_pattern]=aHR0cDovL2ZpbmFuc3Bhbm8ubXluZXQuY29tL2NsaWVudC5waHA/cGFnZT17UEFHRX0=&config[comment_per_page]=5&config[page]=2&config[reply_count]=2&config[title]=yorumlar&config[hash]=f30e6e99e5216549f07ac7fb75f6c23c&data[orderBy]=c.created&data[ordering]=desc&orderChanged=1',
            'http://finanspano.mynet.com/index/index/?config[service]=finanspano&config[moderation]=1&config[item_alias]=3c4991f10a63ec125b794f4983cb15f9&config[item_category]=Ym9yc2E=&config[item_title]=QVNFTFM=&config[item_url]=aHR0cDovL2ZpbmFucy5teW5ldC5jb20vYm9yc2EvaGlzc2VsZXIvYXNlbHMtYXNlbHNhbi8=&config[profile]=0&config[share_email]=1&config[share_fb]=1&config[share_tw]=1&config[profile_pattern]=Iw==&config[pagination]=1&config[pagination_pattern]=aHR0cDovL2ZpbmFuc3Bhbm8ubXluZXQuY29tL2NsaWVudC5waHA/cGFnZT17UEFHRX0=&config[comment_per_page]=5&config[page]=2&config[reply_count]=2&config[title]=yorumlar&config[hash]=184cf0c74eade9de6c9d6f19deb05c00&data[orderBy]=c.created&data[ordering]=desc&orderChanged=1',
            'http://finanspano.mynet.com/index/index/?config[service]=finanspano&config[moderation]=1&config[item_alias]=ee8410db4ba50bb1bc0aa84026c587e3&config[item_category]=Ym9yc2E=&config[item_title]=RU5LQUk=&config[item_url]=aHR0cDovL2ZpbmFucy5teW5ldC5jb20vYm9yc2EvaGlzc2VsZXIvZW5rYWktZW5rYS1pbnNhYXQv&config[profile]=0&config[share_email]=1&config[share_fb]=1&config[share_tw]=1&config[profile_pattern]=Iw==&config[pagination]=1&config[pagination_pattern]=aHR0cDovL2ZpbmFuc3Bhbm8ubXluZXQuY29tL2NsaWVudC5waHA/cGFnZT17UEFHRX0=&config[comment_per_page]=5&config[page]=2&config[reply_count]=2&config[title]=yorumlar&config[hash]=ba44e0d944e8f215ac4eef523d9815d7&data[orderBy]=c.created&data[ordering]=desc&orderChanged=1',
            'http://finanspano.mynet.com/index/index/?config[service]=finanspano&config[moderation]=1&config[item_alias]=149b24b3bec6922afe5300ca69e5d379&config[item_category]=Ym9yc2E=&config[item_title]=VUxLRVI=&config[item_url]=aHR0cDovL2ZpbmFucy5teW5ldC5jb20vYm9yc2EvaGlzc2VsZXIvdWxrZXItdWxrZXItYmlza3V2aS8=&config[profile]=0&config[share_email]=1&config[share_fb]=1&config[share_tw]=1&config[profile_pattern]=Iw==&config[pagination]=1&config[pagination_pattern]=aHR0cDovL2ZpbmFuc3Bhbm8ubXluZXQuY29tL2NsaWVudC5waHA/cGFnZT17UEFHRX0=&config[comment_per_page]=5&config[page]=2&config[reply_count]=2&config[title]=yorumlar&config[hash]=566292c16d750a068d5fddcdd171fcfd&data[orderBy]=c.created&data[ordering]=desc&orderChanged=1',
            'http://finanspano.mynet.com/index/index/?config[service]=finanspano&config[moderation]=1&config[item_alias]=bfc954510b288870c7184c5eaf186e10&config[item_category]=Ym9yc2E=&config[item_title]=VFRLT00=&config[item_url]=aHR0cDovL2ZpbmFucy5teW5ldC5jb20vYm9yc2EvaGlzc2VsZXIvdHRrb20tdHVyay10ZWxla29tLw==&config[profile]=0&config[share_email]=1&config[share_fb]=1&config[share_tw]=1&config[profile_pattern]=Iw==&config[pagination]=1&config[pagination_pattern]=aHR0cDovL2ZpbmFuc3Bhbm8ubXluZXQuY29tL2NsaWVudC5waHA/cGFnZT17UEFHRX0=&config[comment_per_page]=5&config[page]=2&config[reply_count]=2&config[title]=yorumlar&config[hash]=5a777c7e85ce6dddd28a52214af360b0&data[orderBy]=c.created&data[ordering]=desc&orderChanged=1',
            'http://finanspano.mynet.com/index/index/?config[service]=finanspano&config[moderation]=1&config[item_alias]=3c4ca28de3948c537ec76fa33c7eb5c9&config[item_category]=Ym9yc2E=&config[item_title]=VEFWSEw=&config[item_url]=aHR0cDovL2ZpbmFucy5teW5ldC5jb20vYm9yc2EvaGlzc2VsZXIvdGF2aGwtdGF2LWhhdmFsaW1hbmxhcmkv&config[profile]=0&config[share_email]=1&config[share_fb]=1&config[share_tw]=1&config[profile_pattern]=Iw==&config[pagination]=1&config[pagination_pattern]=aHR0cDovL2ZpbmFuc3Bhbm8ubXluZXQuY29tL2NsaWVudC5waHA/cGFnZT17UEFHRX0=&config[comment_per_page]=5&config[page]=2&config[reply_count]=2&config[title]=yorumlar&config[hash]=11edbbb5912b993d5bb0adac7bc4be4e&data[orderBy]=c.created&data[ordering]=desc&orderChanged=1',
            'http://finanspano.mynet.com/index/index/?config[service]=finanspano&config[moderation]=1&config[item_alias]=e1132ab4453e1c1136a6509f383c6f5a&config[item_category]=Ym9yc2E=&config[item_title]=RlJPVE8=&config[item_url]=aHR0cDovL2ZpbmFucy5teW5ldC5jb20vYm9yc2EvaGlzc2VsZXIvZnJvdG8tZm9yZC1vdG9zYW4v&config[profile]=0&config[share_email]=1&config[share_fb]=1&config[share_tw]=1&config[profile_pattern]=Iw==&config[pagination]=1&config[pagination_pattern]=aHR0cDovL2ZpbmFuc3Bhbm8ubXluZXQuY29tL2NsaWVudC5waHA/cGFnZT17UEFHRX0=&config[comment_per_page]=5&config[page]=2&config[reply_count]=2&config[title]=yorumlar&config[hash]=e9f47ed01fff4d1ad6d1f9c3b7f9b503&data[orderBy]=c.created&data[ordering]=desc&orderChanged=1',
            'http://finanspano.mynet.com/index/index/?config[service]=finanspano&config[moderation]=1&config[item_alias]=52cb5738c175fc8cf9a78dbc10f0231f&config[item_category]=Ym9yc2E=&config[item_title]=U09EQQ==&config[item_url]=aHR0cDovL2ZpbmFucy5teW5ldC5jb20vYm9yc2EvaGlzc2VsZXIvc29kYS1zb2RhLXNhbmF5aWkv&config[profile]=0&config[share_email]=1&config[share_fb]=1&config[share_tw]=1&config[profile_pattern]=Iw==&config[pagination]=1&config[pagination_pattern]=aHR0cDovL2ZpbmFuc3Bhbm8ubXluZXQuY29tL2NsaWVudC5waHA/cGFnZT17UEFHRX0=&config[comment_per_page]=5&config[page]=2&config[reply_count]=2&config[title]=yorumlar&config[hash]=078cc7ff11120d007456ede4723319ba&data[orderBy]=c.created&data[ordering]=desc&orderChanged=1',
            'http://finanspano.mynet.com/index/index/?config[service]=finanspano&config[moderation]=1&config[item_alias]=61a87a707e109be0a86e9c9debed45ce&config[item_category]=Ym9yc2E=&config[item_title]=VEtGRU4=&config[item_url]=aHR0cDovL2ZpbmFucy5teW5ldC5jb20vYm9yc2EvaGlzc2VsZXIvdGtmZW4tdGVrZmVuLWhvbGRpbmcv&config[profile]=0&config[share_email]=1&config[share_fb]=1&config[share_tw]=1&config[profile_pattern]=Iw==&config[pagination]=1&config[pagination_pattern]=aHR0cDovL2ZpbmFuc3Bhbm8ubXluZXQuY29tL2NsaWVudC5waHA/cGFnZT17UEFHRX0=&config[comment_per_page]=5&config[page]=2&config[reply_count]=2&config[title]=yorumlar&config[hash]=0ebdc8759b6b8fd400528194d6fcf7d4&data[orderBy]=c.created&data[ordering]=desc&orderChanged=1',
            'http://finanspano.mynet.com/index/index/?config[service]=finanspano&config[moderation]=1&config[item_alias]=50b4e51816d1b0e5f9a71240ea63450a&config[item_category]=Ym9yc2E=&config[item_title]=S1JETUQ=&config[item_url]=aHR0cDovL2ZpbmFucy5teW5ldC5jb20vYm9yc2EvaGlzc2VsZXIva3JkbWQta2FyZGVtaXItZC8=&config[profile]=0&config[share_email]=1&config[share_fb]=1&config[share_tw]=1&config[profile_pattern]=Iw==&config[pagination]=1&config[pagination_pattern]=aHR0cDovL2ZpbmFuc3Bhbm8ubXluZXQuY29tL2NsaWVudC5waHA/cGFnZT17UEFHRX0=&config[comment_per_page]=5&config[page]=2&config[reply_count]=2&config[title]=yorumlar&config[hash]=0cacdd4b972e8be5f3b975f9db4595c5&data[orderBy]=c.created&data[ordering]=desc&orderChanged=1',
            'http://finanspano.mynet.com/index/index/?config[service]=finanspano&config[moderation]=1&config[item_alias]=f908d50247309e3abdf1e418e196f7fa&config[item_category]=Ym9yc2E=&config[item_title]=TUFWSQ==&config[item_url]=aHR0cDovL2ZpbmFucy5teW5ldC5jb20vYm9yc2EvaGlzc2VsZXIvbWF2aS1tYXZpLWdpeWltLw==&config[profile]=0&config[share_email]=1&config[share_fb]=1&config[share_tw]=1&config[profile_pattern]=Iw==&config[pagination]=1&config[pagination_pattern]=aHR0cDovL2ZpbmFuc3Bhbm8ubXluZXQuY29tL2NsaWVudC5waHA/cGFnZT17UEFHRX0=&config[comment_per_page]=5&config[page]=2&config[reply_count]=2&config[title]=yorumlar&config[hash]=f5dca0bd57cfd8711b3db59445b01319&data[orderBy]=c.created&data[ordering]=desc&orderChanged=1',
            'http://finanspano.mynet.com/index/index/?config[service]=finanspano&config[moderation]=1&config[item_alias]=d65969718c662731fefeff9acd7427a8&config[item_category]=Ym9yc2E=&config[item_title]=S09aQUw=&config[item_url]=aHR0cDovL2ZpbmFucy5teW5ldC5jb20vYm9yc2EvaGlzc2VsZXIva296YWwta296YS1hbHRpbi8=&config[profile]=0&config[share_email]=1&config[share_fb]=1&config[share_tw]=1&config[profile_pattern]=Iw==&config[pagination]=1&config[pagination_pattern]=aHR0cDovL2ZpbmFuc3Bhbm8ubXluZXQuY29tL2NsaWVudC5waHA/cGFnZT17UEFHRX0=&config[comment_per_page]=5&config[page]=2&config[reply_count]=2&config[title]=yorumlar&config[hash]=eb54744fba333c2c0a84a3c38b1964b6&data[orderBy]=c.created&data[ordering]=desc&orderChanged=1',
            'http://finanspano.mynet.com/index/index/?config[service]=finanspano&config[moderation]=1&config[item_alias]=07efbe8b6e5441c330a022b5bacf1a62&config[item_category]=Ym9yc2E=&config[item_title]=RE9IT0w=&config[item_url]=aHR0cDovL2ZpbmFucy5teW5ldC5jb20vYm9yc2EvaGlzc2VsZXIvZG9ob2wtZG9nYW4taG9sZGluZy8=&config[profile]=0&config[share_email]=1&config[share_fb]=1&config[share_tw]=1&config[profile_pattern]=Iw==&config[pagination]=1&config[pagination_pattern]=aHR0cDovL2ZpbmFuc3Bhbm8ubXluZXQuY29tL2NsaWVudC5waHA/cGFnZT17UEFHRX0=&config[comment_per_page]=5&config[page]=2&config[reply_count]=2&config[title]=yorumlar&config[hash]=23fb416db7aa2bc216765d4173f82c9f&data[orderBy]=c.created&data[ordering]=desc&orderChanged=1']


company_list = ['AKBNK', 'GARAN', 'BIMAS', 'TUPRS', 'TCELL', 'SAHOL', 'ISCTR', 'EREGL', 'KCHOL',
                'HALKB', 'EKGYO','THYAO', 'ARCLK', 'VAKBN', 'PETKM', 'YKBNK',
                'TOASO', 'SISE', 'ASELS', 'ENKAI', 'ULKER', 'TTKOM', 'TAVHL',
                'FROTO', 'SODA', 'TKFEN', 'KRDMD', 'MAVI', 'KOZAL','DOHOL']


def url_to_dict(url):
    url_again= url

    hdr = {
        'User-Agent': 'Chrome/60.0.3112.101 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Safari/537.11 Mozilla/55.0.2',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}


    data2= urllib.request.Request(url,headers= hdr)
    # proxy_support = urllib.request.ProxyHandler({"http": "http://61.233.25.166:80"})
    # opener = urllib2.build_opener(proxy_support)
    # urllib2.install_opener(opener)



    #data = urllib.request.urlopen(url).read().decode('utf-8')
    data = requests.get(url)
    json_type_string = re.findall('({.*})', data.text)[0]
    json_data = json.loads(json_type_string)
    total_page = json_data['data']['totalPage']
    return json_data,total_page






def get_data(json_data):
    data = json_data[0]['data']['items']
    parsed_data= [[],[],[],[],[]]
    print()
    print(type(parsed_data))
    for x in range(len(data)):
        #print(parsed_data)
        parsed_data[x].append(data[x]['id'])
        parsed_data[x].append(data[x]['user'])
        parsed_data[x].append(data[x]['created'])
        parsed_data[x].append(data[x]['clike'])
        parsed_data[x].append(data[x]['cdislike'])
        parsed_data[x].append(data[x]['child'])
        parsed_data[x].append(data[x]['comment'])

        print(parsed_data[x][5])
        a = int(parsed_data[x][5])
        if a != 0:
            try:
                for y in range(len(data[x]['children'])):
                    new_id = str(data[x]['children']).split("'")[1]
                    parsed_data[x].append(data[x]['children'][new_id]['id'])
                    parsed_data[x].append(data[x]['children'][new_id]['user'])
                    parsed_data[x].append(data[x]['children'][new_id]['created'])
                    parsed_data[x].append(data[x]['children'][new_id]['clike'])
                    parsed_data[x].append(data[x]['children'][new_id]['cdislike'])
                    parsed_data[x].append(data[x]['children'][new_id]['comment'])
            except Exception:
                print ("do not have children data ")
    return parsed_data


def add_to_mongo(data,company_name):
    client= MongoClient()
    db = client['web']
    collection = db['mynet2']
    for x in range(len(data)):
        if data[x][5] == 0:
            try:
                db.mynet2.insert_one(
                    {'_id': data[x][0], 'Username' : data[x][1], 'Date' : data[x][2],
                     'Liked' : data[x][3], 'Disliked' : data[x][4], 'Comment' : data[x][6], 'Company_Name' : company_name})
            except DuplicateKeyError:
                print("Duplicate value cannot insert")
                pass
        else:
            try:
                db.mynet2.insert_one(
                    {'_id': data[x][0], 'Username': data[x][1], 'Date': data[x][2],
                     'Liked': data[x][3], 'Disliked': data[x][4], 'Comment': data[x][6], 'Children': data[x][7:],
                     'Company_Name': company_name})
            except DuplicateKeyError:
                print("Duplicate value cannot insert")
                pass


def count_comment():
    count_com = 0
    for x in url_list:
        total = url_to_dict(x)
        count_com = count_com + total[1]
        print(total[1])
    print(count_com*5)


def main_func(counter):
    # rate = 1
    # capacity = 100
    # token_bucket.Limiter(rate, capacity, token_bucket.MemoryStorage())
    # bucket = TokenBucket(80, 0.5)
    # proxy_support = urllib.request.ProxyHandler({"http": "http://208.83.106.105:9999"})
    # opener = urllib.request.build_opener(proxy_support)
    # urllib.request.install_opener(opener)
    for x in range(len(url_list)):
        url=url_list[x]
        company_name=company_list[x]
        total=url_to_dict(url)
        total_page=total[1]
        for y in range(int(total_page/10)+1):
            index = url.find('config[page]=')
            index2 = url.find('&config[reply')
            k = y*10
            url = url[:index+13] + str(counter+k) + url[index2:]
            print(url)
            data = url_to_dict(url)
            parsed_data = get_data(data)
            add_to_mongo(parsed_data,company_name)


def str_to_datetime():
    client = MongoClient()
    db = client['web']
    df = pd.DataFrame(list(db.mynet2.find({})))
    numbers=0
    for x in range(len(df['Date'])):
        numbers= numbers + 1
        new_date = datetime.strptime(df['Date'][x], '%Y-%m-%d %H:%M:%S')
        db.mynet2.update({"_id": df['_id'][x]},
        {
            "$set": {
            "Date": new_date
            }
        })
        print(str(df['Date'][x]) + "      " + str(numbers))


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

def update():

    for x in range(len(url_list)):
        url=url_list[x]
        company_name= company_list[x]
        print("x is : " + str(x))
        print(url)
        url_to_dict(url)

        for y in range(1,5):
            index = url.find('config[page]=')
            index2 = url.find('&config[reply')
            url = url[:index + 13] + str(y) + url[index2:]
            print(url)
            time.sleep(100)
            data = url_to_dict(url)
            parsed_data = get_data(data)
            add_to_mongo(parsed_data,company_name)

#update()
