from flask import Flask,render_template,request
import json
from socket import *


'''
NOTE: The print statements used are just for testing
if the information exchange is working perfectly or not

The info_receieved_html is just a tester web page
'''

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/initial_user_data',methods = ['POST','GET'])
def initial_user_data():
    #this function will get the basic user query and send it via the socket to the server socket
    
    #getting all the form data
    source_location = request.form['source_name']
    destination_location = request.form['destination_name']
    date_of_travel = request.form['date_of_travel']
    passenger_count = request.form['passenger_count']

    print(source_location,destination_location,date_of_travel,passenger_count) #just checking
    '''
    the following function will be used to create a socke and will be used
    to connect to the server socket and pass the information to it '''

    #lets bundle everything up to pass to the client socket function
    packet = [source_location,destination_location,date_of_travel,passenger_count] #just checking
    received_packet = client_socket(packet) #sending this packet to the client socket function
    received_packet = received_packet[0]
    print(received_packet)
    processed_packet = [str(i) for i in received_packet] #processing to handle the unicode encoding
    print("recieved packet type:",processed_packet)
    return render_template("train_schedules.html",output=processed_packet)


def client_socket(packet):
    serverName = '127.0.0.1'
    serverPort = 12000
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))

    packet_json = json.dumps(packet)
    print(type(packet_json))
    clientSocket.send(packet_json)
    received_packet = clientSocket.recv(1024)
    print ("From Server:",received_packet)
    clientSocket.close()
    print("hello here")
    received_packet = json.loads(received_packet) #converting the json string to a list
    return received_packet #returning it back to the initial_user_datafunction






if __name__ == "__main__":
    app.run(debug=True)