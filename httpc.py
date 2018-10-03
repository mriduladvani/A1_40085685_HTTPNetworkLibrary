# COMP 6461 Lab Assignment-1 Submitted by Mridul Advani (40085685) (m_advani@encs.concordia.ca)
# Running instructions:
# On the terminal, run:
# python httpc.py request_type(get|post) [-v] [-k key:value] [-d inline_data] [-f file] [-o write_on_file] URL



import socket
import argparse

#creating arguments for the command line implementation
parser= argparse.ArgumentParser()
parser.add_argument('request_type', type=str, help='the type of request that the user wants to send')
parser.add_argument('URL', type=str, help='signifies the request URL')
parser.add_argument('-v', '--verbose', action='store_true', help='increase output verbosity')
parser.add_argument('-k', '--header', action='append', help='the headers that are intended to be passed request' )
parser.add_argument('-d', '--data', action='append', help='the inline data intended to be passed in request')
parser.add_argument('-f', '--readfile', action='store', help='reads the content of the file to be passed in the request')
parser.add_argument('-o', '--writefile', action='store', help='to write the response of the body on a new file')
args=parser.parse_args()

url=(args.URL).split("/")   #parsing the user entered URL before / to connect with server
client_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #socket object
server_address= (url[0], 80)
client_socket.connect(server_address)   #connecting with the server

answer= args.request_type   #parsing user entered request type
params=''

string1= args.URL #spliting the URL for query parameter
string2= string1.split('?')

#condition check for GET and -d/-f to not be used simultaneously
if (args.request_type=='get') and (args.readfile):
    print('You cant ask a file to be read in a get request')
    exit(0)
elif (args.request_type=='get') and (args.data):
    print('You cannot send inline data along with a get request')
    exit(0)



#condition check for -d and -f to not be used simultaneously
if (args.readfile) and (args.data):
    print('you cant use -d and -f together')
    exit(0)
elif (args.data) and (args.readfile!=True):
    y= '&'.join(args.data)
    params=y
elif (args.data!=True) and (args.readfile):
    file=open(args.readfile, "r")
    params= file.read()

#parsing user entered headers (using -k) and passing them with request
aheaders=''
if args.header:
    for x in args.header:
        aheaders =aheaders+x+"""\r\n"""

bparams = params.encode('ascii') #encoding request to byte format

gheader="GET / HTTP/1.0\r\nHost:"+args.URL+"\r\n\r\n"  #GET request header

#POST request headers
pheaders = """\     
POST http://"""+args.URL+""" HTTP/1.1\r
Content-Type: application/json\r
Content-Length: """+str(len(params)+1)+"""\r
Host: """+args.URL+"""\r
Connection: close\r"""+"""\n"""+aheaders+"""\r
 """

#Encoding POST headers
bheader = pheaders.format(
    url= args.URL,
    content_type="application/json",
    content_length=len(bparams),
    host=str(args.URL) + ":" + str(80)
).encode('iso-8859-1')

gheader2= gheader+pheaders

request = bheader + bparams

#making request (GET and POST)
if args.request_type== 'get':
    client_socket.send(gheader2.encode())
else:
    client_socket.sendall(request)



#receiving response and decoding back to string
response = client_socket.recv(1024)
decoded_response= response.decode()

#Using rsplit to extract status code of the response
x=decoded_response.rsplit('\r\n', 1)
length= len(x)

#writing in the file functionality (-o file_name)
def writeinfile():
    file = open(args.writefile, "w+")
    file.write(x[length - 1])

#verbose and writing in file conditions
if (args.verbose) and (args.writefile):
    print(x[0])
    print('\n The message body has been written into file')
    writeinfile()
elif (args.verbose) and (args.writefile!=True):
    print(decoded_response)

elif (args.verbose!=True) and (args.writefile) :
    writeinfile()
    print('\n The response body has been written into file')

else:
    print(x[length-1])

#extracting status code of response and checking if redirect is needed
#redirect done if the status code is in 3xx form
#Redirection.py runs for redirected request and implements a POST request on httpbin.org/post
resparray= decoded_response.splitlines()
x= resparray[0].split(' ')
length= len(x)
if (x[1]>= '300') and (x[1]<'400'):
    print('The page was not found. Redirecting you to another page...\n Response from the redirected page:')
    exec(open("Redirection.py").read())

client_socket.close()   #terminating the connection