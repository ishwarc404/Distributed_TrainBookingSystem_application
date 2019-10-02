from flask import Flask,render_template,request
import json
from socket import *



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
    client_socket(packet) #sending this packet to the client socket function

    return render_template("info_recieved.html")


def client_socket(packet):
    
    serverName = '127.0.0.1'
    serverPort = 12000
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))

    packet_json = json.dumps(packet)
    print(type(packet_json))
    clientSocket.send(packet_json)
    recieved_packet = clientSocket.recv(1024)
    print ("From Server:", recieved_packet)
    clientSocket.close()






if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")