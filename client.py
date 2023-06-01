import socket
import pickle
import configparser
from Ciron_src_exer01 import print_matrix

s = socket.socket()
config = configparser.ConfigParser()
config.read("config.ini") 

host = config.get("Connect", "host")
port = config.getint("Connect", "port")

try:
    s.connect((host, port)) # connect to the server
except socket.error as e:
    print(str(e))

serialized_data = bytearray()

while True:
    data_chunk = s.recv(4096) # receive data
    serialized_data.extend(data_chunk)
    if (len(data_chunk) < 4096): # check if end of matrix is reached
        break
try:
    data = pickle.loads(serialized_data) # deserializing data
except pickle.UnpicklingError as e:
    print(f"Error occurred while unpickling: {e}")

# print_matrix(data)
s.send("[ACK] Client has received submatrix".encode()) # sends submatrix to client
print("Submatrix received. Client will now close.")
s.close()
