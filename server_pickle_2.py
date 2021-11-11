import subprocess
import socketserver
import argparse
import pickle

HEADER=1024
PORT = 5050
HOST= "localhost"

class ConnectionHandler(socketserver.BaseRequestHandler):
    def handle(conn):
        print(f"Nuevo cliente")
        connected=True
        while connected:
            msg = conn.recv(HEADER)       
            loaded_msj = pickle.loads(msg)
            if loaded_msj == b"Disconnect":    
                connected=False
            else:
                msj = loaded_msj.split()
                proceso = subprocess.Popen(msj, stdout=subprocess.PIPE, universal_newlines=True, stderr=subprocess.PIPE)
                stdout, stderr = proceso.communicate()
                
                fail = pickle.dumps(stderr)
                conn.send(fail)
                
                output = pickle.dumps(stdout)
                conn.send(output)

class ForkTCPServer(socketserver.ForkingMixIn,socketserver.TCPServer):
    pass                
class ThreadTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--metodo", dest="tipo", required=True,default='t')
    args = parser.parse_args()

    if args.tipo.lower() == "p":
        tipo = ForkTCPServer
    
    elif args.tipo.lower() == "t":
        tipo = ThreadTCPServer
    
    with tipo ((HOST, PORT), ConnectionHandler) as server:
        server.serve_forever()