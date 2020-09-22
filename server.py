from socket import *
import threading

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen()

client_list = []
lock = threading.Lock()

print('The TCP server is ready to receive')

def addClient(clientSocket, addr):
	global client_list
	client_name = ""
	while True:
		try:
			msg = clientSocket.recv(1024).decode()
		except:
			print(client_name, ': connection failed')
			break
		
		if not msg:
			break
		
		print('msg: ',msg)
		
		data = msg.split('/')
		if data[0] == '@register':
			lock.acquire()
			client_list.append(clientSocket)
			lock.release()
			client_name = data[1]
			sendMemberInfo(data[1], ' enters.')
			#print(client_list,'\n')
		elif data[0] == '@unregister':
			lock.acquire()
			client_list.remove(clientSocket)
			lock.release()
			sendMemberInfo(data[1], ' exits.')
			#print(client_list,'\n')
		elif data[0] == '@chat':
			sendToAll(data[1], data[2])
			
		
	clientSocket.close()
	
def sendToAll(ID, content):
	global serverSocket, client_list
	msg = ID + ": " + content
	for clientSocket in client_list:
		clientSocket.send(msg.encode())

def sendMemberInfo(ID, status):
	global serverSocket, client_list
	msg = ID + status + ' Current # of members: '+str(len(client_list))
	for clientSocket in client_list:
		clientSocket.send(msg.encode())


while True:
	clientSocket, addr = serverSocket.accept()
	t = threading.Thread(target=addClient, args=(clientSocket, addr))
	t.start()
	
