#-*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import httplib, urllib, urllib2
import os, sys
import time
import threading


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
	data = ""
	for attemp in range(try_count):
		try:
			data = urllib2.urlopen(req, timeout = timeout)
		except:
			print(err_log)
			time.sleep(5)
			continue
		break;
	return data

def img_link_crawler(no, path, destDir):
	#path = base_path + gall_owner + "&no=" + str(no)
		
	print("No : " + str(no) + "-----------")
		
	req = urllib2.Request(path, headers = hdr)

	#crawler 
	print(path)
	data = urlopen_try(req, timeout = 10000, err_log = "Except!!! " + path).read()
	if data == "":
		return False				
				
	name_list = [];
	img_url_list = [];

	soup = BeautifulSoup(data, 'html.parser');
	for l in soup.find_all('li'):
		if l.get('class') != None and l.get('class')[0] == u'icon_pic' :
			for link in l.contents:
					
				filename, file_extension = os.path.splitext(link.contents[0])
				name = gall_owner + "_IMG_" + str(no) + file_extension
				print(name)
					
				name_list.append(destDir + name)
					

	for img in soup.find_all('img'):
		img_link = img.get('src')
		if img.get('alt') != None : 
			continue
		if img_link[0:12] == "http://dcimg":
			img_url_list.append(img_link)

	# result check
	
	for i in range(0, len(name_list)):
		print("[%d] : %s" % (i, name_list[i]))
		print("[%d] : %s" % (i, img_url_list[i]))

				
	## down load
	#for i in range(0, len(name_list)):
	#	print("path :: " + img_url_list[i])
	#	if img_url_list[i][12] == u'1':
	#		img_url_list[i] = img_url_list[i].replace("http://dcimg1", "http://dcimg2")
	#		print("path change => %s" % (img_url_list[i]))
			
	#	img_req = urllib2.Request(img_url_list[i], headers = hdr);
	#	res = urlopen_try(img_req, timeout = 5000, err_log = "Download url open Except!!!")
	#	if res == "" :
	#		continue

	#	ano_i = 1;
	#	while (os.path.exists(name_list[i])):
	#		filename, file_extension = os.path.splitext(name_list[i])
	#		anoname = filename + "_" + str(ano_i) + file_extension
	#		if os.path.exists(anoname) :
	#			ano_i += 1
	#		else:
	#			name_list[i] = anoname
	#			break;

	#	print(name_list[i])
	#	wif = open(name_list[i], "wb");
	#	wif.write(res.read());
	#	wif.close()
	#	time.sleep(1)
	#time.sleep(1)

def first_img_link(gall_owner):
	
	path = "http://gall.dcinside.com/board/view/?id=" + gall_owner + "&page=1"
	
	req = urllib2.Request(path, headers = hdr)
	print(path)
	
	data = urlopen_try(req, timeout = 10000, err_log = "Except!!! " + path).read()
	if data == "":
		return False				
	
	soup = BeautifulSoup(data, 'html.parser');
	for td in soup.find_all('td'):
		if td.get('class')[0] == 't_notice' and td.contents[0] != "공지":
			print(td.contents[0])
			

	#for l in soup.find_all('li'):
	#	if l.get('class') != None and l.get('class')[0] == u'icon_pic' :
visit_list = []
if __name__ == "__main__":
	print("Hi DC");
	reload(sys)
	sys.setdefaultencoding('utf-8')

	argv = sys.argv

	gall_owner = "youjung"#argv[1]#"chungha" 
	sys.stdout = Logger(gall_owner + "_log.txt")
	
	#vl = open("./visit_db", r);
	#for l in vl.readlines():
	#	visit_list.append(l)
	#vl.close()
	first_img_link(gall_owner)
	
	#img_link_crawler(148345, "http://gall.dcinside.com/board/view/?id=youjung&no=148345", "./youjung/")

	#dirname = "./youjung_img/"#argv[4]
	#if not os.path.exists(dirname):
	#		os.mkdir(dirname)

	#for no in range(int(argv[2]), int(argv[3])):
		
		#path = base_path + gall_owner + "&no=" + str(no)
		
		#print("No : " + str(no) + "-----------")
		
		#req = urllib2.Request(path, headers = hdr)

		#print(path)
		#data = urlopen_try(req, timeout = 10000, err_log = "Except!!! " + path).read()
		#if data == "":
		#	continue							
		#name_list = [];
		#img_url_list = [];

		#soup = BeautifulSoup(data, 'html.parser');
		#for l in soup.find_all('li'):
		#	if l.get('class') != None and l.get('class')[0] == u'icon_pic' :
		#		for link in l.contents:
					
		#			filename, file_extension = os.path.splitext(link.contents[0])
		#			name = gall_owner + "_IMG_" + str(no) + file_extension
		#			print(name)
					
		#			name_list.append(dirname + name)
					

		#for img in soup.find_all('img'):
		#	img_link = img.get('src')
		#	if img.get('alt') != None : 
		#		continue
		#	if img_link[0:12] == "http://dcimg":
		#		img_url_list.append(img_link)
				

		#for i in range(0, len(name_list)):
		#	print("path :: " + img_url_list[i])
		#	if img_url_list[i][12] == u'1':
		#		img_url_list[i] = img_url_list[i].replace("http://dcimg1", "http://dcimg2")
		#		print("path change => %s" % (img_url_list[i]))
			
		#	img_req = urllib2.Request(img_url_list[i], headers = hdr);
		#	res = urlopen_try(img_req, timeout = 5000, err_log = "Download url open Except!!!")
		#	if res == "" :
		#		continue

		#	ano_i = 1;
		#	while (os.path.exists(name_list[i])):
		#		filename, file_extension = os.path.splitext(name_list[i])
		#		anoname = filename + "_" + str(ano_i) + file_extension
		#		if os.path.exists(anoname) :
		#			ano_i += 1
		#		else:
		#			name_list[i] = anoname
		#			break;

		#	print(name_list[i])
		#	wif = open(name_list[i], "wb");
		#	wif.write(res.read());
		#	wif.close()
		#	time.sleep(1)
		#time.sleep(1)
		

	#img_db_file.close()