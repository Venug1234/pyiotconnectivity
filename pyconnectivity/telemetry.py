import export
from pubsub import pub
from threading import Thread, Lock
import time
import jsonwrapper
'''
global variable to store telemetry data
{
	chillderid: {iotkey: [periodicity, persentvalue], iotkey:[periodicity, persentvalue]},
	chillderid: {iotkey: [periodicity, persentvalue], iotkey:[periodicity, persentvalue]}
} 
'''
teledata={}

# global variables to store lcm data
'''
global variable to store 
{
	chillderid: lcm1, chillderid: lcm2
}
'''
periodicitylcm = {}

mutex = Lock()

'''
This is a callback function on every data pushed by the publisher.
It updates the present value of given chiller id and given rpc key.
input arguement: [chillerid, iotkey, presentvalue]
'''
def updatevalue(curvalue):
	global teledata

	print("tele message received ", curvalue)

	mutex.acquire()
	try:
		for devkey in teledata:
			# search for matching chiller device id
			if curvalue[0] == devkey:
				iotkey = teledata[devkey]
				values = (iotkey.get(curvalue[1]))
				values[1] = curvalue[2]
				break;
	finally:
		mutex.release()

'''
This is the thread which wakesup every minute and see if any point
has crossed the telemetry timeout in any device. If a point reaches 
periodicity timeout send it to iot hub.
'''
def runtelemetry():
	global teledata
	global periodicitylcm
	while True:	
		print("\n *********** telemetery thread *********** ")

		mutex.acquire()
		try:
			for devid in teledata: # loop for every device
				data = {} #data to send to iot
				data.update({"devid":devid}) #first entry will be device id

				# get the calculated lcm for specific device
				callcm = periodicitylcm[devid]

				# if no device found, just skip the iteration
				if callcm == None:
					continue

				keys = teledata[devid].keys()
				values = teledata[devid].values()
				depth = len(teledata[devid])-1

				for i in range(depth):
					configlcm = values[i][0]
					if (callcm % configlcm == 0):
						data.update({str(keys[i]):values[i][1]})	

				data.update({"timestamp": long(time.time())})
				jsonwrapper.convertpayload(data)
		finally:
			mutex.release()

		time.sleep(60)
		pass

'''
This is the telemetry init function which reads the all telemetry type
datapoints from all configured chillers. This also subscribe for telemetry topic
in order to receive every telemetry change.
'''
def init():	
	# get the number of chillers
	num = export.getnumberofchillers()

	# get the list of chiller id's
	chillerid = export.getchillersidlist()

	#print(chillerid)

	print("inside telemetry init ************************ ")
	# loop each chiller and collect the telemetry type points and lcm
	for i in chillerid:
		teledata.update({i:export.gettelemetrydata(i)})
		periodicitylcm.update({i:export.getperiodicitylcm(i)})

	print("calculated lcm list of all device is %s" %periodicitylcm)

	#print("FULL TELEDATA IS ", teledata)
	# subscribe for the telemetry topic
	pub.subscribe(updatevalue, 'telemetry')

	# create a thread with 1min interval
	handle = Thread(target=runtelemetry, name='telemetry')

	# start the thread
	handle.start()

# function to clear all global data maintained in this module
def destroy():
	teledata.clear()
	periodicitylcm.clear()


