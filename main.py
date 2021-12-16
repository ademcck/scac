import argparse
from asyncio.runners import run
import validators
from time import sleep
from lib.threadPath import Scac
from lib.fileFinder import ScacDirb
from lib.exploitation import ScacExploitation
from colorama import Fore


class Controller:
    def __init__(self):

        self.pars()
    def pars(self):
        parser = argparse.ArgumentParser(
            exit_on_error=False,
            description='Scanner Tool.',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument("-u", 
                            dest="url",
                            help="""Target urls/hosts,\n 
                                {Examples}\n
                                [+] 'https://www.google.com'\n
                                [+] 'file,/root/Dekstop/urls.txt'\n
                            """)
        parser.add_argument("-t", dest="thread", type=int, default=10, help="Threading. Please use prime numbers. Sample; 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43")
        parser.add_argument("-d", dest="delay", type=int, default=3, help="Delay")
        parser.add_argument("-f", dest="fileFinder",  action='store_true', help="Use it to find directories and files. The URLs to be found will be used to search for vulnerabilities. ")
        parser.add_argument("-m", dest="methode", type=str, default='all', help="Method: 'all','spider','search'")
        parser.add_argument("-q", dest="query", type=str, default='', help="it's for to search with google and bing. Please, Use common keywords.")
        parser.add_argument("-c", dest="cookie", type=str, default=None, help="Authenticated Cookie")
        parser.add_argument("-v", dest="verbose", type=bool , default=False ,help="Verbose")
        parser.add_argument("-o", dest="output", type=str, default=False, help="Output file")
        args = parser.parse_args()
        message = 'Please, Enter the URL or URL list\n'+ Fore.CYAN+'[+]'+Fore.RESET+' Type -h or --help for use'
        if not args.url:
            print(message)
        elif validators.url(args.url) == True:
            # if args.url[-1:len(args.url):1] != "/":
            #     args.url += "/"
            if args.fileFinder:
                self.url = args.url
                self.thread = args.thread
                self.delay = args.delay
                self.fileFinder = args.fileFinder
                self.methode = args.methode
                self.query = args.query
                self.outputFile = args.output
                self.verbose = args.verbose
                self.cookie = args.cookie
                self.fileFinders()
                self.threadPath()
                self.exploitions()

            elif not args.fileFinder:
                self.url = args.url
                self.thread = args.thread
                self.delay = args.delay
                self.outputFile = args.output
                self.verbose = args.verbose
                self.cookie = args.cookie
                self.threadPath()
                self.exploitions()

        elif args.url.split(',')[0].lower() == 'file':
            self.url = self.fileUpload(args.url.split(',')[-1])
            
            if args.fileFinder:
                self.url = args.url
                self.thread = args.thread
                self.delay = args.delay
                self.fileFinder = args.fileFinder
                self.methode = args.methode
                self.query = args.query
                self.outputFile = args.output
                self.verbose = args.verbose
                self.cookie = args.cookie
                self.fileFinders()
                self.threadPath()
                self.exploitions()
            elif not args.fileFinder:
                self.url = args.url
                self.thread = args.thread
                self.delay = args.delay
                self.outputFile = args.output
                self.verbose = args.verbose
                self.cookie = args.cookie
                self.threadPath()
                self.exploitions()
        

    def fileUpload(self,file):
        f = []
        try:
            with open(file,'r') as fL:
                for i in fL.readlines():
                    if validators.url(i): 
                        i = i.rsplit("\n")[0]
                        if i[-1:len(i):1] != "/":
                            i += "/"
                        f.append(i)
            
            return f
        except:
            print(Fore.RED+'[-]'+Fore.CYAN+' Make sure you entered the file path correctly')
            return False

    def fileFinders(self):
        ScacDirb(urls=self.url, thread=self.thread,methode=self.methode,verbose=self.verbose,delay=self.delay,query=self.query)

    def threadPath(self):
        Scac(urls=self.url, thread=self.thread, delay=self.delay, verbose=self.verbose)
    def exploitions(self):
        ScacExploitation(thread=self.thread,delay=self.delay,cookie=self.cookie)

    
if __name__ == '__main__':
    Controller()