#import database
from controllerobject import chiller
#import globalvar

dblist= {}

'''
maxchillers = 4

#global chillers runtime table
indata={}
'''
# check if given key is telemetry
def istelemetry(chillerid, key):
	obj = dblist.get(chillerid)
	return obj.istelemetry(key)

# check if given key is cov
def iscov(chillerid ,key):
	obj = dblist.get(chillerid)
	return obj.iscov(key)

# check if given key is alarm
def isalarm(chillerid , key):
	obj = dblist.get(chillerid)
	return obj.isalarm(key)
'''
# initialize the runtime database
# {rpckey:[iotkey, config, value ]}
def runtimedatabaseinit():
	database.opendatabase()
	
	# verify the table has at least one row
	if 0 == database.readtotalcount():
		print("iot: runtimedatabaseinit: No Records found")
		database.closedatabase()
		return -1

	# read rows and fill the runtime database
	for j in range(maxchillers-1):
		keys = database.readallvalues()
		for i in keys:
			val = [i[1],i[2],i[3],i[4]]
			indata.update({i[0]:val})
		print(indata)


	database.closedatabase()
	#print(indata)

	print("iot: runtimedatabaseinit: runtime database created")
	#print(chillersdata)
	return 0
'''
def createdataobject(chillerid):
	obj = chiller()
	dblist.update(chillerid, obj)

def runtimedatabaseinit():
	#i = 0
	#length = dblist.count()
	#for i in range (length - 1):
	for i in range(3):
		obj = chiller()
		dblist.update({i:obj})
		obj.filldata(i)

def getchillercount():
	l = dblist.keys()
	print(l)
	return len(l)

def getchilleridlist():
	print(dblist.keys())
	return dblist.keys()

def deletedataobject(chillerid):
	dblist.pop(chillerid)

def deleteallobjects():
	dblist.clear()

def gettelemetrylist(chillerid):
	obj = dblist.get(chillerid)
	return obj.getteledata()

def getcovandthresholdlist(chillerid):
	obj = dblist.get(chillerid)
	return obj.getcovandthresholdlist()


def getperiodicitylcm(chillerid):
	obj = dblist.get(chillerid)
	return obj.getperiodicitylcm()

def getchillerobj(chillerid):
	return dblist.get(chillerid)

def getiotkey(chillerid, rpckey):
	obj = dblist.get(chillerid)
	return obj.getiotkeyfromdb(rpckey)