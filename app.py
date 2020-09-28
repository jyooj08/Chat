from tkinter import *
from socket import *
import threading
import tkinter.messagebox as msbox

serverIP = '192.168.243.1'
serverPort = 12001
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverIP, serverPort))
client_list = []
ID = ""
color="#b0e0e6"

def btncmd():
    global clientSocket
    msg = entry.get()
    if msg == "":
        return
    msg = '@chat/'+ID+'/'+msg
    clientSocket.send(msg.encode())

def pressEnter(event):
    btncmd()

def login():
    global ID
    ID = id_entry.get()
    if ID== "":
        msbox.showwarning("Warning", "Enter your ID")
        return

    msg = "@register/"+ID
    clientSocket.send(msg.encode())

    t = threading.Thread(target=getMessage)
    t.daemon=True
    t.start()


    color_frame.destroy()
    main_frame.pack(fill='both', expand=True)

def pressLogin(event):
    login()



root = Tk()
root.geometry("500x400")
root.resizable(False, False)
root.title("Chat Room")
root.propagate(0)

color_frame = Frame(root, bg=color)
color_frame.pack(fill='both', expand=True)
login_frame = Frame(color_frame, bg=color)
login_frame.pack(fill='x', expand=True)
id_label = Label(login_frame, text="Enter your ID", bg=color)
id_entry = Entry(login_frame, width=30)
login_btn = Button(login_frame, text="Login", command=login, bg="#ffffff", padx=10)

id_label.pack()
id_entry.bind('<Return>', pressLogin)
id_entry.pack()
login_btn.pack()


main_frame = Frame(root, bg=color, padx=3, pady=3)

input_frame = Frame(main_frame, padx=3, pady=3, bg=color)
input_frame.pack(side="bottom", fill="both")

entry = Entry(input_frame)
entry.bind('<Return>', pressEnter)
entry.pack(side="left", fill="x", expand=True)

enter_btn = Button(input_frame, text="Enter", command=btncmd, padx=2)
enter_btn.pack(side="right")

##################################
member_frame = LabelFrame(main_frame, text="member_list", padx=3, pady=3, bg=color)
member_frame.pack(side="left", fill="both")

list_frame = Frame(member_frame, bg="white")
list_frame.pack(fill="both", expand=True)
member_list = Listbox(list_frame, selectmode="extended", height=2, relief="solid")
member_list.pack()

# member_scroll = Scrollbar(member_frame)
# member_scroll.pack(side="right", fill="y")
# member_scroll.configure(member_list.yview)

##################################
chat_frame = LabelFrame(main_frame, text="Chat", padx=3, pady=3, bg=color)
chat_frame.pack(side="right", fill="both")
readOnlyText = Text(chat_frame)

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



root.mainloop()

msg = "@unregister/"+ID
clientSocket.send(msg.encode())

clientSocket.close()