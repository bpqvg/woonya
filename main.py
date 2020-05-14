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
from time import sleep, time

headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0',
    }

fileDir = os.path.dirname(os.path.realpath('__file__'))

token = 'b884b8a3e2557fc59feca21ac1c0002f4f542ae41672b02659b472573027f35466e5081cac81c712e9993'

vk_bot_session = vk_api.VkApi(token=token)
bot_api = vk_bot_session.get_api()
bot_upload = VkUpload(vk_bot_session)

#loop = asyncio.get_event_loop()

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
    print('до.....')
    response = requests.get('http://api.forismatic.com/api/1.0/', send_data)
    json_response = response.json()
    print('после.....')
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

#def GetProxy():
    #response = requests.get('http://spys.me/proxy.txt', headers=headers)
    #async with aiohttp.ClientSession() as session:
     #   async with session.get('http://spys.me/proxy.txt', headers=headers) as response:
      #      #print((await response.content.read()).decode('utf-8').split('\n')[8::][1:-2])
       #     proxy = (await response.content.read()).decode('utf-8').split('\n')[8::]  # [1].split(' ')[0]
        #    #print(proxy)
         #   proxies = []
          #  #print(proxy)
           # for i in proxy[1:-2]:
            #    proxies.append(i.split(' ')[0])
            #return proxies
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

def GetDamn(name, sex):
    proxies = GetProxies()
    #print('got proxy', proxies)
    message = 'Прости, не смог оскорбить данного господина =('
    for proxy in proxies:
        try:
            print('trying', proxy, ' : ', end='')
            response = requests.get('https://damn.ru/?name={}&sex={}'.format(name, sex), proxies={'http': proxy, 'https': proxy}, headers=headers, stream=True, timeout=5)
            print(response.status_code)
            print(response.content.decode('utf-8'))
            message = response.status_code
            break
        except:
            print('Cant connect with this proxy, continue')
    return message

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
                                help_bot = """помощь - текущая команда помощи\nоботе - информация о боте\nвремя - текущая дата и время по МСК\nцитата - случайная цитата\nзаебало - случайный комментарий с сервиса zaebalo.ru\nобосрать - обосрать человека"""
                                VkBot_SendMessage(function=None, function_args=None, chat_id=event.chat_id, message=help_bot)
                            elif message == 'оботе':
                                about_bot = """Бот написан на Python.\nРазработчик: @sudo.rmrf\nРеппозиторий на github: github.com/sonerzerone/woonya\n~~~ Наслаждайтесь ~~~\nУзнать команды: .помощь"""
                                t0 = time()
                                VkBot_SendMessage(function=None, function_args=None, chat_id=event.chat_id, message=about_bot)
                                print(time()-t0)
                            elif message == 'время':
                                VkBot_SendMessage(function=None, function_args=None, chat_id=event.chat_id, message=str(datetime.datetime.now()))
                            elif message == 'цитата':
                                language = 'ru'
                                VkBot_SendMessage(function=None, function_args=None, chat_id=event.chat_id, message=GetRandomQuote(language))
                                #VkBot_SendMessage(function=SendRandomQuote, function_args=(language), chat_id=event.chat_id)
                            elif message == 'gavno':
                                print('test')
                                attachments = []
                                pic = Image.open(os.path.join(fileDir, 'static/images/memes/Трансформаторная-будка.jpg'))
                                print(pic)
                                image = bot_upload.photo_messages(pic)  # [0]
                                print(image)
                                attachments.append('photo{}_{}'.format(image['owned_id'], image['id']))
                                #VkBot_SendMessage(event.chat_id, message="соси хуй", attachments=','.join(attachments))
                            elif message == 'заебало':
                                #VkBot_SendMessage(event.chat_id, GetRandomCommentFromZaebaloRu())
                                VkBot_SendMessage(function=GetRandomCommentFromZaebaloRu, function_args=(None), chat_id=event.chat_id)
                            elif message == 'обосрать':
                                #VkBot_SendMessage(event.chat_id, message="Да иди ты к хуям блять хуяндопало ты тракторское сдохни и умри чтобы о тебе твоя мать не вспомнила, припизденыш ебаный блять")
                                #threading.Thread(target=GetDamn, args=['name', 'm']).start()
                                VkBot_SendMessage(function=GetDamn, function_args=('name', 'm'), chat_id=event.chat_id)
                                #VkBot_SendMessage(event.chat_id, GetDamn('name', 'm'))
                                #print('testtesttesttest')
                                #print('opa')
                                #VkBot_SendMessage(event.chat_id, GetDamn('name', 'm'))
                                


                    except:
                        continue




        except requests.exceptions.ReadTimeout as timeout:
            continue

if __name__ == "__main__":
    main()


