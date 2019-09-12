import runtimedb
import telemetry
import cov
import alarm
import iotclient
import inputinterface
import jsonwrapper
import deviceprovision
import time
from pubsub import pub
import random

def main():

	# initialize the runtime database
	runtimedb.runtimedatabaseinit()

	# initialize the input channel
	inputinterface.init()

	# initialize the device provisioning in provisioning server
	deviceprovision.init()

	# initialize iot connection
	iotclient.iotconnection_init()

	# initialize the data consumers
	telemetry.init()
	cov.init()
	alarm.init()


	print("******************** changing values ")
	while True:
		data = inputinterface.readdata()

		if len(data) != 0:
			dicto = jsonwrapper.converttoobj(data)
			chillerid = dicto.get("devid")

			#remove the "devid" key entry from the dictionary as its not useful further
			dicto.pop("devid")

			keys = dicto.keys()
			
			values = dicto.values()
			#print("device %d, key %s, values are :%s" % (chillerid, keys, values))
			count = len(keys)

			for i in range(count - 1):
				flag = False
				#print(keys[i], chillerid)
				key = int(keys[i])
				iotkey = runtimedb.getiotkey(chillerid, key)

				if iotkey == None:
					continue
					
				#print("found valid iotkey%d from key%d" % (iotkey, key))

				# #check data point configuration
				if runtimedb.istelemetry(chillerid , iotkey):
					#print("posintg telemetry ", iotkey, values[i])
					pub.sendMessage('telemetry', curvalue=[chillerid, iotkey, values[i]])

				#check data point configuration
				if runtimedb.isalarm(chillerid ,iotkey):
					flag = True
					#print("posting alarm ", iotkey, values[i])
					pub.sendMessage('alarm', curvalue=[chillerid, iotkey, values[i]], epochtime=long(time.time()))

				#check data point configuration
				if runtimedb.iscov(chillerid , iotkey) and flag == False :
					print("cov ", iotkey, values[i])
					pub.sendMessage('cov', curvalue=[chillerid, iotkey, values[i]], epochtime=long(time.time()))

		time.sleep(1)

	# registeralarm()
	# registercov()

	# initialize the 




	# monitor iot connection status

'''
	database.opendatabase()

	print("************readallaliasnames**************")
	database.readallaliasnames()
	print("**************readalarmpoints************")
	database.readalarmpoints()
	print("****************readcovpoints**********")
	database.readcovpoints()
	print("*************readtelmetrypoints*************")
	database.readtelmetrypoints()
	print("*************readtelmetrycovpoints*************")
	database.readtelmetrycovpoints()
	print("**************readtelemetryperiodicity************")
	database.readtelemetryperiodicity()
	print("**************readtelemetrypiontscount************")
	database.readtelemetrypiontscount()
	print("**************************")

	database.closedatabase()
'''

if __name__ == '__main__':
	main()