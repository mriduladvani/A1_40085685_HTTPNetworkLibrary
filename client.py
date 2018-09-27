import socket
HOST= 'www.tutorialpoint.com'

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (HOST, 80)
client_socket.connect(server_address)

params= 'licenseID=string&content=string&/paramsXML=string\r\n'
header= """
POST /cgi-bin/process.cgi HTTP/1.1
User-Agent: Mozilla/4.0 (compatible; MSIE5.01; Windows NT)
Host: www.tutorialspoint.com
Content-Type: application/x-www-form-urlencoded
Content-Length: length
Accept-Language: en-us
Accept-Encoding: gzip, deflate
Connection: Keep-Alive
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