import socket
import pickle

PORT = 5050
CLIENT = socket.gethostbyname(socket.gethostname())
ADDR = (CLIENT, PORT)
FORMAT = 'utf-8'
HEADER=1024

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clientsocket.connect(ADDR)

def send(msg):
    loaded_msj = pickle.dumps(msg)
    clientsocket.send(loaded_msj)
    print(clientsocket.recv(HEADER))
    print(loaded_msj)
    
text_input =bytes(input("Digite texto a ingresar: "), FORMAT)
while text_input != b"quit":
    send(text_input)
    text_input = bytes(input("Digite comando: "),FORMAT)
    if text_input == b"quit":
        send(b"Disconnect")
        clientsocket.close()