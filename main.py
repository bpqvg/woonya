import vk_api
import requests
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api import VkUpload
import random
import os
from PIL import Image
import datetime
from bs4 import BeautifulSoup
from lxml import html
from lxml import etree
#import asyncio
#from proxybroker import Broker
#import gevent
#from itertools import cycle
#import aiohttp
#from threading import Thread
import threading
#from bs4 import BeautifulSoup as B
from time import sleep, time, ctime

headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0',
    }

fileDir = os.path.dirname(os.path.realpath('__file__'))

token = ''

vk_bot_session = vk_api.VkApi(token=token)
bot_api = vk_bot_session.get_api()
bot_upload = VkUpload(vk_bot_session)

bot_services = ['https://damn.ru']
is_proxy_available = False
available_proxy = []

def CheckAndAddProxy(proxy):
    global is_proxy_available
    global available_proxy
    try:
        #print('trying', proxy, ' : ', end='')
        #response = requests.get('https://damn.ru/?name={}&sex={}'.format(name, sex), proxies={'http': proxy, 'https': proxy}, headers=headers, stream=True, timeout=5)
        temp = ''.join((random.choice('qwertyuiopasdfghjklzzxcvbnm1234567890') for i in range(random.randint(3, 10))))
        response = requests.get('https://damn.ru/words?search={}'.format(temp), proxies={'http': proxy, 'https': proxy}, headers=headers, stream=True, timeout=1)
        #print(response.status_code)
        #print(response.content.decode('utf-8'))
        #message = response.status_code
        if response.status_code:
            is_proxy_available = True
            if proxy not in available_proxy:
                available_proxy.append(proxy)
                # print('ProxyUpdater | YES YES YES YES')
            if len(available_proxy) > 10:
                available_proxy.pop(0)
    except:
        #print('ProxyUpdater | Cant connect with this proxy, continue')
        pass

def ProxyUpdater():
    global is_proxy_available
    global available_proxy
    is_proxy_available = False
    while(True):
        proxies = GetProxies2()       
        #available_proxy = []
        for proxy in proxies:
            threading.Thread(target=CheckAndAddProxy, args=[proxy]).start()
            
        sleep(30)
        #print(available_proxy)


def VkBot_SendMessage(function, function_args, chat_id, message="", attachments=','):
    if function == None:
        bot_api.messages.send(chat_id=chat_id, random_id=random.getrandbits(32), message=message)  # message=random.choice(replies)  message=event.message.text
    else:
        if function_args == None:
            result = function()
        else:
            result = function(*function_args)
        bot_api.messages.send(chat_id=chat_id, random_id=random.getrandbits(32), message=result) 


def GetRandomQuote(language='ru'):
    send_data = {
        'method': 'getQuote',
        'format': 'json',
        'lang': language,
        'key': ""
    }
    # print('до.....')
    response = requests.get('http://api.forismatic.com/api/1.0/', send_data)
    json_response = response.json()
    # print('после.....')
    quote = json_response['quoteText']
    author = json_response['quoteAuthor']
    if author == '':
        author = 'Аноним'
    return '{}\n(c) {}'.format(quote, author)
    

def GetRandomCommentFromZaebaloRu():
    random_page_id = random.randint(1, 1649)
    getpage = requests.get('http://zaebalo.ru/?page=' + str(random_page_id))
    tree = html.fromstring(getpage.content)

    comment_texts = tree.xpath('//div[contains(@align, "left")]')
    comment_headers = tree.xpath('//div[contains(@class, "item")]//b[contains(text(), "#")]')

    random_comment_id = random.randint(0, len(comment_texts)-1)
    header = comment_headers[random_comment_id].text_content().lstrip().rstrip()
    text = comment_texts[random_comment_id].text_content().lstrip().rstrip()
    return '{}\n{}'.format(header, text)


def GetProxies():
    response = requests.get('https://free-proxy-list.net/', headers=headers, stream=True)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table',id='proxylisttable')
    list_tr = table.find_all('tr')
    list_td = [elem.find_all('td') for elem in list_tr]
    list_td = list(filter(None, list_td))
    list_ip = [elem[0].text for elem in list_td]
    list_ports = [elem[1].text for elem in list_td]
    list_proxies = [':'.join(elem) for elem in list(zip(list_ip, list_ports))]
    #print(list_proxies)
    return list_proxies

