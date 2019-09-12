import runtimedb

# returns the number of chillers configured
def getnumberofchillers():
	return runtimedb.getchillercount()

# returns the [id1, id2, id3, ... ]
def getchillersidlist():
	return runtimedb.getchilleridlist()

#  creates object for chiller and fill the data
def addchiller(chillerid):
	return runtimedb.createdataobject()

# delete the given chiller from the database
def deletechiller(chillerid):
	return runtimedb.deletedataobject(chillerid)

# deletes all chillers information from database
def deleteallchillers():
	return runtimedb.deleteallobjects()

# returns the {iotkey:[periodicity, value]}
def gettelemetrydata(chillerid):
	return runtimedb.gettelemetrylist(chillerid)

# returns the periodicity lcm of given chiller
def getperiodicitylcm(chillerid):
	return runtimedb.getperiodicitylcm(chillerid)

def getallcovandthresholds(chillerid):
	return runtimedb.getcovandthresholdlist(chillerid)