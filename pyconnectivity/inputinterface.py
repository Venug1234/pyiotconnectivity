import socket
import sys
import time


# default port for socket 
port = 13321

def init():
	global s
	try: 
	    s = socket.socket() 
	    print "Socket successfully created"
	except socket.error as err: 
		print("socket creation failed with error %s" %(err))

	while True:
		try:
			# connect to the server on local computer 
			s.connect(('127.0.0.1', 13321))
			break;
		except:
			time.sleep (2)
			print("Retrying socket connection")


def readdata():
	#global s
	# receive data from the server (in json format)
	data=s.recv(1024)
	return data


def close():
	s.close()
	