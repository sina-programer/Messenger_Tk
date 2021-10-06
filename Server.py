from tkinter import *
from tkinter import simpledialog, colorchooser, messagebox
import webbrowser
import threading 
import winsound
import socket
import time
import os


class PersonalizeDialog(simpledialog.Dialog):
    def __init__(self, parent, app):
        self.app = app
        super().__init__(parent, 'Personalize')

    def body(self, frame):
        self.color = self.app.color
        Label(self, text='Color: ').place(x=10, y=50)
        self.color_btn = Button(self, bg=self.color, width=2, command=self.change_color)
        self.color_btn.place(x=50, y=48)
        
        self.username = StringVar()
        self.username.set(self.app.username)
        Label(self, text='Username: ').place(x=10, y=15)
        Entry(self, textvariable=self.username).place(x=75, y=17)
        
        Button(self, text='Apply', width=7, command=self.apply).place(x=150, y=50)
        Button(self, text='Cancel', width=7, command=self.destroy).place(x=85, y=50)
        
        self.geometry('220x90+550+350')
        self.resizable(False, False)
        self.bind('<Return>', lambda _: self.apply())
        self.bind('<Escape>', lambda _: self.destroy())
        winsound.MessageBeep()
        
        return frame
    
    def change_color(self):
        _, color = colorchooser.askcolor(initialcolor=self.color)
        self.color = color
        self.color_btn.config(bg=self.color)
        
    def apply(self):
        self.app.color = self.color
        self.app.username = self.username.get()
        messagebox.showinfo('Apply', 'Your changes saved successfuly')

    def buttonbox(self):
        pass


class AboutDialog(simpledialog.Dialog):
    def __init__(self, parent):
        super().__init__(parent, 'About us')

    def body(self, frame):
        Label(self, text='This program made by Sina.f').pack(pady=12)
        Button(self, text='GitHub', width=8, command=lambda: webbrowser.open('https://github.com/sina-programer')).place(x=30, y=50)
        Button(self, text='Instagram', width=8, command=lambda: webbrowser.open('https://www.instagram.com/sina.programer')).place(x=120, y=50)
        Button(self, text='Telegram', width=8, command=lambda: webbrowser.open('https://t.me/sina_programer')).place(x=210, y=50)

        self.geometry('300x100+550+350')
        self.resizable(False, False)
        winsound.MessageBeep()

        return frame

    def buttonbox(self):
        pass


class App:
    def __init__(self, master):
        self.master = master
        self.master.config(menu=self.init_menu())
        
        self.username = 'Server'
        self.color = '#FF9187'
        
        self.send_btn = Button(self.master, text='Send', state='disabled', command=self.send)
        self.send_btn.pack(side=BOTTOM, fill=X)
        self.text_var = StringVar()
        Entry(self.master, textvariable=self.text_var).pack(side=BOTTOM, fill=X)
    
    def send(self):
        text = self.text_var.get()
        if text:
            self.text_var.set('')
            self.connection.send(f'{self.username}::::{self.color}::::{text}'.encode())
            Label(self.master, text=f'You: {text}', bg=self.color, anchor='w', relief='raised').pack(side=TOP, fill=X)
        
    def recv(self):
        while True:
            text = self.connection.recv(1024).decode('utf-8')
            username, color, msg = text.split('::::')
            Label(self.master, text=f'{msg} :{username}', bg=color, anchor='e', relief='raised').pack(side=TOP, fill=X)

    def connect(self, ip, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((ip, port))
        server.listen(10)
        self.connection, address = server.accept()
        self.send_btn.config(state='normal')
        self.master.bind('<Return>', lambda _: self.send())
        threading.Thread(target=self.recv).start()
        
    def init_menu(self):
        menu = Menu(self.master)
        menu.add_command(label='Personalize', command=lambda: PersonalizeDialog(self.master, self))
        menu.add_command(label='About us', command=lambda: AboutDialog(self.master))
        
        return menu
    

IP = 'localhost'
PORT = 12345
icon = 'files/server_icon.ico'

if __name__ == "__main__":
    root = Tk()
    root.title('Server')
    root.geometry('400x580+250+130')
    root.resizable(False, False)
    if os.path.exists(icon):
        root.geometry('400x600+250+130')
        root.iconbitmap(default=icon)
    root.focus_force()
    
    app = App(root)
    threading.Thread(target=app.connect, args=(IP, PORT)).start()
    
    root.mainloop()
