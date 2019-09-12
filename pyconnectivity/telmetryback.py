import export
from pubsub import pub
import threading
import time
import jsonwrapper
'''
global variable to store telemetry data
[ 
	{chillderid: {iotkey: [periodicity, persentvalue], iotkey:[periodicity, persentvalue]}},
	{chillderid: {iotkey: [periodicity, persentvalue], iotkey:[periodicity, persentvalue]}}
] 
'''
teledata=[]

# global variables to store lcm data
'''
global variable to store 
[ 
	{chillderid: lcm1},
	{chillderid: lcm2},
] 
'''
periodicitylcm = []


'''
This is a callback function on every data pushed by the publisher.
It updates the present value of given chiller id and given rpc key.
input arguement: [chillerid, iotkey, presentvalue]
'''
def updatevalue(curvalue):
	global teledata
	idx = 0
	print("message received ", curvalue)

	for i in teledata:
		devkey = i.keys() # get list of chiller ID's (ideally only one)

		# search for matching chiller device id
		if curvalue[0] == devkey[0]:
			print("Matching device found ")
			# search for matching iot key
			print("first i values", i)
			iotkey = (i.values())[0] #{iotkey : [], iotkey: []}
			#print("dict is %s and input key is %d " %(iotkey, curvalue[1]))
			values = (iotkey.get(curvalue[1]))
			#print("values are ", values)
			values[1] = curvalue[2]
			i.update({curvalue[1]:values})
			#print ("after i values ", i)
			(teledata[idx]).update({curvalue[0]:i})
			print("after update", teledata)
			break;
		else:
			idx = idx + 1
			

	print("*******")
	#print("after update", teledata)
'''
	listval = i.values()


	chiller = teledata[curvalue[0]] #index 0 is chiller ID
	.get(curvalue[0])
	if( val != None):
		val[1] = curvalue[1]
		#print(curvalue, curvalue[0], val)
		teledata.update({curvalue[0]:l})
	#print teledata
'''
'''
This is the thread which wakesup every minute and see if any point
has crossed the telemetry timeout in any device. If a point reaches 
periodicity timeout send it to iot hub.
'''
def runtelemetry():
	global teledata
	global periodicitylcm
	while True:
		print("calculated lcm list of all device is %s" %periodicitylcm)
		if periodicitylcm:
			print("\n *********** telemetery thread *********** ")

			for dev in teledata: # loop for every device
				devid = (dev.keys())[0] #only one device id
				callcm = 0

				# get the calculated lcm for specific device
				for i in range((len(periodicitylcm)-1)):
					if devid == ((periodicitylcm[i]).keys())[0]:
						callcm = ((periodicitylcm[i]).values())[0]

				# if no device found, just skip the iteration
				if callcm == 0:
					continue

				data = {}
				#for e in dev: # from the dictionary of [{key :values,key:values}]
				x = dev.values() # e is a list will store [{key :values,key:values}]
				e = x[0] #always one {key :values,key:values}
				keys = e.keys()
				values = e.values() #[ [periodicity, value ] , [], []]
				#print("values %s" %values)

				for i in range(len(keys)-1):
					inputpcity = values[i][0]
					#print("inputcity", inputpcity)
					if (callcm % inputpcity == 0):
							data.update({keys[i]:values[i][1]})
							#teledata[]e.update({data})})
				

			#data.update({1000, long(time.time())})
			#jsonwrapper.convertpayload(data)
		time.sleep(30)
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
		record = {}
		valdict = export.gettelemetrydata(i)
		record.update({i:valdict})
		#print(record)
		teledata.append(record)
		periodicitylcm.append({i:export.getperiodicitylcm(i)})

	print("FULL TELEDATA IS ", teledata)
	# subscribe for the telemetry topic
	pub.subscribe(updatevalue, 'telemetry')

	# create a thread with 1min interval
	handle = threading.Thread(target=runtelemetry, name='telemetry')

	# start the thread
	#handle.start()

# function to clear all global data maintained in this module
def destroy():
	teledata.clear()
	periodicitylcm.clear()


