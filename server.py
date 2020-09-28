from socket import *
import threading

serverPort = 12001
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen()

client_list = [] #(client_name, clinetSocket)
lock = threading.Lock()

print('The TCP server is ready to receive')

def addClient(clientSocket, addr):
	global client_list
	client_name = ""
	while True:
		try:
			msg = clientSocket.recv(1024).decode()
		except Exception as e:
			print('Error: ', e)
			break
		
		if not msg:
			break
		
		print('msg: ',msg)
		
		data = msg.split('/')
		if data[0] == '@register':
			client_name = data[1]
			sendMemberInfo(client_name, 'register')
			lock.acquire()
			client_list.append((client_name, clientSocket))
			lock.release()
			sendClientList(clientSocket)
			#print(client_list,'\n')
		elif data[0] == '@unregister':
			lock.acquire()
			client_list.remove((client_name, clientSocket))
			lock.release()
			sendMemberInfo(client_name, 'unregister')
			#print(client_list,'\n')
		elif data[0] == '@chat':
			sendToAll(data[1], data[2])
			
		
	clientSocket.close()
	
def sendClientList(clientSocket):
	global serverSocket, client_list
	msg = "@init_client_list"
	for client in client_list:
		msg += ("/"+client[0])
	
	try:
		clientSocket.send(msg.encode())
	except Exception as e:
		print('Error: ', e)
	
def sendToAll(ID, content):
	global serverSocket, client_list
	msg = ID + ": " + content
	try:
		for client in client_list:
			client[1].send(msg.encode())
	except Exception as e:
		print('Error: ', e)

def sendMemberInfo(ID, status):
	global serverSocket, client_list
	msg = ""
	if status == "register":
		msg = "@add_client/"+ID
	elif status == "unregister":
		msg = "@remove_client/"+ID
	
	try:
		for client in client_list:
			client[1].send(msg.encode())
	except Exception as e:
		print('Error: ', e)

while True:
	clientSocket, addr = serverSocket.accept()
	t = threading.Thread(target=addClient, args=(clientSocket, addr))
	t.start()
	
