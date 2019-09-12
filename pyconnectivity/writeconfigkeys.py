

import sqlite3


def openandupdatedbfile():
	conn = sqlite3.connect('Config.db')
	for table in range(3):
		query = "SELECT Key from ConfigTable%d" %table
		print(query)
		l = conn.execute(query)
		print (l.fetchall())
	#for table in range(3):
	#	for i in range()

	conn.close()
		

if __name__ == '__main__':
	openandupdatedbfile()
