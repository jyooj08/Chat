from tkinter import *

def btncmd():
    readOnlyText.configure(state="normal")
    readOnlyText.insert(END, entry.get()+"\n")
    entry.delete(0,END)
    readOnlyText.configure(state="disabled")
    readOnlyText.see(END)

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
member_list.insert(END, "member1")
member_list.insert(END, "member2")
member_list.insert(END, "member3")
#member_list.configure(state="disabled")
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

root.mainloop()