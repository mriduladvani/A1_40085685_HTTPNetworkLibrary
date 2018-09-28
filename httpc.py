import socket
HOST = "www.ptsv2.com"
PORT = 80
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address= (HOST,PORT)
client_socket.connect(server_address)
params= "username=mridul&password=pass\r\n"
bparams= params.encode('ascii')
header = """\
POST /t/mridul/post HTTP/1.1\r
Content-Type: application/x-www-form-urlencoded\r
Content-Length: 29\r
Host: ptsv2.com\r
Connection: close\r
\r\n """
bheader = header.format(
    content_type="application/x-www-form-urlencoded",
    content_length=len(bparams),
    host=str(HOST) + ":" + str(PORT)
).encode('iso-8859-1')

request = bheader + bparams
client_socket.sendall(request)
response = client_socket.recv(1024)
print('Result : \n', response.decode())
client_socket.close()

