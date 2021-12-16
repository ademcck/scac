from bs4 import BeautifulSoup
from urllib.parse import urlencode, urlunparse, urlparse
from urllib.request import urlopen, Request
from time import time, ctime
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import os
from colorama import Fore


class SearchBing:
    def __init__(self,url,limit=10, verbose=False):
        self.num = 0 
        self.num2 = 0
        self.num3 = 1
        self.link_next = ""
        self.all_a_links = ()
        self.rest = True
        self.resultt = []
        self.query = url
        self.verbose = verbose
        self.limit = limit

    def searchBing(self):
        while self.num <= self.limit:
            if self.rest != False:
                try:
                    self.run()
                except KeyboardInterrupt:
                    print(Fore.YELLOW+"Exit done") 
                    self.result()
                    break
                except:
                    pass
            else:
                self.result()
                break
        self.result()
        return self.resultt

    def request_bing(self,page_next=""):
        software_names = [SoftwareName.CHROME.value,SoftwareName.FIREFOX.value]
        operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value] 
        user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
        user_agent = user_agent_rotator.get_random_user_agent()
        if self.num == 0:
            url = urlunparse(("https", "www.bing.com", "/search", "", urlencode({"q": self.query}), "" ))
        else:
            url = page_next
        custom_user_agent = user_agent
        req = Request(url, headers={"User-Agent": custom_user_agent})
        page = urlopen(req)
        self.num += 1
        return page

    def soup_bing(self,page_next=""):
        page = self.request_bing(page_next)
        
        soup = BeautifulSoup(page.read(),"html.parser")
        links_a = soup.find_all("li",attrs={"class":"b_algo"})
        links = soup.find_all("a",attrs={"class":"b_widePag sb_bp"})
        links_list = []
        for i in links:
            links_list.append("https://www.bing.com"+i["href"])
        link_next =  soup.find("a",attrs={"class":"sb_pagN sb_pagN_bp b_widePag sb_bp"})["href"]
        link_next = "https://www.bing.com" + link_next
        
        
        for i in links_a:
            self.resultt.append(i.h2.a["href"])
            context = str(self.num3) + "-" + urlparse(i.h2.a["href"]).netloc + "||" + i.h2.a["href"]
            new_list = list(self.all_a_links)
            new_list.append(context)
            self.all_a_links = tuple(new_list)
            self.num3 += 1
            
        return {"links":links_list, "link_next":link_next}


    def run(self):
        while True:
            if self.num == 0:
                result = self.soup_bing()
                self.link_next = result["link_next"]
            else:
                try:
                    if self.link_next:
                        result = self.soup_bing(self.link_next)
                        self.link_next = result["link_next"]
                    else:
                        self.rest = False
                        break
                except UnboundLocalError:
                    if self.num2 <= 10:
                        self.num2 += 1
                        continue
                    else:
                        self.rest = False
                        break

    def result(self):
        rows, columns = os.popen('stty size', 'r').read().split()
        for context in self.all_a_links:
            context =  context.split("||")
            # if self.verbose == True:
            #     print(Fore.GREEN + "[+]",Fore.RESET+"%s: %s" % (context[1], Fore.LIGHTRED_EX + ctime(time())))
        print(Fore.CYAN+"+"*int(columns))



 