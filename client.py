import socket
HOST= 'www.facebook.com'

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (HOST, 80)
client_socket.connect(server_address)

params= 'username:helloworld&pass=blah\r\n'
header= """
POST HTTP/1.1
Host: www.facebook.com
Content-Type: application/x-www-form-urlencoded
Connection: keep-alive
"""
content_length= str(len(params.encode('ascii')))


x= input('Which request do you want to send?')

if(x=='GET'):
    request_header = 'GET / HTTP/1.0\r\nHost: '+HOST+'\r\n\r\n'
    client_socket.send(request_header.encode())

    response = ''
    while True:
        recv = client_socket.recv(1024)
        if not recv:
            break
        response= response+recv.decode()
else:
    request_header= header+content_length+params
    client_socket.send(request_header.encode())

    response = ''
    while True:
        recv = client_socket.recv(1024)
        if not recv:
            break
        response = response + recv.decode()


print (response)
client_socket.close()