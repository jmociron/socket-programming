import socket
import pickle
import configparser
from Ciron_src_exer01 import print_matrix, terrain_inter

s = socket.socket()
config = configparser.ConfigParser()
config.read("config.ini") 

host = config.get("Connect", "host")
port = config.getint("Connect", "port")

try:
    s.connect((host, port)) # connect to the server
except socket.error as e:
    print(str(e))

# serialized_data = bytearray()
data = bytearray()
data_size = int.from_bytes(s.recv(4), "big")

while len(data) < data_size:
    packet = s.recv(4096)
    data.extend(packet)
# while True:
#     data_chunk = s.recv(4096) # receive data
#     serialized_data.extend(data_chunk)
#     if (len(data_chunk) < data_size): # check if end of matrix is reached
#         break
# while True:
#     data_chunk = s.recv(4096) # receive data
#     serialized_data.extend(data_chunk)
#     if (len(data_chunk) < data_size): # check if end of matrix is reached
#         break
try:
    data = pickle.loads(data) # deserializing data
except pickle.UnpicklingError as e:
    print(f"Error occurred while unpickling: {e}")

terrain_inter(data)
s.send("[ACK] Client has received submatrix".encode()) # sends submatrix to client
print("Submatrix received. Client will now close.")
s.close()
