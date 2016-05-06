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

#def urlopen_try(req, timeout, requeue, err_log = "Occur Exception") :
#	data = ""
#	try:
#		data = urllib2.urlopen(req, timeout = timeout)
#	except:
#		print(err_log)
#		requeue.put(req)
#		time.sleep(5)
		
	
#	return data


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
				continue

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
			

			#crawler 
			print(path)
			#data = urlopen_try(req, timeout = 10000, self.page_queue,
			#					err_log = "Except!!! " + path).read()
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
							name = gall_owner + "_IMG_" + str(page_num) + file_extension.encode("euc-kr")
							print(name)
							
							name_list.append(self.destDir + name)
					
				for img in soup.find_all('img'):
					img_link = img.get('src')
					if img.get('alt') != None : 
						continue
					if img_link[0:12] == "http://dcimg":
						img_url_list.append(img_link)

				visit_list.append(page_num)
			except IndexError as e:
				print("EMPTY NAME ERROR : " + e.message)

			# result check
	
			for i in range(0, len(name_list)):
				print("[%d] : %s" % (i, name_list[i]))
				print("[%d] : %s" % (i, img_url_list[i]))
				self.img_down_info_queue.put((name_list[i], img_url_list[i]))

			self.page_queue.task_done()

class WatchGall(threading.Thread):
	def __init__(self, gall_owner, page_func):
		threading.Thread.__init__(self)
		self.gall_owner = gall_owner
		self.page_func = page_func
	
	def run(self):
		page = 1
		page = self.page_func(page)
		while True:
			
			path = "http://gall.dcinside.com/board/view/?id=" + gall_owner + "&page=" + str(page)
	
			print(path)
	
			#data = urlopen_try(req, timeout = 10000, err_log = "Except!!! " + path).read()
			try:
				req = urllib2.Request(path, headers = hdr)
				data = urllib2.urlopen(req, timeout = 5000).read()
				#self.img_down_info.queue.put(tuple(info))

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
				time.sleep(10)
			break;

visit_list = []
img_page_queue = Queue.Queue()
img_down_info_queue = Queue.Queue()

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

	#vl = open("./visit_db", r);
	#for l in vl.readlines():
	#	visit_list.append(l)
	#vl.close()
	
	#page1st_craw_th = threading.Thread(target = page1st_crawler, args = (gall_owner, ))
	#page1st_craw_th.setDaemon(True)
	#page1st_craw_th.start()

	#page1_watch_dog = WatchGall(gall_owner, lambda x: 1)
	#page1_watch_dog.setDaemon(True)
	#page1_watch_dog.start()

	page_all_watch_dog = WatchGall(gall_owner, lambda x: x + 1)
	page_all_watch_dog.setDaemon(True)
	page_all_watch_dog.start()

	imgDownLinkTh = ImgDownLinkCrawler(img_page_queue, img_down_info_queue, dirname)
	imgDownLinkTh.setDaemon(True)
	imgDownLinkTh.start()
	
	imgDownTh = ImgDownloader(img_down_info_queue)
	imgDownTh.setDaemon(True)
	imgDownTh.start()
			
	#page1_watch_dog.join()
	page_all_watch_dog.join()
	imgDownLinkTh.page_queue.join()
	imgDownTh.img_down_info_queue.join()


























