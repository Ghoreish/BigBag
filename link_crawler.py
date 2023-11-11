import re
import requests

def getlinks(text):
    links = re.findall('[\'\"](http[s]?://[^\'\"<>\n]+)', text)
    return links


def getpaths(text):
    paths = re.findall('[\'\"](/[-a-zA-Z0-9()!@:%_+.~#?&=]+[-a-zA-Z0-9()!@:%_+.~#?&/=]+)[\'\"]', text)
    if '//' in paths:
        print(text)
    return paths


def gethost(link):
    hostname = re.findall('(http[s]?://)?([a-zA-Z0-9.]+[.][a-zA-Z]+)', link)
    try:
        return hostname[0][0] + hostname[0][1]
    except:
        return []


def extract_links(link, allowed_host, checked_links=[], selected_links=[], proxy=None):
    if link in checked_links:
        return None
    checked_links.append(link)
    hostname = gethost(link)
    if allowed_host not in hostname:
        return None
    try:
        r = requests.get(link, verify=False, proxies=proxy)
        res = r.text
    except:
        return None
    if r.url not in selected_links:
        selected_links.append(r.url)
    pure_links = getlinks(res)
    pure_paths = getpaths(res)
    links = []
    for i in pure_links:
        if i not in checked_links:
            links.append(i)
    for i in pure_paths:
        temp_link = hostname + i
        if temp_link not in checked_links:
            links.append(temp_link)
    for i in links:
        if i not in checked_links:
            extract_links(i, allowed_host, checked_links)
    return selected_links



proxy = {'http': 'http://127.0.0.1:8080',
         'https': 'http://127.0.0.1:8080'}

l = extract_links('{example link}', '{example host}', proxy=proxy)


f = open('links.txt', 'w')
for i in l:
    try:
        f.write(i)
        f.write('\n')
    except:
        print(i)
f.close()
for i in l:
    print(i)
