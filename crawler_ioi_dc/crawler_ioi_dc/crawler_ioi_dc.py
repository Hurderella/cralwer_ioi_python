#-*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from imgurpython import ImgurClient
import imgur_uploader
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
	def __init__(self, _img_down_info_queue, _img_upload_queue):
		threading.Thread.__init__(self)
		self.img_down_info_queue = _img_down_info_queue
		self.img_up_queue = _img_upload_queue

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

				save_list = open(save_path, "a")
				save_list.writelines(str(info[0]) + "\n")
				save_list.close()

				self.img_up_queue.put(str(info[0]))
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
					
			#path = "http://gall.dcinside.com/board/view/?id=" + gall_owner + "&no=" + str(page_num)
			path = "http://gall.dcinside.com/mgallery/board/view/?id=" + gall_owner + "&no=" + str(page_num)	
			print("No : " + str(page_num) + "-----------")
			
			print(path)

			try:
				req = urllib2.Request(path, headers = hdr)
				data = urllib2.urlopen(req, timeout = 5000).read()
				#time.sleep(100)
			except:
				print("Except!!! " + path)
				self.page_queue.task_done()
				self.page_queue.put(page_num)
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
			min = len(name_list) if len(name_list) < len(img_url_list) else len(img_url_list)
			for i in range(0, min):
				print("[%d] : %s" % (i, name_list[i]))
				print("[%d] : %s" % (i, img_url_list[i]))
				self.img_down_info_queue.put((name_list[i], img_url_list[i]))
			
			visit_list.append(page_num)
			vl = open(db_file, "a");
			vl.writelines(page_num + "\n")
			vl.close()
			self.page_queue.task_done()

class WatchGall(threading.Thread):
	def __init__(self, gall_owner, page_func, start_page = 1, sleep_count = 5, limit = 0):
		threading.Thread.__init__(self)
		self.gall_owner = gall_owner
		self.page_func = page_func
		self.limit = limit
		self.sleep_count = sleep_count
		self.page = start_page
		
	def run(self):
		loop = 0
		while True:
			self.page = self.page_func(self.page)
			if self.limit != 0 and self.limit < loop:
				print("Approach Limit")
				break;
			loop += 1
			
			#http://gall.dcinside.com/board/lists/?id=youjung
			path = "http://gall.dcinside.com/mgallery/board/lists/?id=" + gall_owner + "&page=" + str(self.page)
	
			print(path)
	
			try:
				req = urllib2.Request(path, headers = hdr)
				data = urllib2.urlopen(req, timeout = 5000).read()
				
				if data == "":
					print("false urlopen")
					return False				
				soup = BeautifulSoup(data, 'html.parser');
	
				for tr in soup.find_all('tr', {'onmouseover':"this.style.backgroundColor='#eae9f7'"}):
					for td in tr.find_all('td'):
						if td.get('class')[0] == 't_notice' and td.contents[0] == "공지":
							break
						elif td.get('class')[0] == 't_subject' :
							link = td.contents[0].get('href')
							img_page_num = link.split('&no=')[1].split('&page')[0]
							if not img_page_num in visit_list:
								img_page_queue.put(img_page_num)
								print(img_page_num)

			except:
				print("Except!!! " + path)
			finally:
				time.sleep(self.sleep_count)
			
class ImgUploader(threading.Thread):
	def __init__(self, _img_upload_queue, _album_id):
		threading.Thread.__init__(self)
		self.img_upload_queue = _img_upload_queue
		self.upload_album_id = _album_id

		complete_list = []
		if os.path.exists(complete_path):
			complete_list_file = open(complete_path, "r")
			for l in complete_list_file.readlines():
				complete_list.append(l.rsplit()[0])

			complete_list_file.close()

		if os.path.exists(save_path):
			save_list_file = open(save_path, "r")
			#for l in save_list_file.readlines():
			#	if not l in complete_list : 
			#		self.img_upload_queue.put(l.rsplit()[0])

			save_list_file.close()
		
		_access_token, _refresh_token = imgur_uploader.get_access_token()
		print(_access_token)
		print(_refresh_token)
		
		self.client = imgur_uploader.ImgurClient(imgur_uploader.client_id, imgur_uploader.client_secret)
		self.client.set_user_auth(_access_token, _refresh_token)
		self.client.mashape_key = imgur_uploader.x_mash_key

	def run(self):
		while True:
			upload_file_path = self.img_upload_queue.get()
			print(">" + upload_file_path)

			x_mash_info = imgur_uploader.get_x_mash_limit(self.client)
			remain = int(x_mash_info[0])
			print("upload remain : " + str(remain))
			if remain < 2:
				break

			filename, file_ext = os.path.splitext(upload_file_path)
			if file_ext == '.GIF' or file_ext == '.gif':
				print("!!! " + filename + "+" + file_ext)
				filename = os.path.basename(upload_file_path)
				imgur_uploader.img_upload(self.client, upload_file_path, self.upload_album_id, filename)

				complete_list_file = open(complete_path, "a")
				complete_list_file.writelines(upload_file_path + "\n")
				complete_list_file.close()

			self.img_upload_queue.task_done()


visit_list = []
img_page_queue = Queue.Queue()
img_down_info_queue = Queue.Queue()
img_upload_queue = Queue.Queue()
db_file = "./visit_db.txt"
save_path = "./save_list.txt"
complete_path = "./complete_list.txt"
album_id = "QLUdt" #"oXvZ7"

if __name__ == "__main__":
	print("Hi DC");
	reload(sys)
	sys.setdefaultencoding('utf-8')

	argv = sys.argv
	#youjung album : oXvZ7
	gall_owner = "chungha"#argv[1]#"chungha" 
	#sys.stdout = Logger(gall_owner + "_log.txt")
	
	dirname = "./chungha_que/"
	if not os.path.exists(dirname):
			os.mkdir(dirname)

	#download check
	
	if os.path.exists(db_file):
		vl = open(db_file, "r");
		for l in vl.readlines():
			visit_list.append(l.rstrip())
		vl.close()
#print(visit_list)

	page1_watch_dog = WatchGall(gall_owner, lambda x: 1, sleep_count = 10)
	page1_watch_dog.setDaemon(True)
	page1_watch_dog.start()

	page_all_watch_dog = WatchGall(gall_owner, lambda x: x + 1, start_page = 1, limit = 20000)
	page_all_watch_dog.setDaemon(True)
	page_all_watch_dog.start()

	imgDownLinkTh = ImgDownLinkCrawler(img_page_queue, img_down_info_queue, dirname)
	imgDownLinkTh.setDaemon(True)
	imgDownLinkTh.start()
	
	imgDownTh = ImgDownloader(img_down_info_queue, img_upload_queue)
	imgDownTh.setDaemon(True)
	imgDownTh.start()

	imgUpTh = ImgUploader(img_upload_queue, album_id)
	imgUpTh.setDaemon(True)
	imgUpTh.start()


	# imgUpTh.img_upload_queue.join()
	imgUpTh.join()
	print("imgUpTh Join")
	sys.exit(2)

	page1_watch_dog.join()
	page_all_watch_dog.join()
	imgDownLinkTh.page_queue.join()
	imgDownTh.img_down_info_queue.join()
	

























