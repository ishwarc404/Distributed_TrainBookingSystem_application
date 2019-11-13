from flask import Flask,render_template,request
import json
from socket import *
# import MySQLdb
import pymysql as MySQLdb



'''
NOTE: The print statements used are just for testing
if the information exchange is working perfectly or not

The info_receieved_html is just a tester web page
'''

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")


@app.route("/ticket_cancellation")
def cancellation():
    ticket_id = str(request.form(["ticket_id"]))
    #we now need to access the database and remove this particular row from there



@app.route("/booking_confirmation",methods = ['POST','GET']) #when the person clicks on Book
def booking(): 
    source = str(request.form['source'])
    destination = str(request.form['destination'])
    train_name = str(request.form['train_name'])
    avalilable_seats = request.form['availability'] #no of seats available in that train
    print("THE TRAIN U BOOKED IS",train_name," from: ",source," to: ",destination)
    return render_template("booking_confirmation.html",booked_train_details = [source,destination,train_name,avalilable_seats])

@app.route("/booking_payment",methods = ['POST','GET']) #when the person finishes entering passenger details
def payment():
    #we first need to get the numbe of passengers that were registered
    no_of_passengers = request.form['counter_text']
    no_of_passengers = int(no_of_passengers)
    date_of_travel = request.form["date_of_travel"]
    date_of_travel = str(date_of_travel)
    train_name = request.form["train_name"]

    passenger_data = []
    print("NUMBER OF PASSENGERS REGISTERED::",no_of_passengers)
    for i in range(1,no_of_passengers+1):
        passenger_name = str(request.form["passenger_name"+str(i)])
        passenger_age = str(request.form["passenger_age"+str(i)])
        passenger_data+=[[passenger_name,passenger_age]]

    
    new_single_list = [date_of_travel,train_name] #adding the date of travel initially
    for i in passenger_data:
        for j in i:
            new_single_list+=[j]
   

    #commenting the following line for now until the database is sorted
    client_socket(new_single_list) #we do this as in the server, json cannot process a list oflis
    
    passenger_data = json.dumps(passenger_data) #showing all passenger data
    return render_template("booking_payment.html", no_of_passengers =passenger_data)


@app.route('/initial_user_data',methods = ['POST','GET'])
def initial_user_data():
    #this function will get the basic user query and send it via the socket to the server socket
    
    # getting all the form data
    source_location = request.form['source_name']
    destination_location = request.form['destination_name']
    date_of_travel = request.form['date_of_travel']
    passenger_count = request.form['passenger_count']

    # print(source_location,destination_location,date_of_travel) #just checking
    '''
    the following function will be used to create a socke and will be used
    to connect to the server socket and pass the information to it '''

    #lets bundle everything up to pass to the client socket function
    packet = [source_location,destination_location,date_of_travel] #just checking
    received_packet = client_socket(packet) #sending this packet to the client socket function
    print("All the rows recieved:",received_packet)
    print("packets recieved were printed above")
    #received_packet = received_packet[0] #to just test printing a single row
    #print(received_packet)
    #processed_packet = [str(i) for i in received_packet] #processing to handle the unicode encoding
    processed_packet = []
    for i in received_packet:
        processed_packet += [str(j) for j in i] #processing to handle the unicode encoding

    print("recieved packet type:",processed_packet)

    #HERE; THE NUMBER OF SEATS AVAILABLE RETURNED FROM THE DB REFERS TO THE TOTAL CAPACITY OF THE TRAIN.
    #BUT WE NEED TO SHOW TO THE USER THE NUMBER OF SEATS AVAILABLE FOR THAT DATE OF TRAVEL
    #WE CAN SHOW IT AS AN ANOTHER COLUMN
    #BUT WE NOW NEED TO KEEP TRACK OF THE DATE OF TRAVEL TOO. ACTUALLY NOT REALLY

    #the processed packet contains the names of the trains
    train_db = []
    for i in range(3,len(processed_packet),6):
        train_db+=[processed_packet[i]]

    print("DATE OF TRAVEL",date_of_travel)

    train_seats = [100 for i in range(len(train_db))]

    # for train_name in train_db:
    #     #now we need to connect and access the sql database
    #     db = MySQLdb.connect("localhost","root","rootroot","train_tkt" ) 
    #     # prepare a cursor object using cursor() method
    #     cursor = db.cursor()
    #     sql = "SELECT Seats_booked FROM booking where Date_of_journey=\'{}\' AND Train_name=\'{}\';".format(date_of_travel,train_name)
    #     cursor.execute(sql)
    #     results = cursor.fetchall()
    #     if(len(results)==0):
    #         #means no bookings for that corresponding date and trains
    #         sql = "SELECT No_of_available_seat FROM trains where Trains=\'{}\';".format(train_name)
    #         cursor.execute(sql)
    #         results = cursor.fetchall()
    #         capacity = results[0][0]
    #         train_seats += [capacity] #means the entire capacity is available for booking
    #     else:
    #         seats_booked = results[0][0] #these are the total seats booked
    #         sql = "SELECT No_of_available_seat FROM trains where Trains=\'{}\';".format(train_name)
    #         cursor.execute(sql)
    #         results = cursor.fetchall()
    #         capacity = results[0][0]
    #         train_seats+=[capacity - seats_booked] #these are the total seats available

    # #we now need to insert the data from train seats back into the processed packet
    # #we need to make a new list now 
    print("TRAIN SEATS ARE:",train_seats)
    new_processed_packet = []
    k = 0
    for i in train_seats:
        new_processed_packet += processed_packet[k:k+6]
        new_processed_packet.append(i)
        k +=6

    # print("THE NEW PROCESSED PACKET IS:", new_processed_packet)
    return render_template("train_schedules.html",output=new_processed_packet)


def client_socket(packet):
    serverName = '169.254.161.103'
    serverPort = 12000
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))

    packet_json = json.dumps(packet)
    print("Sent from Client to the Sever:=",packet_json)
    print(type(packet_json))
    clientSocket.send(packet_json.encode()) #sending to the server
    received_packet = clientSocket.recv(1024)
    print ("From Server:",received_packet)
    clientSocket.close()
    print("hello here")
    received_packet = json.loads(received_packet) #converting the json string to a list
    return received_packet #returning it back to the initial_user_datafunction


if __name__ == "__main__":
    app.run()