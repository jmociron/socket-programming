import socket
import pickle
import configparser
from Ciron_src_exer01 import assign_values
 
s = socket.socket()
config = configparser.ConfigParser()
config.read("config.ini") 

host = config.get("Connect", "host")
port = config.getint("Connect", "port")

n = 8001
client_count = 1
matrix = assign_values([[0 for x in range(n)] for y in range(n)])
row_start = 0


try:      
  s.bind((host, port)) # binds server socket to port
except socket.error as e:
  print(str(e))  

print(f"Server is listening on the port {port}...")
s.listen()
 
while client_count != 0:
  serialized_data = pickle.dumps(matrix[row_start:row_start+int(n/client_count)])
  row_start += int(n/client_count)
  client, address = s.accept() # connection with client is established
  print ("\nGot connection from", address)
  client.send(serialized_data)
  client_count -= 1
  print(client.recv(4096).decode())

print("\nMatrix has been distributed. Server will now close.")
s.close()