import database
import globalvar

class chiller():
	def __init__(self):
		self.chillerid = 0 		#chiller id
		self.data = {}			#runtime database
		self.periodicitylcm = 0 #periodicity lcm
		self.teledata={}		#list of telemetry type points
		self.covdata={}

	def filldata(self, tablenum):
		val = []
		periodicitylist = []
		database.opendatabase()

		# verify the table has at least one row
		if 0 == database.readtotalcount(tablenum):
			print("iot: runtimedatabaseinit: No Records found")
			database.closedatabase()
			return -1

		# read rows and fill the runtime database
		# {rpckey:[iotkey, periodicity, cov, alarm]}
		keys = database.readallvalues(tablenum)
		for i in keys:
			val = [i[1],i[2],i[3],i[4]]
			self.data.update({i[0]:val})
		#print(self.data)

		# read all telemetry type points and update the lcm and teledat
		# {iotkey:[periodicity, current value]}
		obj = database.readtelmetrypoints(tablenum)
		for i in obj:
			val = [i[1], 0.0]
			periodicitylist.append(i[1])
			self.teledata.update({i[0]:val})

	    # read all cov type points and its threshold values
	    # iotkey : [thresholdvalue, previous value, presentvalue]}
		obj = database.readtelmetrycovpoints(tablenum)
		for i in obj:
			val = [i[1], 0.0]
			self.covdata.update({i[0]:val})

		obj =  database.readcovpoints(tablenum)
		for i in obj:
			val = [i[1], 0.0]
			self.covdata.update({i[0]:val})

		self.periodicitylcm = database.getlcm(periodicitylist)

		database.closedatabase()

	def getteledata(self):
		return self.teledata

	def getperiodicitylcm(self):
		return self.periodicitylcm

	def istelemetry(self,key):
		val = self.data.get(key)
		if( val != None):
			if (val[1]):	 #2 for periodcity	
				return True
		return False

	def getcovandthresholdlist(self):
		return self.covdata

	# check if given key is cov
	def iscov(self,key):
		val = self.data.get(key)
		if( val != None):
			if (val[2]):	 #3 for cov	
				return True
		return False

	# check if given key is alarm
	def isalarm(self,key):
		val = self.data.get(key)
		if( val != None):
			if (val[3]):	 #4 for alarm	
				return True
		return False

	# return iotkey of given rpckey
	def getiotkeyfromdb(self, key):
		key = int(key)
		val = self.data.get(key)
		#print(val)
		if val != None:
			return val[0]