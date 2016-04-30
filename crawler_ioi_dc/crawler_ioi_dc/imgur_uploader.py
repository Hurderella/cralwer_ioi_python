from imgurpython import ImgurClient
import urllib2
import os
import json

client_id = '...........'
client_secret = '...........'
x_mash_key = "..........."

def img_upload(_access_token, _refresh_token):

	client = ImgurClient(client_id, client_secret)
	client.set_user_auth(_access_token, _refresh_token)
	client.mashape_key = x_mash_key

	conf = {"album" : "JtebE",
		 "description": "Hello World",
		 "title" : "Hi"}
	res = client.upload_from_path("./image_1_2.gif", config = conf, anon = False)
	print(res)
	print(res["link"])


def main():
	
	if not os.path.exists("./token.txt"):
		print("Need Token File. Run make_credential.py")

	token_file = open("./token.txt", "r")
	access = token_file.readline().strip().split(" : ")[1]
	refresh = token_file.readline().strip().split(" : ")[1]
	token_file.close()
	
	print(access)
	print(refresh)

	img_upload(access, refresh)


if __name__ == "__main__":
	
	main()
	