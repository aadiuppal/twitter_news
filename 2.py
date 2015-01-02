import urllib
import urllib2
import sys
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import re
from random import randint
import time


def makeurl(query):
	return "http://news.google.com/news?pz=1&cf=all&ned=us&hl=en&q="+query+"&output=rss"

def fetchcontent(url):
	page=urllib2.urlopen(url)
	content=page.read()
	return content

def savecontent(content):
	file=open("news.xml","w")
	file.write(content)
	file.close()


def startserver():
	HandlerClass = SimpleHTTPRequestHandler
	ServerClass  = BaseHTTPServer.HTTPServer
	Protocol     = "HTTP/1.0"

	if sys.argv[1:]:
	    port = int(sys.argv[1])
	else:
	    port = 8000
	server_address = ('192.168.1.149', port)
	
	HandlerClass.protocol_version = Protocol
	httpd = ServerClass(server_address, HandlerClass)
	
	sa = httpd.socket.getsockname()
	print "Serving HTTP on", sa[0], "port", sa[1], "..."
	httpd.serve_forever()


def findtrend(num):
	t_page=urllib2.urlopen("http://trends24.in/united-states/~cloud")
	t_content=t_page.read()
#	pattern="Twitter trend tag-cloud for Worldwide- "+"(.*)"+","
	pattern="Twitter trend tag-cloud for United States- "+"(.*)"+","
	m=re.search(pattern,t_content)
#	print m
#	print m.group()
	string = m.group()
	splitted=string.split()
	print splitted[6]
	q1=process(splitted[6])
	print q1
	q=[]
	if num <= 1 :
		return q1
	else :
		for i in range(0,num):
			q.append(process(splitted[6+i]))
		print "+".join(q)
		return "+".join(q)
#	print m.group(1)
#	print m
#	return m


def process(s):
	length=len(s)
	if s[0] == '#':
		if s[length-1] == ',' or s[length-1] == '.':
			return s[1:length-1]
		else :
			return s[1:]
	else :
		if s[length-1] == ','or s[length-1] == '.':
			return s[:length-1]
		else:
			return s
	
if __name__ == "__main__":
	
	
#	startserver()
	while (True):
		print "fetching NOW"
		num=randint(1,3)
		query=findtrend(num)
		url=makeurl(query)
		content=fetchcontent(url)
		savecontent(content)
		time.sleep(5)
#	num=randint(1,3)
#	q=findtrend(num)
#	startserver()
