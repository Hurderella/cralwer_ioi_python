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

base_path = "http://gall.dcinside.com/board/view/?id="

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

def urlopen_try(req, timeout, try_count = 10, err_log = "Occur Exception") :
	for attemp in range(try_count):
		try:
			data = urllib2.urlopen(req, timeout = timeout)
		except:
			print(err_log)
			continue
		break;
	return data


if __name__ == "__main__":
	print("Hi DC");
	reload(sys)
	sys.setdefaultencoding('utf-8')
	gall_owner = sys.argv[1]#"chungha" 
	sys.stdout = Logger(gall_owner + "_log.txt")
	
	dirname = "./" + gall_owner + "/"
	if not os.path.exists(dirname):
		os.mkdir(dirname)

	#for no in range(1244, 1245): #917 occur error
	for no in range(sys.argv[2], sys.argv[3]):
		
		path = base_path + gall_owner + "&no=" + str(no)
		
		print("No : " + str(no) + "-----------")
		
		req = urllib2.Request(path, headers = hdr)

		print(path)
		data = urlopen_try(req, timeout = 5000, err_log = "Except!!! " + path).read()
													
		name_list = [];
		img_url_list = [];

		soup = BeautifulSoup(data, 'html.parser');
		for l in soup.find_all('li'):
			if l.get('class') != None and l.get('class')[0] == u'icon_pic' :
				for link in l.contents:
					try :
						name = link.contents[0]
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
			
			img_req = urllib2.Request(img_url_list[i], headers = hdr);
			res = urlopen_try(img_req, timeout = 5000, err_log = "Download url open Except!!!")
								
			ano_i = 1;
			while (os.path.exists(name_list[i])):
				filename, file_extension = os.path.splitext(name_list[i])
				anoname = filename + "_" + str(ano_i) + file_extension
				if os.path.exists(anoname) :
					ano_i += 1
				else:
					name_list[i] = anoname
					break;

			print(name_list[i])
			wif = open(name_list[i], "wb");
			wif.write(res.read());
			wif.close()
			time.sleep(1)
		time.sleep(1)
		

	#img_db_file.close()