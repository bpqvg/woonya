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
import lxml
import threading
from time import sleep, time, ctime
from io import StringIO, BytesIO

headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0',
    }

help_bot = """помощь - текущая команда помощи
оботе - информация о боте
время - текущая дата и время по МСК
цитата - рандомная цитата
заебало - высеры случайных людей
обосрать @имя - обозвать кого-либо"""

about_bot = """Бот написан на Python.
Разработчик: @sudo.rmrf
Реппозиторий на github: github.com/sonerzerone/woonya
~~~ Наслаждайтесь ~~~
Узнать команды: .помощь"""


fileDir = os.path.dirname(os.path.realpath('__file__'))

token = ''

vk_bot_session = vk_api.VkApi(token=token)
bot_api = vk_bot_session.get_api()
bot_upload = VkUpload(vk_bot_session)

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
        for proxy in proxies:
            threading.Thread(target=CheckAndAddProxy, args=[proxy]).start()
            
        sleep(30)


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
    return list_proxies


def GetProxies2():
    response = requests.get('http://spys.me/proxy.txt', headers=headers)
    proxy = response.content.decode('utf-8').split('\n')[8::]  # [1].split(' ')[0]
    proxies = []
    for i in proxy[1:-2]:
        proxies.append(i.split(' ')[0])
    return proxies


def GetRandomQuote(language='ru'):
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


def GetCurrentDateAndTime():
    datetime = ctime()
    return datetime


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


def GetDamn(name, sex):
    message = 'Не смог оскорбить, утерял дар речи.'
    proxies = available_proxy
    for proxy in reversed(proxies):
        try:
            custom_headers = headers
            response = requests.get('https://damn.ru/?name={}&sex={}'.format(name, sex), proxies={'http': proxy, 'https': proxy}, headers=custom_headers, stream=True, timeout=3)
            #print(response.status_code)
            root = lxml.html.fromstring(response.content)
            damn = root.xpath('/html/body/div[2]/div/div/div[2]/div[1]/div[1]')[0].text_content()
            message = damn
            break
        except:
            print('Def | GetDamn | Cant connect with this proxy, continue. Proxy: {}'.format(proxy))
    return message


def VkBot_SendMessage(from_id, peer_id, message=""):
    if from_id != -1:
        message = '@id{}(Семпай,) {}'.format(from_id, message)
    bot_api.messages.send(peer_id=peer_id, random_id=random.getrandbits(32), message=message)


def eventHandler_NewMessage(event):
    peer_id = event.message.peer_id
    from_id = event.message.from_id
    message = event.message.text
    message = message.split(' ')
    if message[0] == '.помощь':
        VkBot_SendMessage(from_id=from_id, peer_id=peer_id, message=help_bot)
    elif message[0] == '.оботе':
        VkBot_SendMessage(from_id=from_id, peer_id=peer_id, message=about_bot)
    elif message[0] == '.время':
        VkBot_SendMessage(from_id=from_id, peer_id=peer_id, message=GetCurrentDateAndTime())
    elif message[0] == '.цитата':
        language = 'ru'
        VkBot_SendMessage(from_id=from_id, peer_id=peer_id, message=GetRandomQuote(language=language))
    elif message[0] == '.gavno':
        pass

        # 591975834
        # print('test')
        # attachments = []
        # pic = Image.open(os.path.join(fileDir, 'static/images/memes/Трансформаторная-будка.jpg'))
        # print(pic)
        # image = bot_upload.photo_messages(pic)  # [0]
        # print(image)
        # attachments.append('photo{}_{}'.format(image['owned_id'], image['id']))
        #VkBot_SendMessage(event.chat_id, message="соси хуй", attachments=','.join(attachments))
    elif message[0] == '.заебало':
        VkBot_SendMessage(from_id=from_id, peer_id=peer_id, message=GetRandomCommentFromZaebaloRu())
    elif message[0] == '.обосрать':
        required_help = 'Необходимо указать человека :P'
        if len(message) < 2:
            VkBot_SendMessage(from_id=from_id, peer_id=peer_id, message=required_help)
            return
        user_group_id = message[1].replace('[',' ').replace(']',' ').split('|')[0]
        group_info, user_info = -1, -1
        if 'club' in user_group_id:
            user_group_id = user_group_id[5:]
            group_info = bot_api.groups.getById(group_id=user_group_id)[0]
        elif 'id' in user_group_id:
            user_group_id = user_group_id[3:]
            user_info = bot_api.users.get(user_id=user_group_id)[0]
        if user_info == -1 and group_info == -1:
            VkBot_SendMessage(from_id=from_id, peer_id=peer_id, message=required_help)
            return
        dictionary = 'qwertyuiopasdfghjklzxcvbnm'
        damnname = ''.join(random.choice(dictionary) for x in range(random.randint(5, len(dictionary))))
        damn = GetDamn(damnname, 'm')  # Выполнить функцию с запросом
        tmpname = ''
        if user_info != -1:
            name = user_info['first_name']
            id = user_info['id']
            tmpname = '@id{}({})'.format(id, name)
        elif group_info != -1:
            name = group_info['name']
            id = group_info['id']
            tmpname = '@club{}({})'.format(id, name)
        damn = damn.replace(damnname, tmpname)
        VkBot_SendMessage(from_id=-1, peer_id=peer_id, message=damn)



def main():
    while True:
        longpoll = VkBotLongPoll(vk_bot_session, '194888734')
        try:
            for event in longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    threading.Thread(target=eventHandler_NewMessage, args=[event]).start()

        except requests.exceptions.ReadTimeout as timeout:
            continue

if __name__ == "__main__":
    threading.Thread(target=ProxyUpdater, args=[]).start()
    main()

