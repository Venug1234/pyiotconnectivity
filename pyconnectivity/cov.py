import jsonwrapper
import export
from pubsub import pub
'''
#stores all chillers COV type IOTkeys and its threshold values
{
	chillerid : {iotkey:[threshold, previous value, ],iotkey:[threshold, previous value, ]},
	chillerid : {iotkey:[threshold, previous value, ],iotkey:[threshold, previous value, ]},	
}
'''
covdata = {}

#curvalue will hold [devid, iotkey, presentvalue]
def updatevalue(curvalue, epochtime):
	global covdata

	print("cov message received", curvalue)
	for devid in covdata:
		data = {}
		if devid == curvalue[0]:
			data.update({"devid":devid})
			preValue = (covdata[devid].get(curvalue[1]))[1]
			threshold = (covdata[devid].get(curvalue[1]))[0]
			if abs(preValue - curvalue[2]) >= threshold:
				data.update({str(curvalue[1]): curvalue[2]})
				data.update({"timestamp":epochtime})
				jsonwrapper.convertpayload(data)

			#update the value
			(covdata[devid].get(curvalue[1]))[1] = curvalue[2]
			print("after cov update", covdata[devid])


def init():

	# get the list of chiller id's
	chillerid = export.getchillersidlist()

	# loop each chiller and collect the telemetry type points and lcm
	for i in chillerid:
		covdata.update({i: export.getallcovandthresholds(i)})

	print("full COV list", covdata)

	#create 1min timer for telmetry
	pub.subscribe(updatevalue, 'cov')