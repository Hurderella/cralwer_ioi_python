from imgurpython import ImgurClient
import urllib2
import os
import json
import sys
import getopt

client_id = '.............'
client_secret = '.................'
x_mash_key = "..........."

def img_upload(client, img_path, 
			   album_id, 
			   title = "Hi", 
			   description = "Hello World", 
			   dump_path = "./dump.txt"):
		
	conf = {"album" : album_id,
		 "description": description,
		 "title" : title}
	
	res = client.upload_from_path(img_path, config = conf, anon = False)
	d = open(dump_path, "a")
	if res != None:
		d.writelines(str(res) + "\n")
	else:
		conf["img_path"] = img_path
		d.writelines("NONE : " + str(conf) + "\n") 
	d.close()
	return res

def get_album_id(client, user, album_name):
	
	res = client.get_account_album_ids(user)
	
	for album_id in res:
		req_url = "https://imgur-apiv3.p.mashape.com/3/account/%s/album/%s" % (user, album_id)
		req = urllib2.Request(req_url, headers ={
				"X-Mashape-Key" : x_mash_key,
				"Authorization" : "Bearer " + client.auth.get_current_access_token(),
				"Accept": "application/json"
			})
		res_data = urllib2.urlopen(req, timeout = 2000)
		res_json = json.loads(res_data.read())
		if res_json["data"]["title"] == album_name:
			return album_id
	

def get_access_token():
	
	if not os.path.exists("./token.txt"):
		print("Need Token File. Run make_credential.py")
		sys.exit(2)

	token_file = open("./token.txt", "r")
	access = token_file.readline().strip().split(" : ")[1]
	refresh = token_file.readline().strip().split(" : ")[1]
	token_file.close()
	
	return access, refresh

def main(argv):

	img_source = argv["source"] + "/" #"./sohye_img/"
	
	name_list = []
	img_oriUrl_list = []
	board_url = ""
	count = 1
	name_flag = False

	#img_upload(access, refresh)

	_access_token, _refresh_token = get_access_token()
	client = ImgurClient(client_id, client_secret)
	client.set_user_auth(_access_token, _refresh_token)
	client.mashape_key = x_mash_key
	
	album_id = get_album_id(client, argv["user"], argv["album"])
	if album_id == "" and album_id == None:
		print("Need Valid Album Name")
		sys.exit(2)

	log_file = open(argv["inlog"], "r")
	#log_file = open("./test_case.txt", "r")
	
	log = log_file.readlines()
	for line in log:
		if line[0:2] == "No":
			if len(name_list) > 0:
				
				print(board_url)
				for i in range(len(name_list)):
					print("upload name : " + name_list[i])
					print("upload img ori : " + img_oriUrl_list[i])
					res = img_upload(client, 
								img_source + name_list[i], 
								album_id,
								name_list[i],
								board_url,
								argv["dump"])
					print("------------------")
				name_list = []
				img_oriUrl_list =[]
				board_url = ""
			
			count += 1
			if count > int(argv["end"]):
				break
		elif line[0:11] == "http://gall":
			board_url = line
		elif line[0:7] == "path ::":
			img_oriUrl_list.append(line.split(" :: ")[1])
			name_flag = True
		elif line[0:7] == "path ch":
			img_oriUrl_list.pop()
			img_oriUrl_list.append(line.split(" => ")[1])
		elif name_flag :
			filename = os.path.basename(line).rsplit("\n")[0].encode('euc-kr')
			name_list.append(filename)
			name_flag = False
	
	for i in range(len(name_list)):
		print("upload name : " + name_list[i])
		print("upload img ori : " + img_oriUrl_list[i])
		img_upload(client, 
					img_source + name_list[i], 
					album_id,
					name_list[i],
					board_url,
					argv["dump"])
		print("------------------")
		
	log_file.close()
	
if __name__ == "__main__":
	reload(sys)
	sys.setdefaultencoding('utf-8')

	try:
		argv = dict()
		opts, args = getopt.getopt(sys.argv[1:], 
									"hi:d:e:a:u:s:", 
									["inlog=", "dump=", 
									"end=", "album=", 
									"user=", "source="])
		for opt, arg in opts:
			if opt in ("-h", "--help"):
				print("--inlog=[parsing file]") 
				print("--dump=[dump file]")
				print("--end=[parsing end]")
				print("--album=[upload album]")
				print("--user=[user id]")
				print("--source=[source dir]")
				sys.exit(0)
			elif opt in ("-i", "--inlog"):
				argv["inlog"] = arg
			elif opt in ("-d", "--dump"):
				argv["dump"] = arg
			elif opt in("-e", "--end"):
				argv["end"] = arg
			elif opt in("-a", "--album"):
				argv["album"] = arg
			elif opt in("-u", "--user"):
				argv["user"] = arg
			elif opt in("-s", "--source"):
				argv["source"] = arg
		
		if len(argv) < 6:
			raise getopt.GetoptError("Few Argument")
		
		main(argv)
	except getopt.GetoptError as ge:
		print("Need Valid Argument : " + ge.msg);
	
	
	