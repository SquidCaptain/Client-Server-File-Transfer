## client(serverName, n_port) is a program that consumes a server
## 	address and a port number n_port and connects to the specified
## 	server in order to transfer files.
## requires: has exactly 2 command line arguments
## 	     no special characters in file names
## 	     n_port the same as n_port from client
## effects: read and write local files

from socket import *
import sys

serverName=str(sys.argv[1])
n_port=int(sys.argv[2])
r_port=11234
get=False
put=False
txtFile=""
fileName=""
##Initiate negotiation
clientSocket=socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, n_port))
command=raw_input('Input command:')
if command.split()[0] != "EXIT":
	fileName=command.split(' ', 1)[1]
	if command.split()[0] == "GET":
		get=True
	elif command.split()[0] == "PUT":
		put=True
		txtFile=open(fileName, "r").read()
clientSocket.send(command.encode())
reply=clientSocket.recv(1024).decode()
##Transaction
if reply=="OK":
	tempPort=int(raw_input('Input r_port:'))
	if tempPort is int:
		if tempPort >= 1024:
			r_port = tempPort
	##Creating transaction socket
	transferSocket=socket(AF_INET, SOCK_STREAM)
	transferSocket.bind(('', r_port))
	transferSocket.listen(1)
	clientSocket.send(str(r_port).encode())
	##End negotiation
	clientSocket.close()
	connectionSocket, addr=transferSocket.accept()
	if get:
		txtFile=connectionSocket.recv(1024).decode()
		##File save
		open(fileName, "w").write(txtFile)
	elif put:
		connectionSocket.recv(1024)
		connectionSocket.send(txtFile.encode())
	##End Transaction
	connectionSocket.close()
	transferSocket.close()
else:
	clientSocket.close()
