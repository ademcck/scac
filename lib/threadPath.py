from typing import Counter
from urllib.parse import urlparse
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import time, sleep, ctime
import json, asyncio
import random, os
from colorama import Fore
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

class Scac:
    def __init__(self, urls, thread, delay, verbose):
        self.config = json.loads(open('json/path-php.json').read())
        self.keys = list(self.config.keys()) # Json keys
        if urls == 'json':
            self.config_urls = json.loads(open('json/urls.json').read())
            self.keys_urls = list(self.config_urls.keys()) # Json keys
        self.config_fe = json.loads(open('json/dirs_files.json').read())
        self.keys_f = list(self.config_fe['files']) # Json keys
        self.keys_e = list(self.config_fe['exts']) # Json keys
        self.url = urls
        self.past = [] # tried json values
        self.send_list = []
        self.processes = [] 
        self.delay = delay
        self.thread = thread
        self.content_lengt = 0
        self.pathResult = []
        self.count = 0 # counting for the thread. If the remaining result of the given thread section is 0, the program will enter sleep mode.
        self.verbose = bool(verbose)
        self.rows, self.columns = os.popen('stty size', 'r').read().split() # Terminal rows and columns sizing.
        self.info()
    
    # async def races(self):
    #     # this function for sleep mode
    #     if self.verbose:
    #         print(Fore.YELLOW+f"{self.delay} seconds in standby mode")
    #     await asyncio.sleep(self.delay)
    
    def info(self):

        text = "Calm down my friend. We Strive For You.|At this stage, you better go sip your coffee.|The best results come from the best research."
        str = " "
        for i in text.split("|"):
            for x in i :
                str += x
                print('{}\r'.format(str),end="")
                sleep(random.uniform(0.01, 0.1))
            str = ""
            print()
        sleep(1)
        print(Fore.CYAN+"*"*int(self.columns))
        self.run()
        

    def sender(self,url):
        # for http requests

        if url.split("/")[-1] in self.past:
            pass
        else:
            try:
                html = requests.get(url, stream=True)
                if self.verbose:
                    print(Fore.GREEN + "[+]",Fore.RESET+"%s: %s" % (url.split("/")[-1], ctime(time())))
                return Fore.GREEN+str(html.status_code) + Fore.RESET+ " [+] For " + url

            except requests.exceptions.ConnectionError:
                print(Fore.RED+'[-]'+Fore.CYAN+f' connection error for {url}')
    def urlsOnJson(self):
        self.url = []
        for i in self.config_urls[self.keys_urls[0]]:
            if i[-1:len(i):1] == "/":
                self.url.append(i)
            elif "?" not in i:
                self.url.append(i + "/")
        self.run()
    def randomAgent(self):
        software_names = [SoftwareName.CHROME.value,SoftwareName.FIREFOX.value]
        operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value] 
        user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
        return user_agent_rotator.get_random_user_agent()

    def urlPathTesting(self,u):
        def pathFinder(url):
            if url not in self.past:
                self.past.append(url)
                r = requests.get(url,headers={'User-Agent': self.randomAgent()})
                if (r.status_code == 200 or r.status_code == 301 or r.status_code == 302 or r.status_code == 201) and len(r.content) != self.content_lengt and '404 not fount' not in r.text.lower():
                    print(Fore.GREEN + "[+]",Fore.RESET+"%s: %s" % (url, Fore.LIGHTRED_EX+ctime(time())))
                    self.pathResult = list(set(self.pathResult)).append(url)
                elif self.verbose == True: print(Fore.RED + "[-]",url)

        pathFinder(u)
    def run(self):
        # pool processor.

        self.start = time()
        self.count = 0
        contResult = False
        with ThreadPoolExecutor(max_workers=10) as executor:
            if type(self.url) == list:
                for url in self.url:
                    for i in self.keys_e:
                        if i in urlparse(url).path: 
                            contResult = False
                            break
                        else: contResult = True
                    if contResult == False: continue
                    self.content_lengt = requests.get(urlparse(url).scheme + "://" + urlparse(url).netloc,headers={'User-Agent': self.randomAgent()})
                    print(
                        Fore.CYAN+"*"*int(self.columns) + "\n",
                        Fore.GREEN + f'Testing For {url} '.center(int(self.columns)) + "\n" 
                    )
                    for i in self.keys:
                        print(
                            Fore.RED+"+-"*int(self.columns)+ "\n" +
                            Fore.GREEN + f'Testing For {i} '.center(int(self.columns)) + "\n" +
                            Fore.RED+"+-"*int(self.columns)
                            )
                        
                        for a in self.config[i]:
                            # url controls
                            for f in self.keys_f:
                                self.processes.append(executor.submit(self.urlPathTesting, (url + f + a)))
                                for e in self.keys_e:
                                    # Bekleme işleminde kaldık
                                    if self.count % self.thread == 0 and self.count > 0: 
                                        self.processes.append(executor.submit(self.urlPathTesting, (url + f + e + a)))
                                        #asyncio.run(self.races())
                                        if self.verbose:  print(Fore.YELLOW+f"{self.delay} seconds in standby mode")
                                        sleep(self.delay)
                                        self.count += 1
                                    else: 
                                        self.processes.append(executor.submit(self.urlPathTesting, (url + f + e + a)))
                                        self.count += 1
                            
             
                                
                    self.past = []
                            
            else:
                print(
                    Fore.CYAN+"*"*int(self.columns) + "\n",
                    Fore.GREEN + f'Testing For {self.url} '.center(int(self.columns)) + "\n" 
                )
                for i in self.keys:
                        print(
                            Fore.RED+"+-"*int(self.columns)+ "\n" +
                            Fore.GREEN + f'Testing For {i} '.center(int(self.columns)) + "\n" +
                            Fore.RED+"+-"*int(self.columns)
                            )
                        
                        for a in self.config[i]:
                            # url controls
                            for f in self.keys_f:
                                self.processes.append(executor.submit(self.urlPathTesting, (self.url + f + a)))
                                for e in self.keys_e:
                                    # Bekleme işleminde kaldık
                                    if self.count % self.thread == 0 and self.count > 0: 
                                        self.processes.append(executor.submit(self.urlPathTesting, (self.url + f + e + a)))
                                        #asyncio.run(self.races())
                                        if self.verbose and self.delay != 0: print(Fore.YELLOW+f"{self.delay} seconds in standby mode")
                                        sleep(self.delay)
                                        self.count += 1
                                    else: 
                                        self.processes.append(executor.submit(self.urlPathTesting, (self.url + f + e + a)))
                                        self.count += 1
        
        self.finaly()
                
    def finaly(self):
        # and results

        for url in self.pathResult:
            print(Fore.GREEN + "[+]",Fore.RESET+"%s: %s" % (url, Fore.LIGHTRED_EX+ctime(time())))
            data = {}
            data['result'] = self.pathResult
            with open('json/resultPath.json') as outfile:
                json.dump(data, outfile)
        
        return (    
                    Fore.LIGHTRED_EX+"*"*int(self.columns) + "\n" +
                    Fore.GREEN+'File Created'.center(int(self.columns)) + "\n" +
                    Fore.GREEN+f'Exploit stage passed'.center(int(self.columns)) + "\n" +
                    Fore.LIGHTRED_EX+"*"*int(self.columns) 
                )
    
#if __name__ == "__main__":
    # sc = Scac(urls='https://zuhalsunger.com/', thread=11, delay=5, verbose=True)
    # sc.urlsOnJson()
    #Scac(urls='https://zuhalsunger.com/', thread=41, delay=0.5, verbose=False)
   