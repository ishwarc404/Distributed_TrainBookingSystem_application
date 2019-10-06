from socket import *
import MySQLdb
import json
from datetime import datetime

def schedule_packetparse(packet_to_parse):
	#packet parse will basically convert the list into dictionary
	#this will enable easy access to the db
	packet_dictionary = {"Source":packet_to_parse[0],"Destination":packet_to_parse[1],"Date":packet_to_parse[2]}

	return packet_dictionary


def schedule_database_access(packet):

	#we need to parse the packet thast we have sent from the client and 
	# - recieved by the server socket

	#lets call a packet parse function
	parsed_packet = schedule_packetparse(packet) #packet is orignal packet
	#parsed_packet is the pacKet after parsing the data

	print("Let's print the parsed packet",parsed_packet)
	#parsed_packet is in a dictionary format

	#we will now use the information in this packet to retrive the train information


	# Open database connection
	#train_tkt is the name of the database
	db = MySQLdb.connect("localhost","root","rootroot","train_tkt" ) 

	# prepare a cursor object using cursor() method
	cursor = db.cursor()

	#table name is trains

	#proper sql command
	#sql = 'SELECT * FROM trains where From_City= \'{}\' AND To_City=\'{}\''.format(parsed_packet["Source"],parsed_packet["Destination"])
	
	#test sql command to return multiple rows
	sql = 'SELECT * FROM trains' #where From_City= \'{}\' AND To_City=\'{}\''.format(parsed_packet["Source"],parsed_packet["Destination"])
	cursor.execute(sql)

	results = cursor.fetchall()
	print((results))
	# for row in results:
	# 	print((row))
	returned_row = []
	for i in results:
		returned_row += [list(i)]
	
	#need to convert the timedelta into a string
	for i in returned_row:
		i[-1] = str(i[-1])

	return returned_row


#initialization of the data
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
	# print(packet) #this is just printing what the user is sending
	# print("in the server")
	# print(type(packet))

	#now lets call a function which will read the sql database and then return the values stored in it
	packet = json.loads(packet)

	#getting all the rows retrived from the database
	values = schedule_database_access(packet)


	return_packet = list(values) #sending just the first row for now #only 1 row will be sent back as there is only 1 train for every source and destination pair
	print("here",return_packet)
	return_packet = json.dumps(return_packet)
	print("type",type(return_packet))
	connectionSocket.send((return_packet).encode())
	connectionSocket.close() 


