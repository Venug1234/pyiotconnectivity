import sqlite3
from fractions import gcd


# open the database
def opendatabase():
	global conn 
	conn = sqlite3.connect('Config1.db')


def readtotalcount(tablenum):
	cmd =" SELECT count(*) from ConfigTable%d where Key >0 " %tablenum
	#print(cmd)
	names = conn.execute(cmd)
	i = names.fetchall()
	j = i[0]
	return(j[0])


# reads all aliasnames and return object to list of sets
def readallaliasnames():
	names = conn.execute(" SELECT AliasName from ConfigTable")
	return(names.fetchall())


def readallvalues(tablenum):
	cmd = "SELECT Key, IoTKey, Periodic, COV, Alarm  from ConfigTable%d where Key > 0" %tablenum
	names = conn.execute(cmd)
	return names.fetchall()

# reads all aliasnames and return object to list of sets
def readalarmpoints():
	names = conn.execute(" SELECT Key, IoTKey from ConfigTable where Alarm > 0 AND Key > 0")
	#print(names.fetchall())
	#return(names.fetchall())

# reads only cov type points (iotkey, COV )
def readcovpoints(tablenum):
	cmd = " SELECT IoTKey, COV from ConfigTable%d where COV > 0 AND Periodic <=0 AND Alarm <=0 AND Key > 0" %tablenum
	names = conn.execute(cmd)
	return(names.fetchall())

# reads telemetry type points
def readtelmetrypoints(tablenum):
	cmd = " SELECT IoTKey, Periodic from ConfigTable%d where Periodic > 0 AND Key > 0" %tablenum
	names = conn.execute(cmd)
	return(names.fetchall())

# reads only telemetry and cov points
def readtelmetrycovpoints(tablenum):
	cmd = " SELECT IOTKey, COV Periodic from ConfigTable%d where COV > 0 AND Periodic > 0  AND Alarm <=0 AND Key > 0" %tablenum
	names = conn.execute(cmd)
	return(names.fetchall())
	#print(names.fetchall())

# reads all distinct periodicity values from the table
def readtelemetryperiodicity():
	names = conn.execute(" SELECT DISTINCT Periodic from ConfigTable where Periodic > 0 AND Alarm <= 0 AND COV <=0 AND Key > 0")
	#print(names.fetchall())

# returns the number of telemetry points in the table
def readtelemetrypiontscount():
	names = conn.execute(" SELECT count(*) from ConfigTable where Periodic > 0 AND Key > 0")
	#print(names.fetchall())

# close the database
def closedatabase():
	conn.close()

def getlcm(plist):
	lcm = 1
	for i in plist:
		lcm = abs(lcm * i)//gcd(lcm,i)

	return lcm
