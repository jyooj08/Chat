from socket import *
import threading

serverIP = '192.168.243.1'
serverPort = 12001
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverIP, serverPort))
client_list = []

def getMessage():
	global clientSocket
	while True:
		msg = clientSocket.recv(1024).decode()
		if not msg:
			continue
			
		data = msg.split("/")
		if data[0] == "@init_client_list":
			length = len(data)
			for i in range(1, length):
				client_list.append(data[i])
			print("client_list: ", client_list)
			
		elif data[0] == "@add_client":
			client_list.append(data[1])
			print(data[1],' enters. Current # of members: ', len(client_list))
		
		elif data[0] == "@remove_client":
			client_list.remove(data[1])
			print(data[1], ' exits. Current # of members: ', len(client_list))
		else:
			print(msg)


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
