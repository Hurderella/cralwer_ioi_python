from imgurpython import ImgurClient
import urllib2
import sys
import getopt


def main(argv):
	
	client_id = '7bd202e0f6253f8'
	client_secret = 'e8d018d24bf8e44d598f146c4b5a84e90cfb8c36'
	pin = ""

	client = ImgurClient(client_id, client_secret)
	authorization_url = client.get_auth_url('pin')
	usage = "usage : make_credentials.py -p <pin number>"
	usage += "\nauthorization url : \n\t" + authorization_url
	
	try:
		opts, args = getopt.getopt(argv, "hp:", ["--pin="])
		
		for opt, arg in opts:
			if opt == "-h":
				print(usage)
				sys.exit(2)
			elif opt in ("-p", "--pin="):
				pin = arg
		
		credentials = client.authorize(pin, 'pin')
		access_token = "access : " + credentials['access_token']
		refresh_token = "refres : " + credentials['refresh_token']
		print(access_token)
		print(refresh_token)
		keys = open("./token.txt", "w")
		keys.write(access_token + "\r\n")
		keys.write(refresh_token)
		keys.close()
	except getopt.GetoptError:
		print(usage)
	
		
		

if __name__ == "__main__":
	try:
		main(sys.argv[1:])
	except:
		print("type : make_credentials.py -h")