import re
import requests


def getlinks(text):
    links = re.findall('[\'\">](http[s]?://[^\'\"<>\n]+)', text)
    final_links = []
    for i in links:
        temp_link = i.split("//", 1)
        while "//" in temp_link[1]:
            temp_link[1] = temp_link[1].replace("//", "/")
        final_links.append(temp_link[0] + temp_link[1])
    return final_links


def getpaths(text):
    paths = re.findall('([./]*[/][-a-zA-Z0-9()!@:%_+.~#?&=]+[-a-zA-Z0-9()!@:%_+.~#?&/=]+)', text)
    final_paths = []
    for i in paths:
        temp_path = i
        if i[:2] == "//":
            continue
        while "//" in temp_path:
            temp_path = temp_path.replace("//", "/")
        final_paths.append(temp_path)
    return final_paths


def gethost(link):
    hostname = re.findall('(http[s]?://)?([-a-zA-Z0-9.]+[.][-a-zA-Z]+)', link)
    try:
        return hostname[0][0] + hostname[0][1]
    except:
        return []


def check_for_large(url, proxy):
    r = requests.head(url, verify=False, proxies=proxy)

    if 'Content-Length' not in r.headers:
        return False
    cl = r.headers['Content-Length']
    if int(cl) > 100000000:
        return True
    else:
        return False


complete_checked_links = set()
all_links = set()
temp_links = set()
error_links = set()
target_link = input("target: ")
allowed_host = input("allowed host: ")
filename = input("filename: ")
proxy = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"} #burp proxy you can empty this dict for direct crawling
all_links.add(target_link)
while len(all_links) != len(complete_checked_links):
    for i in all_links:
        f = open(filename, "w")
        for j in complete_checked_links:
            f.write(j)
            f.write("\n")
        if i not in complete_checked_links and allowed_host in gethost(i):
            try:
                if check_for_large(i, proxy=proxy) == True:
                    print("large link:", i)
                    complete_checked_links.add(i)
                    continue
                r = requests.get(i, proxies=proxy, verify=False)
                if "<h1>Burp Suite Professional</h1>" in r.text:
                    error_links.add(i)
                    continue
                if gethost(r.url) not in allowed_host:
                    complete_checked_links.add(i)
                    continue
            except:
                print("error")
                error_links.add(i)
                r = None
            if r != None:
                res = r.text
                links = getlinks(res)
                paths = getpaths(res)
                for j in links:
                    if allowed_host in gethost(j) and j not in complete_checked_links:
                        temp_links.add(j)
                for j in paths:
                    if j[:3] == "../":
                        if r.url[-1] == "/":
                            jpath = r.url[:-1] + j
                        else:
                            jpath = r.url + j
                    else:
                        basehost = gethost(r.url)
                        if basehost[-1] == "/" or j[0] == "/":
                            jpath = basehost + j
                        else:
                            jpath = basehost + "/" + j
                    if jpath in complete_checked_links:
                        continue
                    if allowed_host in gethost(jpath):
                        temp_links.add(jpath)
        complete_checked_links.add(i)
    if len(error_links) != 0:
        print("!errors!")
        for j in error_links:
            print(j)
        check_errors_again = None
        while check_errors_again not in ["y", "n"]:
            check_errors_again = input("check them again? (y/n)")
        if check_errors_again == "y":
            for j in error_links:
                if allowed_host in gethost(j):
                    temp_links.add(j)
        else:
            error_links = set()
            error_links.add(1)
        if len(error_links) != 0:
            additional_link_ask = None
            while additional_link_ask not in ["y", "n"]:
                additional_link_ask = input("any additional links? (y/n)")
            if additional_link_ask == "y":
                add_link = input("link: ")
                while add_link != "":
                    temp_links.add(add_link)
                    add_link = input("link: ")
        error_links = set()
    f = open(filename, "w")
    for i in complete_checked_links:
        f.write(i)
        f.write("\n")
    f.close()
    for i in temp_links:
        all_links.add(i)
    temp_links = set()
