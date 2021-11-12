import socket
import threading
from tkinter import *
from ENV import Connection
from tkinter import simpledialog

class Chat():
    def __init__(self):
        # Definindo e estabelecendo parâmetros para conexão com servidor
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((Connection.HOST,Connection.PORT))

        # Criando as janelas para perguntas rápidas de conexão
        login = Tk()
        login.withdraw()

        self.active = True
        self.openedWindow = False

        self.name = simpledialog.askstring('Nome', 'Digite seu nome:', parent=login)
        self.sala = simpledialog.askstring('Sala', 'Digite o nome da sala que deseja entrar:', parent=login)
        thread = threading.Thread(target=self.connect())
        thread.start()
        self.window()

    def close(self):
        self.root.destroy()
        self.client.close()

    def sendMessage(self):
        message = self.txtSend.get()
        self.client.send(message.encode())
        self.txtSend.delete("1.0", 'end')

    def connect(self):
        while True:
            req = self.client.recv(1024)
            if req == b"CONN":
                self.client.send(self.name.encode())
                self.client.send(self.sala.encode())
            else:
                try:
                    self.textArea.insert('end', req.decode())
                except:
                    pass

    def window(self):
        self.root = Tk()
        self.root.geometry("400x600")
        self.root.title('Chat')
        self.textArea = Text(self.root)
        self.textArea.place(relx=0.05,
                            rely=0.01,
                            width=300,
                            height=400)
        self.txtSend = Entry(self.root)
        self.txtSend.place(relx=0.05,
                           rely=0.8,
                           width=250,
                           height=20)
        self.btnSend = Button(self.root, text='Enviar', command=self.sendMessage)
        self.btnSend.place(relx=0.7,
                           rely=0.8,
                           width=50,
                           height=20)
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.mainloop()

chat = Chat()
