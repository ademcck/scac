import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import time, sleep
import time as Ttime
import json


config = json.loads(open('json/path-php.json').read())
print(list(config.keys()))
#from lib import request
import re
from urllib.parse import urljoin
import colorama
from colorama import Fore, Back, Style

colorama.init(autoreset=True)
targetLinks=[]

def spider(url):
	r = requests.get(url)
    hrefLinks = re.findall(r'(?:href=")(.*?)"', r.content.decode('utf-8', 'ignore'))

	for link in hrefLinks:
		link = urljoin(url, link)

		if "#" in link:
			link = link.split("#")[0]
		if (url in link) and (link not in targetLinks):
			targetLinks.append(link)
			print(Fore.RED+"="*30)
			print(Fore.RED+"| ",Fore.GREEN+"[+] Found URL: "+link)
			print(Fore.RED+"="*30)
			try:
				spider(link)
			except KeyboardInterrupt:
				return targetLinks
				break