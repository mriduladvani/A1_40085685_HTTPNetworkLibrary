import socket
HOST = "www.httpbin.org"
PORT = 80

client_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address= (HOST, PORT)
client_socket.connect(server_address)
request_type='post'

gheader="GET / HTTP/1.0\r\nHost:www.httpbin.org/get\r\n\r\n"
pheaders = """\
POST http://www.httpbin.org/post HTTP/1.1\r
Content-Type: application/x-www-form-urlencoded\r
Content-Length: 29\r
Host: www.httpbin.org\r
Connection: close\r
\r\n """

params = 'username=mridul&password=pass'
bparams = params.encode('ascii')
bheader = pheaders.format(
    content_type="application/x-www-form-urlencoded",
    content_length=len(bparams),
    host=str(HOST) + ":" + str(PORT)
).encode('iso-8859-1')
request = bheader + bparams

if request_type== 'get':
    client_socket.send(gheader.encode())
else:
    client_socket.sendall(request)

response = client_socket.recv(1024)
print('Result : \n', response.decode())
client_socket.close()