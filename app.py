from tkinter import *
from socket import *
import threading

serverIP = '192.168.0.5'
serverPort = 12001
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverIP, serverPort))
client_list = []

def btncmd():
    global clientSocket
    msg = entry.get()
    msg = '@chat/'+ID+'/'+msg
    clientSocket.send(msg.encode())

def pressEnter(event):
    btncmd()


root = Tk()
root.geometry("500x400")
root.resizable(False, False)
root.title("Chat Room")
root.propagate(0)

input_frame = Frame(root, relief="solid", bd=1)
input_frame.pack(side="bottom", fill="both")

entry = Entry(input_frame, width=50)
entry.bind('<Return>', pressEnter)
entry.pack(side="left")

enter_btn = Button(input_frame, text="Enter", command=btncmd)
enter_btn.pack(side="right")

##################################
member_frame = Frame(root, relief="solid", bd=1, width=150)
member_frame.pack(side="left", fill="both")

label1 = Label(member_frame, text="member_frame")
label1.pack()

member_list = Listbox(member_frame, selectmode="extended", height=0)
member_list.pack()

# member_scroll = Scrollbar(member_frame)
# member_scroll.pack(side="right", fill="y")
# member_scroll.configure(member_list.yview)

##################################
chat_frame = Frame(root, relief="solid", bd=1, width=250)
chat_frame.pack(side="right", fill="both")
readOnlyText = Text(chat_frame)

label2 = Label(chat_frame, text="chat_frame")
label2.pack()

chat_scroll = Scrollbar(chat_frame, command=readOnlyText.yview)
chat_scroll.pack(side="right", fill="y")


readOnlyText.configure(state="disabled")
readOnlyText.pack(side="left", fill="both")
readOnlyText.configure(yscrollcommand=chat_scroll.set)

####################
def getMessage():
    global clientSocket, readOnlyText, entry
    while True:
        msg = clientSocket.recv(1024).decode()
        if not msg:
            continue

        data = msg.split("/")
        if data[0] == "@init_client_list":
            length = len(data)
            for i in range(1, length):
                member_list.insert(END,data[i])
                
        elif data[0] == "@add_client":
            member_list.insert(END, data[1])
            readOnlyText.configure(state="norma")
            readOnlyText.insert(END, data[1]+" enters.\n")
            readOnlyText.configure(state="disabled")
            readOnlyText.see(END)
            
        
        elif data[0] == "@remove_client":
            #client_list.remove(data[1])
            #print('delete ', member_list.index(data[1]))
            list_size = member_list.size()
            for i in range(0, list_size):
                if data[1] == member_list.get(i):
                    member_list.delete(i)
                    break

            readOnlyText.configure(state="normal")
            readOnlyText.insert(END, data[1]+" exits.\n")
            readOnlyText.configure(state="disabled")
            readOnlyText.see(END)
            
        else:
            print(msg)
            readOnlyText.configure(state="normal")
            readOnlyText.insert(END, msg+"\n")
            entry.delete(0,END)
            readOnlyText.configure(state="disabled")
            readOnlyText.see(END)

#register client
ID = input('Enter your ID: ')
msg = "@register/"+ID
clientSocket.send(msg.encode())

t = threading.Thread(target=getMessage)
t.daemon = True
t.start()



root.mainloop()

msg = "@unregister/"+ID
clientSocket.send(msg.encode())

clientSocket.close()