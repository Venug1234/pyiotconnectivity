import socket
import json
import sys
import time
import random

port = 13321
s = None

def main():
	try: 
	    s = socket.socket() 
	    print("Socket successfully created")
	except socket.error as err: 
		print("socket creation failed with error %s" %(err))

	try:
		# connect to the server on local computer 
		s.bind(('127.0.0.1', 13321))
		print("socket binding succesful ")
	except:
		pass


	s.listen(1)      
	print("socket is listening")


	# Establish connection with client. 
	c, addr = s.accept()      
	print('Got connection from', addr)

	# a forever loop until we interrupt it or  
	# an error occurs 
	while True:
		print("Creating data to send ")
		dicto = {}
		pointscount = random.randint(1, 10)
		chillerid = random.randint(0,2)

		dicto.update({"devid":chillerid})
		for i in range(pointscount-1):
			key = random.randint(1, 256)
			value = float(random.randint(1, 1000))/10

			dicto.update({key:value})

		print("PRINTING THE DICTO")
		print(dicto)
		 	
		msg = json.dumps(dicto , indent=4, separators=(", ", " : "))
		print(msg)

	   	# send a thank you message to the client.  
	  	c.send(msg)

	  	time.sleep(5) 
	  
   	# Close the connection with the client 
   	c.close() 








if __name__ == '__main__':
	main()
