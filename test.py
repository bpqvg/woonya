# import asyncio
# import time
# import aiohttp
# import requests
# from bs4 import BeautifulSoup as B
# from aiohttp_proxy import ProxyConnector, ProxyType
#
# headers = {
#         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0',
#     }
#
# async def download_site(session,Proxy, connector):
#     print('sadfsadf')
#     async with session.get('https://api.steemit.com/', timeout=5) as response:
#         print(response.status)
#
# async def download_all_sites(sites):
#     print('test')
#     connector = ProxyConnector.from_url('http://45.64.99.26:8080')
#     loop = asyncio.get_event_loop()
#     async with aiohttp.ClientSession(connector=connector, loop=loop, headers=headers) as session:
#         tasks = []
#         for Proxy in sites:
#             print(Proxy)
#
#             task = asyncio.ensure_future(download_site(session, Proxy, connector))
#             tasks.append(task)
#         print('test2')
#         await asyncio.gather(*tasks, return_exceptions=True)
#
# def getproxies():
#     response = requests.get('https://free-proxy-list.net/', headers=headers)
#     soup = B(response.text, 'html.parser')
#     table = soup.find('table',id='proxylisttable')
#     list_tr = table.find_all('tr')
#     list_td = [elem.find_all('td') for elem in list_tr]
#     list_td = list(filter(None, list_td))
#     list_ip = [elem[0].text for elem in list_td]
#     list_ports = [elem[1].text for elem in list_td]
#     list_proxies = [':'.join(elem) for elem in list(zip(list_ip, list_ports))]
#     print(list_proxies)
#     return list_proxies
#
# if __name__ == "__main__":
#     sites = getproxies()[:5]
#     print(sites)
#     start_time = time.time()
#     asyncio.get_event_loop().run_until_complete(download_all_sites(sites))
#     duration = time.time() - start_time
#     print(f"Downloaded {len(sites)} sites in {duration} seconds")

# import asyncio
# import aiohttp
# from time import time
# #from aiosocks.connector import ProxyConnector, ProxyClientRequest
# #from aiohttp_proxy import ProxyConnector, ProxyType
# import requests
# from aiohttp_socks import ProxyType, ProxyConnector, ChainProxyConnector

# headers = {
#         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0',
#     }

# async def print_response(data):
#     print(data)

# async def fetch_content(url, session):
#     try:
#         async with session.get(url, allow_redirects=True) as response:
#             data = await response.read()
#             await print_response(data)
#     except aiohttp.ClientError as err:
#         print(err, 'cant connect with this proxy')

# async def print_range():
#     for i in range(10):
#         print(i)
#         await asyncio.sleep(0.2)

# async def main():
#     url = 'https://google.com'
#     tasks = []

#     #task = asyncio.create_task(print_range())
#     #tasks.append(task)

#     conn = ProxyConnector(
#         proxy_type=ProxyType.SOCKS5,
#         host='206.81.2.118',
#         port='1080',
#         rdns=True,
#         ssl=False

#     )
#     #conn = ProxyConnector.from_url('socks5://72.11.148.222:56533')

#     async with aiohttp.ClientSession(connector=conn) as session:  # connector=aiohttp.TCPConnector(ssl=False)
#         for i in range(10):
#             task = asyncio.create_task(fetch_content(url, session))
#             tasks.append(task)


#         await asyncio.gather(*tasks)

# if __name__ == "__main__":
#     t0 = time()
#     asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
#     loop = asyncio.get_event_loop()
#     try:
#         loop.run_until_complete(main())
#         loop.run_until_complete(asyncio.sleep(2.0))
#     finally:
#         #loop.close()
#         pass
#     print(time()-t0)




# from threading import Thread
# import requests
# from time import sleep
#
# headers = {
#         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0',
#     }
#
# def rrr(t):
#     for i in range(10):
#         print(i)
#         sleep(0.3)
#
# def main(t):
#     url = 'https://google.com'
#     for i in range(10):
#         print(requests.get('https://google.com', proxies={'http': '200.63.34.193:55837'}, headers=headers).content)
#
#
# if __name__ == "__main__":
#     thread1 = Thread(target=main, args=(1,))
#     thread2 = Thread(target=rrr, args=(1,))
#
#     thread1.start()
#     thread2.start()
#     thread1.join()
#    thread2.join()





#Get Proxy from spys.one txt format file without their api
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











# Подключаем модуль threading для работы с потоками
import threading
# и модули requests, shutil, os для скачивания файлов из сети
import requests, shutil, os

# Функция скачивания файла которую мы будем выполнять
# в новом потоке на входе номер потока и URL скачиваемого файла
def down(nomer, url):
    # Выводим на экран сообщение о старте нового потока
    print(str(nomer)+' поток ('+url+')\n')
    # Получаем имя файла из URL
    (dirname, filename) = os.path.split(url)
    # Запускаем скачивание через GET запрос
    r = requests.get(url, stream=True)
    # Если код ответа сервера 200 (сервер доступен)
    if r.status_code == 200:
        #r.raw.decode_content = True
        print(r.status_code)
        # Открываем файл в режиме побайтовой записи
        #with open(filename, 'wb') as f:
        #    r.raw.decode_content = True
            # Созхраняем скачиваемый поток в файл
        #    shutil.copyfileobj(r.raw, f)
        # Выводим сообщение что поток закончил загрузку
        print(str(nomer) + " поток закончил загрузку\n")
        

# Список URL которые будем скачивать
urls = ["http://www.irs.gov/pub/irs-pdf/f1040.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040a.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040ez.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040es.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040sb.pdf"]

# Цикл который создаст столько потоков сколько файлов нужно скачать
for nomer, url in enumerate(urls):
    # Запускаем поток указав целью функцию down и ее аргументы
    # к nomer прибавляем 1 чтобы номер потока начинался не с нуля
    threading.Thread(target=down, args = [nomer+1, url]).start()

# Выводим сообщение демонстрирующее что основная программа
# продолжает работать отдельно от созданных потоков
print('\nЕще не завершились потоки а программа уже продолжается\n')