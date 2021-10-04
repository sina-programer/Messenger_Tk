from tkinter import *
from tkinter import simpledialog
import threading 
import socket
import time

class App:
    def __init__(self, master):
        self.master = master
        
        self.send_btn = Button(self.master, text='Send', state='disabled', command=self.send)
        self.send_btn.pack(side=BOTTOM, fill=X)
        self.text_var = StringVar()
        Entry(self.master, textvariable=self.text_var).pack(side=BOTTOM, fill=X)
    
    def send(self):
        text = self.text_var.get()
        if text:
            self.text_var.set('')
            self.client.send(text.encode())
            text = f'You: {text}'
            Label(self.master, text=text, bg='#FF9187', anchor='w', relief='raised').pack(side=TOP, fill=X)
        
    def recv(self):
        while True:
            text = self.client.recv(1024).decode('utf-8')
            if text:
                text = f'{text} :Server'
                Label(self.master, text=text, bg='#AFAFFF', anchor='e', relief='raised').pack(side=TOP, fill=X)
                
    def connect(self):
        ip = simpledialog.askstring('IP', 'Enter server IP: ')
        port = simpledialog.askinteger('Port', 'Enter Port: ')
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((ip, port))
        self.send_btn.config(state='normal')
        self.master.bind('<Return>', lambda _: self.send())
        threading.Thread(target=self.recv).start()
        


if __name__ == "__main__":
    root = Tk()
    root.title('Client')
    root.geometry('400x600+750+130')
    root.iconbitmap('files/client_icon.ico')
    root.resizable(False, False)
    root.focus_force()
    
    app = App(root)
    app.connect()
    
    root.mainloop()
