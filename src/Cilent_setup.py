import socket

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
print('OS Assinged to address {} to me'.format(s.getsockname()))
msg=input('enter the message in the lower case')
data=msg.encode('ascii')

