import time
import socket
import pickle
import configparser
from Ciron_src_exer01 import assign_values, print_matrix
 
s = socket.socket()
config = configparser.ConfigParser()
config.read("config.ini") 

host = config.get("Connect", "host")
port = config.getint("Connect", "port")

n = 4001
c = 4
client_count = c
matrix = assign_values([[0 for x in range(n)] for y in range(n)])
# print_matrix(matrix)
row_start = 0

try:      
  s.bind((host, port)) # binds server socket to port
except socket.error as e:
  print(str(e))  

print(f"Server is listening on the port {port}...")
s.listen()

start = time.time()

while client_count != 0:

  if(client_count > 1):
    increment = round(int(n/c), -1)
    serialized_data = pickle.dumps(matrix[row_start:row_start+increment+1])
    row_start += increment # ensures that row (divisible by 10) with values is included in the next submatrix
  else:
    serialized_data = pickle.dumps(matrix[row_start:n])

  client, address = s.accept() # connection with client is established
  print ("\nGot connection from", address)
  
  client.sendall(len(serialized_data).to_bytes(4, "big"))
  client.sendall(serialized_data)

  client_count -= 1
  print(client.recv(4096).decode())

print("\nMatrix has been distributed. Server will now close.")
end = time.time()
print("Time elapsed:", (end-start))
s.close()