import sqlite3


def main():
	conn = sqlite3.connect('Config1.db')

	for i in range(4):
		for j in range(153):
			cmd = "UPDATE ConfigTable%d set Key=%d where IoTKey=%d" % (i, j, j)
			print(cmd)
			conn.execute(cmd)

	conn.commit()

	conn.close()

	'''
	cmd = cmd =" SELECT count(*) from ConfigTable%d where Key >0 " %i
	names = conn.execute(cmd)
	k = names.fetchall()
	l = i[0]
	count = l[0]
	i = 1
	for i in range(count):
	'''



if __name__ == '__main__':
	main()