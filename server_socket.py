from socket import *
import MySQLdb
import json

def database_access(packet):
	# Open database connection
	db = MySQLdb.connect("localhost","root","rootroot","train_booking" )

	# prepare a cursor object using cursor() method
	cursor = db.cursor()

	sql = "SELECT * FROM train_names"
	cursor.execute(sql)

	results = cursor.fetchall()
	for row in results:
		print(type(row))
	
	#print("everything came properly")
	#now lets send this tuple bacl
	#print(type(results)) -- tuple
	#return row #this is just one row for now
	return results


serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
count = 0

while 1:
	count+=1
	print("The tcp server is ready to receive:",count)
	connectionSocket, addr = serverSocket.accept()
	packet = connectionSocket.recv(1024)
	packet = packet.decode('utf-8')
	#packet is coming in as a json data
	print(packet) #this is just printing what the user is sending

	#now lets call a function which will read the sql database and then return the values stored in it
	values = database_access(packet)
	return_packet = list(values[0]) #sending just the first row for now
	print("here",return_packet)
	return_packet = json.dumps(return_packet)
	print("type",type(return_packet))
	connectionSocket.send((return_packet).encode())
	connectionSocket.close() 


