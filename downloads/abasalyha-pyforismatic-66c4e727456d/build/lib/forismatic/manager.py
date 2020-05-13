# -*- coding: UTF-8 -*-

import urllib
import json
from datetime import datetime


class Quote(object):
    """
    Quote object, forming from given data
    
    """

    def __init__(self, data):
        self.__quote = data['quoteText']
        self.__author = data['quoteAuthor']
        self.__sender_name = data['senderName']
        self.__sender_link = data['senderLink']
        self.__datetime = datetime.now()

    @property
    def quote(self):
        return self.__quote

    @property
    def author(self):
        return self.__author

    @property
    def sender_name(self):
        return self.__sender_name

    @property
    def sender_link(self):
        return self.__sender_link

    @property
    def __recieved_datetime(self):
        return self.__datetime


class Forismatic(object):
    """
    Manager for getting quotes using Forismatic API (default = 1.0)
    Supports POST & GET methods, russian & english quotes
    
    """

    def __init__(self, method="POST", api_url='http://api.forismatic.com/api/1.0/'):

        if method not in ["POST", "GET"]:
            raise Exception("Unknown method %s" % method)
        self.method = method
        self.api_url = api_url


    def get_quote(self, lang='en', key=None):
        '''
        Method for retrieve quote
        
        '''

        str_key = str(key)

        # Validation of input data
        if key:
            if len(str_key) > 6:
                raise Exception('Key max length is 6')

        if lang not in ['en', 'ru']:
            raise Exception('Unknown language: %s' % lang)

        send_data = {
        'method': 'getQuote',
        'format': 'json',
        'lang': lang,
        'key': str_key if key else ""
        }

        if self.method == "POST":
            response = urllib.urlopen(self.api_url, data=urllib.urlencode(send_data))
        else:
            response = urllib.urlopen("%s?%s" % (self.api_url, urllib.urlencode(send_data)))

        if response.getcode() == 200:

            # Decoding JSON and fill Quote, if HTTP responce is OK
            retrieved_data = json.load(response)
            return Quote(data=retrieved_data)
        else:
            return None
