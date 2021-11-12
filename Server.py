import socket
from time import sleep
import threading
from ENV import Connection

# definindo o tipo de conexão
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# definindo o caminho da conexão
server.bind((Connection.HOST, Connection.PORT))
# Iniciando a conexão como servidor
server.listen()
# Guardar os chats ativos
chats = {}
# Enviar mensagens
def delivery(group: list, message):
    for pessoa in group:
        if isinstance(message, str):
            message = message.encode()
        pessoa.send(message)
# Receber mensagens dos usuários e replicá-las para os outros membros do grupo
def listener(chat, name, client):
    while True:
        message = client.recv(1024)
        message = f"{name}: {message.decode()}\n"
        delivery(chat, message)
# Loop de execução do servidor
while True:
#    Aceitando conexão do usuário
    client, addr = server.accept()
#   Solicitando o nome e o grupo no qual ele quer se conectar
    client.send(b'CONN')
#    Recebendo os dados solicitados
    nome = client.recv(1024).decode()
    sleep(1)
    sala = client.recv(1024).decode()
#   Salvando o chat e as pessoas cadastradas nele
    if sala not in chats.keys():
        chats[sala] = []
    chats[sala].append(client)
    print(f'{nome} conectou-se ao grupo {sala}! INFO: {addr}')
    delivery(chats[sala], f'{nome} entrou no grupo!\n')
#    Recurso de execução paralela para que o servidor possa atender a mais de um usuário por vez,
#    ouvindo a todos os usuários conectados
    thread = threading.Thread(target=listener, args=(sala, nome, client))
    thread.start()
