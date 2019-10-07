from socket import *
import MySQLdb
import json
from datetime import datetime


def passenger_database_access(packet):
	passenger_data = {"Name":[],"Age":[]} #we need to make a list now with the passenger names and age
	for i in range(0,len(packet),2):
		passenger_data["Name"]+=[packet[i]] 
		passenger_data["Age"]+=[packet[i+1]] 

	#print(passenger_data)
	
	#now we need to connect and access the sql database
	
	return



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
	
	#test sql command if mysql is not installed
	# returned_row = [[1, 'Boongalore', 'Shimogga', 'Shatabdi ', '8:00:00'], [2, 'Bangalore', 'Chennai', 'Lalbagh', '0:00:08'], [3, 'Bangalore', 'Hubli', 'double decker', '0:00:10'], [4, 'Hubli', 'Shimogga', 'Lalbagh', '0:00:11'], [5, 'Chennai', 'Bangalore', 'Mail', '0:00:07'], [6, 'Chennai', 'Shimogga', 'Chennai Express', '0:00:13']]
	# return returned_row


	cursor.execute(sql)

	results = cursor.fetchall()
	#print((results))
	# for row in results:
	# 	print((row))
	returned_row = []
	for i in results:
		returned_row += [list(i)]
	
	#need to convert the timedelta into a string
	for i in returned_row:
		i[-1] = str(i[-1])

	#print("All rows returned::",returned_row)
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

	#Note that passenger details will come in as a single list and 
	#not as a list of list coz json cannot decode

	#WE NEED TO DIFFERENTIATE BETWEEN THE PAKCETS FOR THE 2 DB ACCESSES
	#FOR NOW LET'S JUST SEE HOW MANY VALUES ARE THERE
	if(len(packet)!=3):
		print("DB ACCESS 2")
		passenger_database_access(packet)
		connectionSocket.close() 
		#means it is the index page database access
	else:
		print("DB ACCESS 1")
		values = schedule_database_access(packet)
		print("PACKET PRINTING:",packet,type(packet))
		#getting all the rows retrived from the database
		return_packet = values #sending just the first row for now #only 1 row will be sent back as there is only 1 train for every source and destination pair
		print("here",return_packet)
		return_packet = json.dumps(return_packet)
		print("type",type(return_packet))
		connectionSocket.send((return_packet).encode())
		connectionSocket.close() 


