from socket import *
import threading

serverIP = '192.168.0.4'
serverPort = 12001
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverIP, serverPort))

def getMessage():
	global clientSocket
	while True:
		msg = clientSocket.recv(1024)
		if not msg:
			continue
		print(msg.decode())


#register client
ID = input('Enter your ID: ')
msg = "@register/"+ID
clientSocket.send(msg.encode())

t = threading.Thread(target=getMessage)
t.daemon = True
t.start()


while True:
	msg = input()
	if msg == '@exit':
		break	
	msg = '@chat/'+ID+'/'+msg
	clientSocket.send(msg.encode())

msg = "@unregister/"+ID
clientSocket.send(msg.encode())


clientSocket.close()
