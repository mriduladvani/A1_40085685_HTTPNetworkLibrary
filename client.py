import socket
HOST= 'www.facebook.com'

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (HOST, 80)
client_socket.connect(server_address)

request_header = 'GET / HTTP/1.0\r\nHost: '+HOST+'\r\n\r\n'
client_socket.send(request_header.encode())

response = ''
while True:
    recv = client_socket.recv(1024)
    if not recv:
        break
    response += recv.decode()

print (response)
client_socket.close()