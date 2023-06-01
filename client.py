import socket
import pickle
import configparser
from Ciron_src_exer01 import terrain_inter

s = socket.socket()
config = configparser.ConfigParser()
config.read("config.ini") 

host = config.get("Connect", "host")
port = config.getint("Connect", "port")

try:
    s.connect((host, port)) # connect to the server
except socket.error as e:
    print(str(e))

data = bytearray() # submatrix will be stored here
data_size = int.from_bytes(s.recv(4), "big") # receives the size of the matrix

while len(data) < data_size:
    packet = s.recv(4096)
    data.extend(packet)

try:
    data = pickle.loads(data) 
except pickle.UnpicklingError as e:
    print(f"Error occurred while unpickling: {e}")

terrain_inter(data)
s.send("[ACK] Client has received submatrix".encode()) # sends submatrix to client
print("Submatrix received. Client will now close.")
s.close()
