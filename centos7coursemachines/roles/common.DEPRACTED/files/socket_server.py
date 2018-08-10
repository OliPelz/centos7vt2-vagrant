#!/usr/bin/python
# taken and modified from https://www.thomaschristlieb.de/ein-python-script-mit-systemd-als-daemon-systemd-tut-garnicht-weh/
import socket
import os

def echo(datagram):
      (cmd, color, tty) = datagram.split("|")
      # to learn more about color codes goto
      if(color == "whiteblue"):
          os.system("echo -e '\E[37;44m'\"\033[1m" + cmd + "\033[0m\" >" + tty)
      if(color == "whitered"):
          os.system("echo -e '\E[37;41m'\"\033[1m" + cmd + "\033[0m\" >" + tty)
      if(color == "whitegreen"):
          os.system("echo -e '\E[37;42m'\"\033[1m" + cmd + "\033[0m\" >" + tty)
      if(color == "cyan"):
          os.system("echo -e '\e[46m'"+ cmd + " > " + tty)
      if(color == "magenta"):
          os.system("echo -e '\e[105m'"+ cmd + " > " + tty)
      if(color == "greenred"):
          os.system("echo -e '\e[1;31;42m " + cmd + " \e[0m' > " + tty)

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response
while 1:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
       
    conn, addr = s.accept()
    print('Connection address:', addr)
    while 1:
        data = conn.recv(BUFFER_SIZE)
        if not data: break
        print("received data:", data)
        echo(data)
        #conn.send(data)  # echo
    conn.close()
