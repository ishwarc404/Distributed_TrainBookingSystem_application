# Distributed_TrainBookingSystem_application

#Pre
1. Install flask
2. Install sql and import the db
3. SQL server needs to be running
4. Note: If MySQL is not installed, don't worry , just uncomment lines 45 and 46 in server_socket.py ; 
This line :: https://github.com/ishwarc404/Distributed_TrainBookingSystem_application/blob/392546eedb963b44439fcec701dfd1481087e863/server_socket.py#L45

#To run
1. run server_socket.py
2. run client_flask.py
3. go to http://127.0.0.1:5000/
4. Have Fun


#Need to work on:
1. Fix "Chennai Express" name display 
2. Populate the "trains" databases with more train details : CURRENTLY WORKING ON
3. Build the flask and db connections for the "passenger" database.

#CURRENTLY WORKING ON:
1. Pass on the name of the train too to the payment

#VERY IMPORTANT THING TO LOOK AT
1. Different Dates and train bookings
2. Need to form a new table [Date,TrainName,No_of_seats_booked,No_of_seats_available]