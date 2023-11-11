import os
import requests
import time

def grab_from_list(dirname: str, links: list, proxy=None):
    os.mkdir(dirname)
    for i in links:
        if i[-1] == '/':
            i = i[:-1]
        filename = i.split('/')[-1]
        if '.' not in filename:
            filename += '.html'
        path = dirname + '/' + filename
        try:
            r = requests.get(i, verify=False, proxies=proxy)
        except:
            print(i)
            continue
        try:
            f = open(path, 'wb')
        except:
            f = open('files/' + str(time.time()) + '.html', 'wb')
        f.write(b'//')
        f.write(r.url.encode())
        f.write(b'\n//')
        f.write(str(r.headers).encode())
        f.write(b'\n')
        f.write(r.content)
        f.close()

f = open('links.txt', 'r')
res = f.readlines()
res = [x[:-1] for x in res]
proxy = {'http': 'http://127.0.0.1:8080',
         'https': 'http://127.0.0.1:8080'}
grab_from_list('files', res, proxy=proxy)
