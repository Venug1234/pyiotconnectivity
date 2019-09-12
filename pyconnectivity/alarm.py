import jsonwrapper
from pubsub import pub

# input data is [deviceid, iotkey, alarmcode]
def updatevalue(curvalue, epochtime):
	d = curvalue[0]
	data = {"devid":curvalue[0],str(d):curvalue[1], "timestamp":epochtime}
	jsonwrapper.convertsinglepayload(data)



def init():
	#create 1min timer for telmetry
	pub.subscribe(updatevalue, 'alarm')