def GetProxies2():
    response = requests.get('http://spys.me/proxy.txt', headers=headers)
    #print((await response.content.read()).decode('utf-8').split('\n')[8::][1:-2])
    proxy = response.content.decode('utf-8').split('\n')[8::]  # [1].split(' ')[0]
    #print(proxy)
    proxies = []
    #print(proxy)
    for i in proxy[1:-2]:
        proxies.append(i.split(' ')[0])
    return proxies

def GetWellTriedProxies():
    if is_proxy_available == False:
        return False
    else:
        return True

def GetDamn(name, sex):
    # print(is_proxy_available)
    # print(available_proxy)
    message = 'Не смог оскорбить, утерял дар речи.'
    if is_proxy_available == False:
        return message
    #proxies = GetProxies()
    proxies = available_proxy
    for proxy in reversed(proxies):
        try:
            # print('trying', proxy, ' : ', end='')
            response = requests.get('https://damn.ru/?name={}&sex={}'.format(name, sex), proxies={'http': proxy, 'https': proxy}, headers=headers, stream=True, timeout=2)
            print(response.status_code)
            #print(response.content.decode('utf-8'))
            message = response.status_code
            break
        except:
            print('Def | GetDamn | Cant connect with this proxy, continue')
    return message

def GetCurrentDateAndTime():
    datetime = ctime()
    # datetime = str(datetime.datetime.now())
    return datetime

def main():
    while True:
        longpoll = VkBotLongPoll(vk_bot_session, '194888734')
        try:
            for event in longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    try:
                        if event.message.text[0] == '.':
                            message = event.message.text[1::]
                            if message == 'помощь':
                                help_bot = """помощь - текущая команда помощи\nоботе - информация о боте\nвремя - текущая дата и время по МСК\nцитата - случайная цитата\nзаебало - случайный комментарий с сервиса zaebalo.ru\nобосрать - обозвать кого-либо"""
                                #VkBot_SendMessage(function=None, function_args=None, chat_id=event.chat_id, message=help_bot)
                                threading.Thread(target=VkBot_SendMessage, args=[None, None, event.chat_id, help_bot, None]).start()
                            elif message == 'оботе':
                                about_bot = """Бот написан на Python.\nРазработчик: @sudo.rmrf\nРеппозиторий на github: github.com/sonerzerone/woonya\n~~~ Наслаждайтесь ~~~\nУзнать команды: .помощь"""
                                #VkBot_SendMessage(function=None, function_args=None, chat_id=event.chat_id, message=about_bot)
                                threading.Thread(target=VkBot_SendMessage, args=[None, None, event.chat_id, about_bot, None]).start()
                            elif message == 'время':
                                #VkBot_SendMessage(function=None, function_args=None, chat_id=event.chat_id, message=str(datetime.datetime.now()))
                                threading.Thread(target=VkBot_SendMessage, args=[GetCurrentDateAndTime, None, event.chat_id, None, None]).start()
                            elif message == 'цитата':
                                language = 'ru'
                                #VkBot_SendMessage(function=None, function_args=None, chat_id=event.chat_id, message=GetRandomQuote(language))
                                threading.Thread(target=VkBot_SendMessage, args=[GetRandomQuote, None, event.chat_id, None, None]).start()                            
                            elif message == 'gavno':
                                pass
                                # print('test')
                                # attachments = []
                                # pic = Image.open(os.path.join(fileDir, 'static/images/memes/Трансформаторная-будка.jpg'))
                                # print(pic)
                                # image = bot_upload.photo_messages(pic)  # [0]
                                # print(image)
                                # attachments.append('photo{}_{}'.format(image['owned_id'], image['id']))
                                #VkBot_SendMessage(event.chat_id, message="соси хуй", attachments=','.join(attachments))
                            elif message == 'заебало':
                                #VkBot_SendMessage(event.chat_id, GetRandomCommentFromZaebaloRu())
                                #VkBot_SendMessage(function=GetRandomCommentFromZaebaloRu, function_args=(None), chat_id=event.chat_id)
                                threading.Thread(target=VkBot_SendMessage, args=[GetRandomCommentFromZaebaloRu, None, event.chat_id, None, None]).start()
                            elif message == 'обосрать':
                                #VkBot_SendMessage(function=GetDamn, function_args=('name', 'm'), chat_id=event.chat_id)
                                threading.Thread(target=VkBot_SendMessage, args=[GetDamn, ('name', 'm'), event.chat_id, None, None]).start()
                                # function, function_args, chat_id, message, attachments


                    except:
                        continue




        except requests.exceptions.ReadTimeout as timeout:
            continue

if __name__ == "__main__":
    threading.Thread(target=ProxyUpdater, args=[]).start()
    main()


