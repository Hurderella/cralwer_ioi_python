from imgurpython import ImgurClient
import urllib2
import sys
import getopt

def main(argv):
	usage = "usage : make_credentials.py -p <pin number>"
	pin = 0
	try:
		opts, args = getopt.getopt(argv, "hp:", ["--pin="])
		
		for opt, arg in opts:
			if opt == "-h":
				print(usage)
			elif opt in ("-p", "--pin="):
				pin = int(arg)
	except getopt.GetoptError:
		print(usage)
	except ValueError as ve:
		print(usage)
		print("error : " + ve.message)
		
		

if __name__ == "__main__":
	main(sys.argv[1:])