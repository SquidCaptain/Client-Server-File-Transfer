## server(n_port) is a program that consumes a port number n_port and
## 	waits at n_port for client to establish negotiation phase 
##	followed by transaction phase for file transfer.
## requires: has exactly 1 command line argument
## 	     no special characters in file names
## 	     n_port the same as n_port from client
## effects: read and write local files

from socket import *
import sys


n_port=int(sys.argv[1])
get=False
put=False
serverSocket=socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', n_port))
serverSocket.listen(1)
print('The server is ready to recieve')
while True:
	##Negotiation
	connectionSocket, addr=serverSocket.accept()
	##Recieving client command
	userInput=connectionSocket.recv(1024).decode()
	txtFile=""
	reply="OK"
	if userInput.split()[0] == "GET":
		get=True
		fileName=userInput.split(' ', 1)[1]
		txtFile=open(fileName, "r").read()
	elif userInput.split()[0] == "PUT":
		put=True
		fileName=userInput.split(' ', 1)[1]
	elif userInput == "EXIT":
		reply="ABORT"
	else:
		reply="ABORT"
	##Sending client feedback
	connectionSocket.send(reply.encode())
	if put or get:
		r_port=int(connectionSocket.recv(1024).decode())
		##Creating transaction socket
		transferSocket=socket(AF_INET, SOCK_STREAM)
		transferSocket.connect((addr[0], r_port))
		##End negotiation
		connectionSocket.close()
		##Transaction (File transfer)
		if get:
			transferSocket.send(txtFile.encode())
		elif put:
			transferSocket.send("OK")
			txtFile=transferSocket.recv(1024).decode()
			##File save
			open(fileName, "w").write(txtFile)
		get=False
		put=False
		##End transaction
		transferSocket.close()
	else:
		connectionSocket.close()

