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
import asyncio
from proxybroker import Broker
import gevent
from itertools import cycle
import aiohttp
from threading import Thread
from bs4 import BeautifulSoup as B
from time import sleep

headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0',
    }

fileDir = os.path.dirname(os.path.realpath('__file__'))

token = '6eefe0bbd01ec0838ae20aa0db713c1cddf3f4e84ccabf4fd05514e6720f4ab78b92eea3ef588c19f4d86'

vk_bot_session = vk_api.VkApi(token=token)
bot_api = vk_bot_session.get_api()
bot_upload = VkUpload(vk_bot_session)

#loop = asyncio.get_event_loop()

def VkBot_SendMessage(chat_id, message="", attachments=','):
    bot_api.messages.send(chat_id=chat_id, random_id=random.getrandbits(32), message=message)  # message=random.choice(replies)  message=event.message.text

def GetRandomQuote(language):
    send_data = {
        'method': 'getQuote',
        'format': 'json',
        'lang': language,
        'key': ""
    }
    response = requests.get('http://api.forismatic.com/api/1.0/', send_data)
    json_response = response.json()
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
    response = requests.get('https://free-proxy-list.net/', headers=headers)
    soup = B(response.text, 'html.parser')
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
    for i in range(10):
        print(i)
        sleep(0.5)
    for i in range(len(proxies)):
        try:
            print('trying', i, ' : ', end='')
            response = requests.get('https://google.com', proxies={'http': '200.63.34.193:55837'}, headers=headers)
            print(response.status_code)
            break
        except:
            print('Cant connect with this proxy, continue')
    #proxy_pool = cycle(proxies)
    #async with aiohttp.ClientSession() as session:
     #   tasks = []
      #  for proxy in proxies:
        #for i in range(0, len(proxies)-1):
            #proxy = next(proxy_pool)
       #     print('Request #{}'.format(proxy))
            #try:
        #    print('zashel')

         #   task = asyncio.ensure_future(test(session, proxy, name, sex))
         #   tasks.append(task)
        #await asyncio.gather(*tasks, return_exceptions=True)
                #print(response)
               # break
           # except:
                #print("Skipping. Connection error with this proxy.")

    #print(response)

#loop.run_until_complete(GetDamn('test', 'm'))



def main():
    #loop = asyncio.get_event_loop()
    #loop.run_until_complete(GetDamn('test', 'm'))
    #asyncio.gather(asyncio.create_task(GetDamn('name', 'm')))
    test_thread = Thread(target=GetDamn('test', 'm'), args=())
    #test_thread.daemon = True
    test_thread.start()
    #test_thread.run()


    while True:
        longpoll = VkBotLongPoll(vk_bot_session, '194888734')
        try:
            for event in longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    try:
                        if event.message.text[0] == '.':
                            message = event.message.text[1::]
                            if message == 'помощь':
                                help = """
                                время - текущая дата и время по МСК
                                цитата - случайная цитата
                                заебало - случайный комментарий с сервиса zaebalo.ru
                                обосрать - обосрать человека
                                """
                                VkBot_SendMessage(event.chat_id, help)
                            elif message == 'оботе':
                                about_bot = """
                                Бот написан на Python.
                                Разработчик: @sudo.rmrf
                                Реппозиторий на github: github.com/sonerzerone/woonya
                                ~~~ Наслаждайтесь ~~~
                                Узнать команды: .помощь
                                """
                                VkBot_SendMessage(event.chat_id, str(about_bot))
                            elif message == 'время':
                                VkBot_SendMessage(event.chat_id, str(datetime.datetime.now()))
                            elif message == 'цитата':
                                language = 'ru'
                                VkBot_SendMessage(event.chat_id, GetRandomQuote(language))
                            elif message == 'gavno':
                                print('test')
                                attachments = []
                                pic = Image.open(os.path.join(fileDir, 'static/images/memes/Трансформаторная-будка.jpg'))
                                print(pic)
                                image = bot_upload.photo_messages(pic)  # [0]
                                print(image)
                                attachments.append('photo{}_{}'.format(image['owned_id'], image['id']))
                                VkBot_SendMessage(event.chat_id, message="соси хуй", attachments=','.join(attachments))
                            elif message == 'заебало':
                                VkBot_SendMessage(event.chat_id, GetRandomCommentFromZaebaloRu())
                            elif message == 'обосрать':
                                #VkBot_SendMessage(event.chat_id, message="Да иди ты к хуям блять хуяндопало ты тракторское сдохни и умри чтобы о тебе твоя мать не вспомнила, припизденыш ебаный блять")
                                #loop.run_until_complete(GetDamn('test', 'm'))



                    except:
                        continue




        except requests.exceptions.ReadTimeout as timeout:
            continue

if __name__ == "__main__":
    #asyncio.run(main())
    #thread_main = Thread(target=main, args=())
    main()


