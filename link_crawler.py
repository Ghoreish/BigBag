import re
import requests


def getlinks(text):
    links = re.findall('[\'\">](http[s]?://[^\'\"<>\n]+)', text)
    return links


def getpaths(text):
    paths = re.findall('[\'\"]([./]*[/][-a-zA-Z0-9()!@:%_+.~#?&=]+[-a-zA-Z0-9()!@:%_+.~#?&/=]+)[\'\"]', text)
    if '//' in paths:
        print(text)
    return paths


def gethost(link):
    hostname = re.findall('(http[s]?://)?([a-zA-Z0-9.]+[.][a-zA-Z]+)', link)
    try:
        return hostname[0][0] + hostname[0][1]
    except:
        return []


def check_for_large(url, proxy):
    r = requests.head(url, verify=False, proxies=proxy)
    if 'Content-Length' not in r.headers:
        return False
    cl = r.headers['Content-Length']
    if int(cl) > 2000000:
        return True
    else:
        return False


def extract_links(link, allowed_host, filename, checked_links=[], selected_links=[], proxy=None, cookies={}):
    print(link)
    if link in checked_links:
        return None
    hostname = gethost(link)
    if allowed_host not in hostname:
        return None
    if check_for_large(link, proxy):
        return None
    try:
        r = requests.get(link, allow_redirects=True, proxies=proxy, verify=False, cookies=cookies)
        res = r.text
    except Exception as e:
        print(link)
        print(e)
        return None
    if link in checked_links:
        return None
    checked_links.append(link)
    hostname = gethost(link)
    if allowed_host not in hostname:
        return None
    f = open(filename, 'w')
    for i in selected_links:
        try:
            f.write(i)
            f.write('\n')
        except Exception as e:
            print(e)
            print(i)
    f.close()
    if r.url not in selected_links:
        selected_links.append(r.url)
    pure_links = getlinks(res)
    pure_paths = getpaths(res)
    links = []
    for i in pure_links:
        if i not in checked_links:
            links.append(i)
    for i in pure_paths:
        if i[0] != '/':
            temp_link = link + '/' + i
        else:
            temp_link = hostname + i
        print(temp_link, 1)

        if temp_link not in checked_links:
            links.append(temp_link)
    for i in links:
        if i not in checked_links:
            extract_links(i, allowed_host, filename, checked_links, proxy=proxy, cookies=cookies)
    return selected_links


filename = 'example.txt'
url = 'https://example.com'
allowed_host = 'https://example.com'
proxy = {'http': 'http://127.0.0.1:8080',
         'https': 'http://127.0.0.1:8080'}
cookie = {}
l = extract_links(url, allowed_host, filename, proxy=proxy, cookies=cookie)

f = open(filename, 'w')
for i in l:
    try:
        f.write(i)
        f.write('\n')
    except:
        print(i)
f.close()
for i in l:
    print(i)
