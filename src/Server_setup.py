import socket

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
port=3000
hostname='127.0.0.1'
s.bind((hostname,port))
print('Listenning at port {}'.format(s.getsockname()))
MAX_SIZE_BYTES = 65535
while True:
    data, clientAddress =s.recvfrom(MAX_SIZE_BYTES)
    message=data.decode('ascii')
    upperCaseMessage=message.upper()
    print('Client of this {} this says {}'.format(clientAddress,upperCaseMessage))
    data=upperCaseMessage.encode('ascii')
    s.sendto(data,clientAddress)








