# scac
SCAC is a directory, file and vulnerability research program.


```python
┌──(ademcck㉿kali)-[~/Desktop/scac]
└─$ python3 main.py -h                                      
usage: main.py [-h] [-u URL] [-t THREAD] [-d DELAY] [-f] [-m METHODE] [-q QUERY]
               [-c COOKIE] [-v VERBOSE] [-o OUTPUT]

Scanner Tool.

optional arguments:
  -h, --help  show this help message and exit
  -u URL      Target urls/hosts, {Examples} [+] 'https://www.google.com' [+]
              'file,/root/Dekstop/urls.txt' (default: None)
  -t THREAD   Threading. Please use prime numbers. Sample; 3, 5, 7, 11, 13, 17,
              19, 23, 29, 31, 37, 41, 43 (default: 10)
  -d DELAY    Delay (default: 3)
  -f          Use it to find directories and files. The URLs to be found will be
              used to search for vulnerabilities. (default: False)
  -m METHODE  Method: 'all','spider','search' (default: all)
  -q QUERY    it's for to search with google and bing. Please, Use common
              keywords. (default: )
  -c COOKIE   Authenticated Cookie (default: None)
  -v VERBOSE  Verbose (default: False)
  -o OUTPUT   Output file (default: False)

```
> Directory, files and vulnerability finder
```python
┌──(ademcck㉿kali)-[~/Desktop/scac]
└─$ python3 main.py -u https://example.com/ -t 41 -d 5 -f -m all          


                               First request sent.                                
[+] https://example.com/: Fri Dec 17 16:22:09 2021
**********************************************************************************
sending multiple requests..
[+] https://example.com/enterprise/contact?ref_page=/&amp;ref_cta=Contact%20Sales&amp;ref_loc=billboard%20launchpad: Fri Dec 17 16:22:10 2021
[+] https://example.com/enterprise/contact: Fri Dec 17 16:22:11 2021
[+] https://example.com/security: Fri Dec 17 16:22:11 2021
[+] https://example.com/#home-collaborate: Fri Dec 17 16:22:11 2021
[+] https://example.com/features/security: Fri Dec 17 16:22:11 2021
[+] https://example.com/about/careers: Fri Dec 17 16:22:11 2021
[+] https://example.com/github: Fri Dec 17 16:22:11 2021
[+] https://example.com/ohmyzsh/ohmyzsh: Fri Dec 17 16:22:11 2021
[+] https://example.com/customer-stories: Fri Dec 17 16:22:11 2021
[+] https://example.com/jasonetco/octocat-classifier.git: Fri Dec 17 16:22:12 2021
[+] https://example.com/signup?ref_cta=Sign+up&amp;ref_loc=header+logged+out&amp;ref_page=%2F&amp;source=header-home: Fri Dec 17 16:22:12 2021
[+] https://example.com/#home-develop: Fri Dec 17 16:22:12 2021
.
.
.
****************************************************************************************************************************************************
                                                  "Google Search" Testing For site:examle.com
****************************************************************************************************************************************************
[+] https://example.co.il/page?idx=85480: Fri Dec 17 16:25:03 2021
[+] https://example.co.il/schools: Fri Dec 17 16:25:03 2021
[+] https://example.co.il/Games/Game?Idx=596895561: Fri Dec 17 16:25:04 2021
[+] https://example.co.il/Forum/Forum?type=3: Fri Dec 17 16:25:05 2021
.
.
.
****************************************************************************************************************************************************
                                                   "Bing Search" Testing For site:examle.com
****************************************************************************************************************************************************
[+] https://examle.com/cdn-cgi/l/email-protection#f88b8d8888978a8cb8959d918a93919c8bd69b97d69194: Fri Dec 17 16:25:00 2021
[+] https://examle.com/cdn-cgi/l/email-protection#187577737d7c58757d716a73717c6b367b77367174: Fri Dec 17 16:25:00 2021      
.
.
.
****************************************************************************************************************************************************
****************************************************************************************************************************************************
                                                         Testing For https://examle.com/                                                         

+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
                                                                  Testing For lfi                                                                   
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
[+] https://examle.com/?cat=: Fri Dec 17 14:20:48 2021
[+] https://examle.com/content?cat=: Fri Dec 17 14:22:39 2021
[+] https://examle.com/Index.html?cat=: Fri Dec 17 14:26:28 2021
[+] https://examle.com/add_comment.asp?cat=: Fri Dec 17 14:32:00 2021
[+] https://examle.com/test?cat=: Fri Dec 17 14:32:46 2021
[+] https://examle.com/test.html?cat=: Fri Dec 17 14:32:46 2021
[+] https://examle.com/LogIn?cat=: Fri Dec 17 14:39:23 2021
[+] https://examle.com/news?cat=: Fri Dec 17 14:40:46 2021
.
.
.

```

> Result

```python
[+]  http://localhost/DVWA/vulnerabilities/sqli/?id= 'or 1=1
[+]  http://localhost/DVWA/vulnerabilities/sqli/?id= '
5 Seconds sleep
[+]  http://localhost/DVWA/vulnerabilities/sqli/?id= or 1=1
[+]  http://localhost/DVWA/vulnerabilities/sqli/?id= "
[+]  http://localhost/DVWA/vulnerabilities/sqli/?id= '
[+]  http://localhost/DVWA/vulnerabilities/sqli/?id= 'or 1=1
[+]  http://localhost/DVWA/vulnerabilities/sqli/?id= 'or 1=1
[+]  http://localhost/DVWA/vulnerabilities/sqli/?id= or 1=1
[+]  http://localhost/DVWA/vulnerabilities/sqli/?id= '
[+]  http://localhost/DVWA/vulnerabilities/sqli/?id= "
[+]  http://localhost/DVWA/vulnerabilities/sqli/?id= "
[+]  http://localhost/DVWA/vulnerabilities/sqli/?id= or 1=1
```
