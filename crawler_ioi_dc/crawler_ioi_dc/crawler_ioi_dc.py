#-*- coding: utf-8 -*-
import BeautifulSoup
import httplib
import urllib

# http://gall.dcinside.com/board/lists/?id=kimsohye

sohye = "http://gall.dcinside.com/board/lists/?id=kimsohye"
daum = "http://www.daum.net"

if __name__ == "__main__":
	print("Hi DC");

	data = urllib.urlopen(sohye).read()
	print(data)
	f = open("./urldump.txt", "w")
	f.write(data)
	f.close()

#	conn = httplib.HTTPConnection(daum, 8080)
	#conn.request("POST", "/board/lists/?id=kimsohye")
	#conn.request("GET", "/")
#	data = conn.getresponse()#
	#print(data.read())
	#conn.close()
