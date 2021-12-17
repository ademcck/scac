import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import time, sleep, ctime
import random, os, re, json
from urllib.parse import urljoin, urlparse
from urllib.error import HTTPError, URLError
from colorama import Fore
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from googlesearch import search
import googlesearch
from lib.searchBing import SearchBing

class ScacDirb:
    def __init__(self, urls, thread, methode, verbose,  delay=2, query=""):
        self.config = json.loads(open('json/dirs_files.json').read())
        self.keys = list(self.config.keys()) # Json keys
        self.url = urls
        self.methode = methode
        self.past_dirs = [] # tried json values
        self.past_files = [] # tried json values
        self.past_exts = [] # tried json values
        self.send_list = []
        self.result_dirs = []
        self.result_file = []
        self.count = 0
        self.processes = []
        self.thread = thread
        self.status = False
        self.duration = 5
        self.verbose = bool(verbose)
        if query != "":
            self.query = f" {query}"
        else:
            self.query = query
        self.query = "site:" + urlparse(self.url).netloc + self.query
        self.delay = delay
        self.rows, self.columns = os.popen('stty size', 'r').read().split() # Terminal rows and columns sizing.
        self.info()
    
    def info(self):
        text =  "I hope everything is fine for you....|Go sip your coffee. Because this will take some time.|Don't worry, everything is under our control."
        str = ""
        if self.methode == 'spider': self.spider()
        else: 
            for i in text.split("|"):
                for x in i :
                    str += x
                    print('{}\r'.format(str),end="")
                    sleep(random.uniform(0.01, 0.2))
                str = ""
                print()
            sleep(1)
            if self.methode == "all":
                self.spider()
                self.search()
            elif self.methode == 'search':
                self.search()
            elif self.methode == 'spider':
                self.spider()
    def randomAgent(self):
        software_names = [SoftwareName.CHROME.value,SoftwareName.FIREFOX.value]
        operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value] 
        user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
        return user_agent_rotator.get_random_user_agent()

    def spider(self):
        print(Fore.YELLOW + "First request sent.".center(int(self.columns)))
        def sp(url):
            r = requests.get(url, headers={"User-Agent": self.randomAgent()})
            hrefLinks = re.findall(r'(?:href=")(.*?)"', r.content.decode('utf-8', 'ignore'))
            print(Fore.GREEN + "[+]",Fore.RESET+"%s: %s" % (url, Fore.LIGHTRED_EX+ctime(time())))
            for link in hrefLinks:
                link = urljoin(self.url, link)
                if urlparse(link).netloc == urlparse(self.url).netloc:
                    self.processes.append(link)
            self.processes = list(set(self.processes))
        sp(self.url)
        print(Fore.GREEN + "*"*int(self.columns))
        print(Fore.YELLOW + "sending multiple requests..")
        with ThreadPoolExecutor(max_workers=10) as executor:
            for i in self.processes:
                if self.count % self.thread == 0 and self.count > 0: 
                    executor.submit(sp, i)
                    sleep(self.delay)
                    self.count += 1
                else: 
                    executor.submit(sp, i)
                    self.count += 1
        print(Fore.GREEN + "*"*int(self.columns))
        # for i in self.processes:
        #     print(Fore.GREEN + "[+]",Fore.RESET+"%s: %s" % (i, ctime(time())))
        #     sleep(random.uniform(0.01, 0.1))
        
    def inTesting():
        pass
        # def sender(self,url):
        #     # for http requests
        #     url, path = url.split(";")[0], url.split(";")[-1]
        #     def reqSend(u,which):
        #         try:
        #             html = requests.get(u, stream=True,headers={"User-Agent": self.randomAgent()})
        #             if html.status_code == 200 and which == 'dir':
        #                 self.result_dirs.append(u)
        #                 self.processes(u)
        #                 print(Fore.GREEN + "[+]",Fore.RESET+"%s: %s" % (u, ctime(time())))
        #                 return Fore.GREEN+str(html.status_code) + Fore.RESET+ " [+] For " + u
        #             elif html.status_code == 200 and which == 'file':
        #                 self.processes(u)
        #                 self.result_file.append(u)
        #                 print(Fore.GREEN + "[+]",Fore.RESET+"%s: %s" % (u, ctime(time())))
        #                 return Fore.GREEN+str(html.status_code) + Fore.RESET+ " [+] For " + u
                    

        #         except requests.exceptions.ConnectionError:
        #             print(Fore.RED+'[-]'+Fore.CYAN+f' connection error for {u}')
        #         except KeyboardInterrupt:
        #             self.finaly()

        #     if path == 'dir' and url.split("/")[-1] in self.past_dirs: pass
        #     else: reqSend(url,'dir')

        #     if path == 'fileExt' and url.split("/")[-1].split(".")[0] in self.past_files:
        #         if url.split("/")[-1].split(".")[-1] in self.past_exts:
        #             pass
        #         else:
        #             reqSend(url,'file')

            

        # def run(self):
        #     # pool processor.
        #     self.start = time()
        #     with ThreadPoolExecutor(max_workers=10) as executor:
        #         print(
        #             Fore.CYAN+"*"*int(self.columns) + "\n",
        #             Fore.GREEN + f'Testing For {self.url} '.center(int(self.columns)) + "\n" 
        #         )
                
        #         for dir in self.config['dirs']:
        #             self.processes.append(executor.submit(self.sender, (self.url + "/" + dir + ";dir")))
        #             self.past_dirs.append(dir)
        #             if len(self.result_dirs) > 0:
        #                 for file in self.config['files']:
        #                     for ext in self.config['exts']:
        #                         if self.status == False: 
        #                             executor.submit(self.sender, (self.url + "/" + file + "." +ext + ";fileExt"))
        #                             self.status = True
        #                         else:
        #                             executor.submit(self.sender, (self.url + "/" + dir + "/" + file + "." +ext + ";fileExt"))
                                
        #                         self.past_exts.append(ext)
        #                     self.past_files.append(file)
        #             self.result_dirs = []
                    
                    
                
        #         self.past_dirs = []
        #         self.past_files = []
        #         self.past_exts = []
            
        #     print(self.finaly())
                
    def search(self):
        self.start = time()
        
        print(
            Fore.CYAN+"*"*int(self.columns) + "\n" +
            Fore.GREEN + f'"Google Search" Testing For {self.query} '.center(int(self.columns)) + "\n" +
            Fore.CYAN+"*"*int(self.columns) 
        )
        def googleSearch():
            links = search(self.query, pause=self.delay)
            for i in links: self.processes.append(i)
            for i in self.processes: 
                    print(Fore.GREEN + "[+]",Fore.RESET+"%s: %s" % (i, Fore.LIGHTRED_EX+ctime(time())))
        while self.duration <= 10:
            try:
                googleSearch()  
                if self.duration == 10:
                    print(
                        Fore.CYAN+"*"*int(self.columns) + "\n" +
                        Fore.RED + "'Google Search' currently unavailable".center(int(self.columns)) + "\n" +
                        Fore.YELLOW + "Duration "+str(self.duration) + "\n" +
                        Fore.CYAN+"*"*int(self.columns) 
                    )
                break
            except HTTPError:
                
                print(
                    Fore.CYAN+"*"*int(self.columns) + "\n" +
                    Fore.RED + "HTTP Error 429: Too Many Requests".center(int(self.columns)) + "\n" +
                    Fore.YELLOW + "Duration For "+str(self.duration) + "\n" +
                    Fore.CYAN+"*"*int(self.columns) 
                    )
                self.duration += 1
                sleep(self.duration)
                continue
            except URLError:
                print(Fore.MAGENTA+"Please Check Your Network Connection") 
                break
            except KeyboardInterrupt:
                print(Fore.YELLOW+"Exit done") 
                break
        
        print(
            Fore.CYAN+"*"*int(self.columns) + "\n" +
            Fore.GREEN + f'"Bing Search" Testing For {self.query} '.center(int(self.columns)) + "\n" +
            Fore.CYAN+"*"*int(self.columns) 
        )
        sb = SearchBing(self.query,limit=100, verbose=self.verbose)
        rst = sb.searchBing()
        for i in rst:
            self.processes.append(i)
            print(Fore.GREEN + "[+]",Fore.RESET+"%s: %s" % (i, Fore.LIGHTRED_EX+ctime(time())))
        self.urlsSave()
        

    def urlsSave(self):
        data = {}
        data['urls'] = list(set(self.processes))
        with open('json/urls.json', 'w') as outfile:
            json.dump(data, outfile)
        
                
    def finaly(self):
        # and results
        for task in as_completed(self.processes):
            if task.result() != None:
                print(task.result())
        
        return (    
                    Fore.LIGHTRED_EX+"*"*int(self.columns) + "\n" +
                    Fore.LIGHTCYAN_EX+f'Time taken: {time() - self.start}'.center(int(self.columns)) + "\n" +
                    Fore.LIGHTRED_EX+"*"*int(self.columns) 
                )
    

   