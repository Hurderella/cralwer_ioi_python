#-*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import httplib
import urllib
import urllib2
import os
import sys
import time

#
# http://gall.dcinside.com/board/lists/?id=kimsohye
# http://gall.dcinside.com/board/view/?id=kimsohye&no=75905 #&page=1
# http://gall.dcinside.com/board/view/?id=kimsohye&no=75906 error page. occur redirection  #&page=1

sohye = "http://gall.dcinside.com/board/view/?id=kimsohye"
sohye_normal = "http://gall.dcinside.com/board/view/?id=kimsohye&no=76800"
sohye_err = "http://gall.dcinside.com/board/view/?id=kimsohye&no=75906"
sohye_empty_image = "http://gall.dcinside.com/board/view/?id=kimsohye&no=76799"

chungha = "http://gall.dcinside.com/board/view/?id=chungha"

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
					'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
					'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
					'Accept-Encoding': 'none',
					'Accept-Language': 'en-US,en;q=0.8',
					'Connection': 'keep-alive'}

class Logger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

if __name__ == "__main__":
	print("Hi DC");
	reload(sys)
	sys.setdefaultencoding('utf-8')
	sys.stdout = Logger("chungha_log.txt")
	#sys.stdout = Logger("log.txt")			
	
	img_db_file = open("./chungha_db.txt", 'a')

	for no in range(500, 500):
		dirname = "D:\\ioi_chungha\\"	
		path = chungha + "&no=" + str(no)
		#dirname = "D:\\ioi_sohye\\"
		#path = sohye + "&no=" + str(no)
		print("No : " + str(no) + "-----------")
		
		req = urllib2.Request(path, headers = hdr)

		print(path)
		for attempt in range(10):
			try:
				data = urllib2.urlopen(req, timeout = 5000).read()
			except:
				print("Except!!! " + path)
				continue
			break
											
		name_list = [];
		img_url_list = [];

		soup = BeautifulSoup(data, 'html.parser');
		for l in soup.find_all('li'):
			if l.get('class') != None and l.get('class')[0] == u'icon_pic' :
				for link in l.contents:
					name = link.contents[0]
					try :
						print(name)
					except:
						print("name error");
						filename, file_extension = os.path.splitext(name)
						name = "_____err" + str(no) + file_extension

					name_list.append(dirname + name)
					

		for img in soup.find_all('img'):
			img_link = img.get('src')
			if img.get('alt') != None : 
				continue
			if img_link[0:12] == "http://dcimg":
				img_url_list.append(img_link)
				

		for i in range(0, len(name_list)):
			print("path :: " + img_url_list[i])
			if img_url_list[i][12] == u'1':
				img_url_list[i] = img_url_list[i].replace("http://dcimg1", "http://dcimg2")
				print("path change => %s" % (img_url_list[i]))
			img_db_file.write(img_url_list[i] + "\n")	
				
		#	img_req = urllib2.Request(img_url_list[i], headers = hdr);
		#	#try:
		#	res = urllib2.urlopen(img_req, timeout = 5000)
			
		#	ano_i = 1;
		#	while(os.path.exists(name_list[i])):
		#		filename, file_extension = os.path.splitext(name_list[i])
		#		anoname = filename + "_" + str(ano_i) + file_extension
		#		ano_i += 1
		#		name_list[i] = anoname
		#	print(name_list[i])
		#	wif = open(name_list[i], "wb");
		#	wif.write(res.read());
		#	wif.close()
		#	time.sleep(1)
		#time.sleep(1)
		

	img_db_file.close()