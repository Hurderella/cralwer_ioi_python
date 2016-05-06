#-*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import httplib, urllib, urllib2
import os, sys
import time
import threading
import Queue


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


class ImgDownloader(threading.Thread):
	def __init__(self, _img_down_info_queue):
		threading.Thread.__init__(self)
		self.img_down_info_queue = _img_down_info_queue

	def run(self):
		while True:
			info = list(self.img_down_info_queue.get())
			print(">>>[0] : " + info[0])
			print(">>>[1] : " + info[1])
			if info[1][12] == u'1':
				info[1] = info[1].replace("http://dcimg1", "http://dcimg2")
			print("path change => %s" % (info[1]))

			try:
				img_req = urllib2.Request(info[1], headers = hdr);
				res = urllib2.urlopen(img_req, timeout = 5000)
			

				ano_i = 1;
				while (os.path.exists(info[0])):
					filename, file_extension = os.path.splitext(info[0])
					anoname = filename + "_" + str(ano_i) + file_extension
					if os.path.exists(anoname) :
						ano_i += 1
					else:
						info[0] = anoname
						break

				print(info[0])
				wif = open(str(info[0]), "wb");
				wif.write(res.read());
				wif.close()
			
			except:
				print("Download url open Except!!!")
				self.img_down_info_queue.put(tuple(info))
				time.sleep(5)
				
			self.img_down_info_queue.task_done()


class ImgDownLinkCrawler(threading.Thread):
	def __init__(self, _page_queue, _img_down_info_queue, destDir):
		threading.Thread.__init__(self)
		self.page_queue = _page_queue
		self.img_down_info_queue = _img_down_info_queue
		self.destDir = destDir
		
	def run(self):
		while True:
			page_num = self.page_queue.get()
			path = "http://gall.dcinside.com/board/view/?id=" + gall_owner + "&no=" + str(page_num)
			
			print("No : " + str(page_num) + "-----------")
			
			print(path)

			try:
				req = urllib2.Request(path, headers = hdr)
				data = urllib2.urlopen(req, timeout = 5000).read()
			except:
				print("Except!!! " + path)
				self.page_queue.queue.put(tuple(info))

			if data == "":
				continue				
				
			name_list = [];
			img_url_list = [];

			try :
				soup = BeautifulSoup(data, 'html.parser');
				for l in soup.find_all('li'):
					if l.get('class') != None and l.get('class')[0] == u'icon_pic' :
						for link in l.contents:
							filename, file_extension = os.path.splitext(link.contents[0])
							if len(file_extension) > 5 or len(file_extension) < 4 :
								raise IndexError
							name = gall_owner + "_IMG_" + str(page_num) + file_extension.encode("euc-kr")
							print(name)
							
							name_list.append(self.destDir + name)
					
				for img in soup.find_all('img'):
					img_link = img.get('src')
					if img.get('alt') != None : 
						continue
					if img_link[0:12] == "http://dcimg":
						img_url_list.append(img_link)

				
			except IndexError as e:
				print("EMPTY NAME ERROR : " + e.message)

			# result check
	
			for i in range(0, len(name_list)):
				print("[%d] : %s" % (i, name_list[i]))
				print("[%d] : %s" % (i, img_url_list[i]))
				self.img_down_info_queue.put((name_list[i], img_url_list[i]))
			
			visit_list.append(page_num)
			vl = open(db_file, "a");
			vl.writelines(page_num + "\n")
			vl.close()
			self.page_queue.task_done()

class WatchGall(threading.Thread):
	def __init__(self, gall_owner, page_func, sleep_count = 10, limit = 0):
		threading.Thread.__init__(self)
		self.gall_owner = gall_owner
		self.page_func = page_func
		self.limit = limit
		self.sleep_count = sleep_count
		self.page = 1

	def run(self):
		loop = 0
		while True:
			self.page = self.page_func(self.page)
			if self.limit < loop:
				print("Approach Limit")
				break;
			loop += 1
			path = "http://gall.dcinside.com/board/lists/?id=" + gall_owner + "&page=" + str(self.page)
	
			print(path)
	
			try:
				req = urllib2.Request(path, headers = hdr)
				data = urllib2.urlopen(req, timeout = 5000).read()
				
				if data == "":
					return False				
	
				soup = BeautifulSoup(data, 'html.parser');
				for td in soup.find_all('td'):
					if td.get('class')[0] == 't_notice' and td.contents[0] != "공지":
						if not td.contents[0] in visit_list :
							img_page_num = td.contents[0]
							img_page_queue.put(img_page_num)
							print(img_page_num)
				
			except:
				print("Except!!! " + path)
			finally:
				time.sleep(self.sleep_count)
			

visit_list = []
img_page_queue = Queue.Queue()
img_down_info_queue = Queue.Queue()
db_file = "./visit_db.txt"

if __name__ == "__main__":
	print("Hi DC");
	reload(sys)
	sys.setdefaultencoding('utf-8')

	argv = sys.argv

	gall_owner = "kimsohye"#"youjung"#argv[1]#"chungha" 
	#sys.stdout = Logger(gall_owner + "_log.txt")
	
	dirname = "./sohye_que/"
	if not os.path.exists(dirname):
			os.mkdir(dirname)

	#download check
	
	if os.path.exists(db_file):
		vl = open(db_file, "r");
		for l in vl.readlines():
			visit_list.append(l.rstrip())
		vl.close()


	page1_watch_dog = WatchGall(gall_owner, lambda x: 1, sleep_count = 60, limit = 3)
	page1_watch_dog.setDaemon(True)
	page1_watch_dog.start()

	page_all_watch_dog = WatchGall(gall_owner, lambda x: x + 1, limit = 10)
	page_all_watch_dog.setDaemon(True)
	page_all_watch_dog.start()

	imgDownLinkTh = ImgDownLinkCrawler(img_page_queue, img_down_info_queue, dirname)
	imgDownLinkTh.setDaemon(True)
	imgDownLinkTh.start()
	
	imgDownTh = ImgDownloader(img_down_info_queue)
	imgDownTh.setDaemon(True)
	imgDownTh.start()
			
	page1_watch_dog.join()
	page_all_watch_dog.join()
	imgDownLinkTh.page_queue.join()
	imgDownTh.img_down_info_queue.join()


























